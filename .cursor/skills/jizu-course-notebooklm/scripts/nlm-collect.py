#!/usr/bin/env python3
"""
NotebookLM 分层采集脚本 — 将对话原始内容落盘，运行轨迹可追踪。

用法（仓库根目录）:
  python .cursor/skills/ai-course-notebooklm/scripts/nlm-collect.py notebooklm-raw/manifests/week3-4.json
  python .cursor/skills/ai-course-notebooklm/scripts/nlm-collect.py ... --resume notebooklm-raw/<module>/runs/latest
  python .cursor/skills/ai-course-notebooklm/scripts/nlm-collect.py merge-runs <src_run> <dst_run>

输出目录:
  notebooklm-raw/<module>/runs/<timestamp>/
    run.meta.json, run.log, manifest.snapshot.json
    <batch-id>.prompt.txt, <batch-id>.answer.md, <batch-id>.answer.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --- Paths ---
SKILL_ROOT = Path(__file__).resolve().parent.parent


def find_repo_root() -> Path:
    for ancestor in Path(__file__).resolve().parents:
        if (ancestor / "notebooklm-raw").is_dir() and (ancestor / "guides").is_dir():
            return ancestor
    raise RuntimeError("无法定位仓库根目录（需同时存在 notebooklm-raw/ 与 guides/）")


REPO_ROOT = find_repo_root()
RAW_ROOT = REPO_ROOT / "notebooklm-raw"
SKILL_DIR = Path.home() / "service/openclaw/workspace/skills/notebooklm-integration"
SKILL_SITE = SKILL_DIR / ".venv/lib/python3.12/site-packages"
SYNC_AUTH = SKILL_DIR / "scripts/sync-auth.py"
NOTEBOOKLM_CLI = SKILL_DIR / ".venv/bin/notebooklm"
DEFAULT_PROXY = "http://127.0.0.1:7897"
DEFAULT_NLM_HTTP_TIMEOUT = 120
DEFAULT_RETRIES = 3
DEFAULT_RETRY_BASE_DELAY = 15.0


def _ensure_notebooklm_import() -> None:
    if SKILL_SITE.is_dir() and str(SKILL_SITE) not in sys.path:
        sys.path.insert(0, str(SKILL_SITE))


def log(msg: str, log_file: Path | None = None) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if log_file:
        with log_file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def rel_repo(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def run_cmd(
    cmd: list[str],
    *,
    env: dict[str, str] | None = None,
    timeout: int = 180,
) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=merged,
        timeout=timeout,
        check=False,
    )


def classify_error(message: str) -> str:
    text = message.lower()
    if any(k in text for k in ("authentication", "expired", "re-authenticate", "not logged in")):
        return "auth"
    if "timed out" in text or "timeout" in text:
        return "timeout"
    if any(k in text for k in ("rate limit", "rate_limit", "quota", "too many requests")):
        return "rate_limit"
    return "unknown"


class AskError(Exception):
    def __init__(self, message: str, *, error_kind: str, stdout: str = "", stderr: str = ""):
        super().__init__(message)
        self.error_kind = error_kind
        self.stdout = stdout
        self.stderr = stderr


def ensure_auth(log_file: Path | None) -> None:
    if not SYNC_AUTH.exists():
        raise FileNotFoundError(f"sync-auth 不存在: {SYNC_AUTH}")
    log("同步认证…", log_file)
    r = run_cmd([sys.executable, str(SYNC_AUTH)], timeout=60)
    if r.returncode != 0:
        raise AskError(
            f"sync-auth 失败:\n{r.stdout}\n{r.stderr}",
            error_kind="auth",
            stdout=r.stdout,
            stderr=r.stderr,
        )
    log("认证 OK", log_file)


def notebook_use(notebook_id: str, env: dict[str, str], log_file: Path | None) -> None:
    log(f"选定 Notebook: {notebook_id}", log_file)
    r = run_cmd([str(NOTEBOOKLM_CLI), "use", notebook_id], env=env, timeout=60)
    if r.returncode != 0:
        msg = f"notebooklm use 失败:\n{r.stdout}\n{r.stderr}"
        raise AskError(msg, error_kind=classify_error(msg), stdout=r.stdout, stderr=r.stderr)


def notebook_clear(env: dict[str, str], log_file: Path | None) -> None:
    log("清空会话上下文 (notebooklm clear)", log_file)
    r = run_cmd([str(NOTEBOOKLM_CLI), "clear"], env=env, timeout=30)
    if r.returncode != 0:
        msg = f"notebooklm clear 失败:\n{r.stdout}\n{r.stderr}"
        raise AskError(msg, error_kind=classify_error(msg), stdout=r.stdout, stderr=r.stderr)


async def _ask_async(prompt: str, notebook_id: str, http_timeout: float) -> dict[str, Any]:
    _ensure_notebooklm_import()
    from notebooklm import NotebookLMClient  # noqa: WPS433

    async with await NotebookLMClient.from_storage(timeout=http_timeout) as client:
        result = await client.chat.ask(notebook_id, prompt, conversation_id=None)
    refs = [asdict(r) for r in result.references]
    return {
        "answer": result.answer,
        "conversation_id": result.conversation_id,
        "turn_number": result.turn_number,
        "is_follow_up": result.is_follow_up,
        "references": refs,
    }


def ask_notebooklm(
    prompt: str,
    notebook_id: str,
    log_file: Path | None,
    *,
    http_timeout: float,
) -> dict[str, Any]:
    log(f"提问 ({len(prompt)} 字, nlm_timeout={http_timeout}s)…", log_file)
    try:
        return asyncio.run(_ask_async(prompt, notebook_id, http_timeout))
    except Exception as e:
        msg = str(e)
        raise AskError(msg, error_kind=classify_error(msg)) from e


def ask_with_retries(
    prompt: str,
    notebook_id: str,
    log_file: Path | None,
    *,
    http_timeout: float,
    retries: int,
    retry_base_delay: float,
) -> tuple[dict[str, Any], int]:
    """返回 (answer_data, retry_count)。"""
    last_err: AskError | None = None
    for attempt in range(retries + 1):
        if attempt > 0:
            delay = retry_base_delay * (2 ** (attempt - 1))
            log(f"重试 {attempt}/{retries}，等待 {delay:.0f}s…", log_file)
            time.sleep(delay)
        try:
            data = ask_notebooklm(
                prompt,
                notebook_id,
                log_file,
                http_timeout=http_timeout,
            )
            if data.get("error"):
                raise AskError(
                    json.dumps(data, ensure_ascii=False),
                    error_kind=classify_error(json.dumps(data)),
                )
            return data, attempt
        except AskError as e:
            last_err = e
            log(f"尝试 {attempt + 1} 失败 [{e.error_kind}]: {e}", log_file)
            if e.error_kind == "auth":
                break
    assert last_err is not None
    raise last_err


def load_manifest(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def batch_done(run_dir: Path, batch_id: str) -> bool:
    md = run_dir / f"{batch_id}.answer.md"
    if md.exists() and md.stat().st_size > 0:
        return True
    legacy = run_dir / f"{batch_id}.answer.json"
    return legacy.exists()


def save_batch(
    run_dir: Path,
    batch: dict,
    answer_data: dict,
    elapsed: float,
) -> None:
    bid = batch["id"]
    (run_dir / f"{bid}.prompt.txt").write_text(batch["prompt"], encoding="utf-8")
    answer_text = answer_data.get("answer", "")
    (run_dir / f"{bid}.answer.md").write_text(answer_text, encoding="utf-8")
    payload = {
        "batch_id": bid,
        "layer": batch.get("layer"),
        "title": batch.get("title"),
        "elapsed_seconds": round(elapsed, 2),
        "conversation_id": answer_data.get("conversation_id"),
        "is_follow_up": answer_data.get("is_follow_up"),
        "answer": answer_text,
        "references": answer_data.get("references"),
        "raw": {k: v for k, v in answer_data.items() if k != "raw_response"},
    }
    (run_dir / f"{bid}.answer.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def update_meta(run_dir: Path, meta: dict) -> None:
    ok = sum(1 for b in meta.get("batches", []) if b.get("status") == "ok")
    skipped = sum(1 for b in meta.get("batches", []) if b.get("status") == "skipped")
    failed = sum(1 for b in meta.get("batches", []) if b.get("status") == "error")
    total = meta.get("batches_total") or 0
    meta["batches_completed"] = ok + skipped
    meta["batches_ok"] = ok
    meta["batches_skipped"] = skipped
    meta["batches_failed"] = failed
    meta["batches_pending"] = max(0, total - ok - skipped - failed)
    (run_dir / "run.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_meta(run_dir: Path) -> dict | None:
    p = run_dir / "run.meta.json"
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def resolve_run_dir(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def list_run_dirs(module: str) -> list[Path]:
    runs_root = RAW_ROOT / module / "runs"
    if not runs_root.is_dir():
        return []
    return sorted(
        [p for p in runs_root.iterdir() if p.is_dir() and not p.name.startswith("_")],
        key=lambda p: p.name,
        reverse=True,
    )


def find_latest_incomplete_run(module: str) -> Path | None:
    for run_dir in list_run_dirs(module):
        meta = load_meta(run_dir)
        if meta is None:
            if any(run_dir.glob("*.answer.md")):
                return run_dir
            continue
        status = meta.get("status", "")
        if status in ("completed",):
            continue
        if status in ("partial", "partial_error", "running", "error", "failed"):
            return run_dir
        pending = meta.get("batches_pending")
        if pending is not None and pending > 0:
            return run_dir
    return None


def update_latest_link(module: str, run_dir: Path) -> None:
    link = RAW_ROOT / module / "runs" / "latest"
    rel = os.path.relpath(run_dir, link.parent)
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(rel)


def batch_ids_in_meta(meta: dict) -> set[str]:
    return {b["id"] for b in meta.get("batches", []) if "id" in b}


def merge_run_batch(src: Path, dst: Path, batch_id: str, *, force: bool) -> bool:
    if batch_done(dst, batch_id) and not force:
        return False
    copied = False
    for ext in (".prompt.txt", ".answer.md", ".answer.json"):
        s = src / f"{batch_id}{ext}"
        if s.exists():
            shutil.copy2(s, dst / s.name)
            copied = True
    return copied


def cmd_merge_runs(args: argparse.Namespace) -> int:
    src = resolve_run_dir(args.src)
    dst = resolve_run_dir(args.dst)
    if not src.is_dir():
        print(f"源 run 不存在: {src}", file=sys.stderr)
        return 1
    if not dst.is_dir():
        print(f"目标 run 不存在: {dst}", file=sys.stderr)
        return 1

    only_ids = {x.strip() for x in args.only.split(",") if x.strip()} if args.only else None
    if only_ids:
        batch_ids = sorted(only_ids)
    else:
        batch_ids = sorted(
            {
                p.name.replace(".answer.md", "")
                for p in src.glob("*.answer.md")
            }
        )

    if not batch_ids:
        print("未找到可合并的 batch", file=sys.stderr)
        return 1

    merged: list[str] = []
    skipped: list[str] = []
    for bid in batch_ids:
        if merge_run_batch(src, dst, bid, force=args.force):
            merged.append(bid)
            log(f"合并 {bid}: {rel_repo(src)} → {rel_repo(dst)}")
        else:
            skipped.append(bid)

    log(f"合并完成: {len(merged)} 个 batch 已复制, {len(skipped)} 个跳过")
    if merged:
        log(f"  已合并: {', '.join(merged)}")
    if skipped:
        log(f"  已跳过: {', '.join(skipped)}")
    return 0 if merged or not batch_ids else 1


def init_or_load_meta(
    run_dir: Path,
    *,
    module: str,
    notebook_id: str,
    manifest_path: Path,
    batches_total: int,
    resume: bool,
) -> dict:
    if resume and (run_dir / "run.meta.json").exists():
        meta = load_meta(run_dir) or {}
        meta["status"] = "running"
        meta["batches_total"] = batches_total
        meta.pop("error", None)
        return meta

    return {
        "module": module,
        "notebook_id": notebook_id,
        "manifest": rel_repo(manifest_path),
        "run_dir": rel_repo(run_dir),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": None,
        "batches_total": batches_total,
        "batches_completed": 0,
        "batches_ok": 0,
        "batches_skipped": 0,
        "batches_failed": 0,
        "batches_pending": batches_total,
        "batches": [],
        "status": "running",
    }


def finalize_status(meta: dict, *, fail_fast_aborted: bool) -> str:
    failed = meta.get("batches_failed", 0)
    ok = meta.get("batches_ok", 0)
    skipped = meta.get("batches_skipped", 0)
    total = meta.get("batches_total", 0)
    if fail_fast_aborted:
        return "failed"
    if failed > 0:
        return "partial" if (ok + skipped) > 0 else "failed"
    if ok + skipped >= total:
        return "completed"
    return "partial"


def cmd_collect(args: argparse.Namespace) -> int:
    manifest_path = args.manifest if args.manifest.is_absolute() else REPO_ROOT / args.manifest
    if not manifest_path.exists():
        print(f"manifest 不存在: {manifest_path}", file=sys.stderr)
        return 1

    mf = load_manifest(manifest_path)
    module = mf["module"]
    notebook_id = mf["notebook_id"]
    all_batches: list[dict] = mf["batches"]
    only_ids = {x.strip() for x in args.only.split(",") if x.strip()}
    batches = [b for b in all_batches if b["id"] in only_ids] if only_ids else list(all_batches)
    if not batches:
        print("没有可执行的 batch", file=sys.stderr)
        return 1

    resume = args.resume
    if only_ids and not resume:
        auto = find_latest_incomplete_run(module)
        if auto:
            resume = auto
            log(f"--only 未指定 --resume，自动续跑: {rel_repo(auto)}")
        else:
            print(
                "使用 --only 补采时请指定 --resume <canonical_run>，"
                "或先存在未完成的 run 以供自动续跑",
                file=sys.stderr,
            )
            return 1

    if resume:
        run_dir = resolve_run_dir(resume)
    else:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir = RAW_ROOT / module / "runs" / ts

    if args.dry_run:
        log(f"模块: {module} | 批次数: {len(batches)} | 输出: {run_dir}")
        for i, b in enumerate(batches, 1):
            done = "✓" if resume and batch_done(run_dir, b["id"]) else " "
            log(
                f"  {i}. [{done}] [{b.get('layer', '?')}] {b['id']} "
                f"clear={b.get('clear_conversation', False)}"
            )
        log("dry-run 结束")
        return 0

    run_dir.mkdir(parents=True, exist_ok=True)
    log_file = run_dir / "run.log"

    snap = run_dir / "manifest.snapshot.json"
    if not snap.exists() or not resume:
        snap.write_text(json.dumps(mf, ensure_ascii=False, indent=2), encoding="utf-8")

    is_resume = bool(resume and run_dir.exists())
    meta = init_or_load_meta(
        run_dir,
        module=module,
        notebook_id=notebook_id,
        manifest_path=manifest_path,
        batches_total=len(all_batches),
        resume=is_resume,
    )
    update_meta(run_dir, meta)

    log(f"模块: {module} | 批次数: {len(batches)} | 输出: {run_dir}", log_file)
    if not NOTEBOOKLM_CLI.exists():
        print(f"notebooklm CLI 不存在: {NOTEBOOKLM_CLI}", file=sys.stderr)
        return 1

    proxy_env = {
        "HTTP_PROXY": args.proxy,
        "HTTPS_PROXY": args.proxy,
    }

    run_t0 = time.time()
    total_retries = 0
    fail_fast_aborted = False
    already_logged = batch_ids_in_meta(meta)

    try:
        if not args.no_auth:
            ensure_auth(log_file)
        notebook_use(notebook_id, proxy_env, log_file)

        for i, batch in enumerate(batches, 1):
            bid = batch["id"]
            if is_resume and batch_done(run_dir, bid):
                if bid not in already_logged:
                    log(f"跳过已完成 batch {i}/{len(batches)}: {bid}", log_file)
                    meta["batches"].append({"id": bid, "status": "skipped"})
                    already_logged.add(bid)
                    update_meta(run_dir, meta)
                continue

            log(f"--- batch {i}/{len(batches)}: [{batch.get('layer')}] {bid} ---", log_file)

            if batch.get("clear_conversation"):
                notebook_clear(proxy_env, log_file)

            t0 = time.time()
            try:
                answer_data, retry_count = ask_with_retries(
                    batch["prompt"],
                    notebook_id,
                    log_file,
                    http_timeout=args.nlm_timeout,
                    retries=args.retries,
                    retry_base_delay=args.retry_base_delay,
                )
                total_retries += retry_count
                elapsed = time.time() - t0
                save_batch(run_dir, batch, answer_data, elapsed)
                log(
                    f"完成 {bid} ({elapsed:.1f}s"
                    + (f", 重试 {retry_count} 次)" if retry_count else ")"),
                    log_file,
                )
                meta["batches"] = [b for b in meta["batches"] if b.get("id") != bid]
                meta["batches"].append(
                    {
                        "id": bid,
                        "layer": batch.get("layer"),
                        "status": "ok",
                        "elapsed_seconds": round(elapsed, 2),
                        "retry_count": retry_count,
                        "conversation_id": answer_data.get("conversation_id"),
                    }
                )
            except AskError as e:
                elapsed = time.time() - t0
                log(f"失败 {bid} ({elapsed:.1f}s) [{e.error_kind}]: {e}", log_file)
                meta["batches"] = [b for b in meta["batches"] if b.get("id") != bid]
                meta["batches"].append(
                    {
                        "id": bid,
                        "layer": batch.get("layer"),
                        "status": "error",
                        "error_kind": e.error_kind,
                        "error": str(e),
                        "elapsed_seconds": round(elapsed, 2),
                    }
                )
                update_meta(run_dir, meta)
                if args.fail_fast:
                    fail_fast_aborted = True
                    raise
                continue

            update_meta(run_dir, meta)
            if i < len(batches) and args.delay > 0:
                log(f"等待 {args.delay}s…", log_file)
                time.sleep(args.delay)

        final_status = finalize_status(meta, fail_fast_aborted=fail_fast_aborted)
        meta["status"] = final_status
        meta["finished_at"] = datetime.now(timezone.utc).isoformat()
        meta["total_elapsed_seconds"] = round(time.time() - run_t0, 2)
        meta["total_retry_count"] = total_retries
        update_meta(run_dir, meta)

        if final_status == "completed":
            update_latest_link(module, run_dir)

        failed_ids = [b["id"] for b in meta["batches"] if b.get("status") == "error"]
        summary = (
            f"采集结束: status={final_status} | "
            f"ok={meta['batches_ok']} skipped={meta['batches_skipped']} "
            f"failed={meta['batches_failed']}/{meta['batches_total']} | "
            f"重试 {total_retries} 次 | 耗时 {meta['total_elapsed_seconds']}s"
        )
        if failed_ids:
            summary += f" | 待重跑: {', '.join(failed_ids)}"
        log(summary, log_file)

        return 0 if final_status == "completed" else 1

    except Exception as e:
        log(f"运行中止: {e}", log_file)
        meta["status"] = "failed"
        meta["finished_at"] = datetime.now(timezone.utc).isoformat()
        meta["error"] = str(e)
        update_meta(run_dir, meta)
        return 1


def build_collect_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NotebookLM 分层采集并落盘")
    parser.add_argument("manifest", type=Path, help="manifest JSON 路径")
    add_collect_args(parser)
    return parser


def build_merge_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="合并补采 run 到 canonical run")
    parser.add_argument("src", type=Path, help="源 run 目录")
    parser.add_argument("dst", type=Path, help="目标 canonical run 目录")
    parser.add_argument("--only", type=str, default="", help="逗号分隔 batch id")
    parser.add_argument("--force", action="store_true", help="覆盖目标已有 batch")
    return parser


def add_collect_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--only", type=str, default="", help="逗号分隔的 batch id")
    p.add_argument("--dry-run", action="store_true", help="只打印计划，不调用 API")
    p.add_argument("--resume", type=Path, default=None, help="续跑已有 run 目录")
    p.add_argument("--delay", type=float, default=3.0, help="批次间等待秒数（默认 3）")
    p.add_argument("--timeout", type=int, default=180, help="subprocess 外层超时（默认 180）")
    p.add_argument(
        "--nlm-timeout",
        type=float,
        default=DEFAULT_NLM_HTTP_TIMEOUT,
        help=f"notebooklm-py HTTP 读超时（默认 {DEFAULT_NLM_HTTP_TIMEOUT}s）",
    )
    p.add_argument(
        "--retries",
        type=int,
        default=DEFAULT_RETRIES,
        help=f"单 batch 失败重试次数（默认 {DEFAULT_RETRIES}）",
    )
    p.add_argument(
        "--retry-base-delay",
        type=float,
        default=DEFAULT_RETRY_BASE_DELAY,
        help=f"重试指数退避基数秒（默认 {DEFAULT_RETRY_BASE_DELAY}）",
    )
    p.add_argument(
        "--fail-fast",
        action="store_true",
        help="遇错即停（默认继续跑完其余 batch）",
    )
    p.add_argument("--no-auth", action="store_true", help="跳过 sync-auth")
    p.add_argument("--proxy", type=str, default=DEFAULT_PROXY, help="HTTP 代理")


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "merge-runs":
        args = build_merge_parser().parse_args(sys.argv[2:])
        return cmd_merge_runs(args)

    args = build_collect_parser().parse_args()
    return cmd_collect(args)


if __name__ == "__main__":
    sys.exit(main())
