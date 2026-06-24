# NotebookLM 认证/验证差异诊断

> **日期**：2026-06-24  
> **范围**：AI H 与计组 H NotebookLM skill / `nlm-collect.py` / SOP / Windows 登录脚本  
> **原则**：只做认证与极简链路验证，不执行补采。

## 结论

本轮未发现“计组 H 仍使用旧认证逻辑、AI H 使用新认证逻辑”的脚本差异。AI H 与计组 H 的 `nlm-collect.py` 功能代码一致，仅文件头用法示例不同；两者都使用系统级 `~/service/openclaw/workspace/skills/notebooklm-integration/scripts/sync-auth.py`，并默认设置 `http://127.0.0.1:7897` 代理、`notebooklm use`、`notebooklm clear`、Python API `NotebookLMClient.from_storage()`。

当前认证链路可用：`sync-auth.py --check` 通过，计组 Notebook `use` 成功，`source list --json` 成功返回 86 个 ready source，极简 `notebooklm ask` 也返回正常 JSON。因此，课件04此前 `[unknown]:` 空错误更像是 NotebookLM/API 当时的提问阶段瞬态异常、上游空响应、限流/风控或脚本对空异常分类不足，不是当前可复现的认证失效。

## AI H vs 计组 H 差异

| 项 | AI H | 计组 H | 判断 |
|---|---|---|---|
| `nlm-collect.py` | 系统级 `sync-auth.py`，默认代理，120s HTTP timeout，3 次重试 | 同功能代码 | 无认证逻辑差异 |
| Skill 认证说明 | 指向系统级 `auth-sop.md`，禁止 WSL 登录/`--refresh` | 同样指向系统级 `auth-sop.md`，并列出 Windows/WSL 分工 | 无落后逻辑 |
| troubleshooting | AI 文档更明确提到 `auth check --test`、短 UUID 报错、超时分类 | 计组文档有同类 SOP，但更像本地摘要 | 可补充但非 bug |
| manifest 模板 | AI Notebook ID | 原先也误写 AI Notebook ID | 计组模板 bug，已修复 |
| 既有计组 manifest | 使用 `e87c0462-b512-40df-8d6a-a0f5d4d30c81` | 使用计组完整 UUID | 课件04失败不是由现有 manifest ID 写错导致 |

已修复：`.cursor/skills/jizu-course-notebooklm/templates/manifest-template.json` 中的 Notebook ID 和 AI 课程语境已改为计组 H。

## 系统级认证脚本

权威 SOP：`~/service/openclaw/workspace/skills/notebooklm-integration/docs/auth-sop.md`。

核心流程：

1. Windows 侧运行 `fix_login_edge.py` 或桌面 `notebooklm-login.ps1`，保存 `C:\Users\Sum\.notebooklm\storage_state.json`。
2. WSL 侧运行 `sync-auth.py`，同步到 `~/.notebooklm/storage_state.json`。
3. `sync-auth.py --check` 调用 `.venv/bin/notebooklm auth check --test`，判断 `token_fetch` 是否成功。

这说明 `sync-auth.py --check` 的覆盖面主要是“storage 文件存在、cookie 可读、token fetch 能过”。它不验证某个课程 Notebook 的 `use`、`source list`、`chat.ask()` 是否都能完成。因此理论上存在 `--check` 通过但 ask 失败的情况，尤其是上游返回空错误、单 notebook 权限/状态异常、代理抖动或 NotebookLM API 变更时。

## Windows 侧脚本要点

桌面脚本：`C:\Users\Sum\Desktop\notebooklm-login.ps1`。

行为：

- 切到 `E:\_WSL\Cowork\notebooklm-py_Prepare`。
- 激活 Windows venv。
- 执行 `python fix_login_edge.py`。
- 成功后提示 WSL 运行 `python3 scripts/sync-auth.py --force`。

实际登录逻辑在 `fix_login_edge.py`：

- 使用 Edge persistent profile：`%USERPROFILE%\.notebooklm\browser_profile`。
- 等待页面从 Google 登录跳回 `notebooklm.google.com`。
- 检查页面 HTML 中的 `SNlM0e` 或 `FdrFJe` token 标记。
- 若 NotebookLM 已打开但 token 未就绪，会自动刷新一次。
- 保存前先访问 `accounts.google.com` 再回 NotebookLM，以补齐 Google cookie 域。
- 最终保存 `%USERPROFILE%\.notebooklm\storage_state.json`。

这是增强过的 Windows 登录/保存逻辑；计组 H 和 AI H 都通过同一个系统级 `sync-auth.py` 消费该文件。

## 本轮低风险验证

| 验证 | 结果 |
|---|---|
| `sync-auth.py --status` | Windows/WSL `storage_state.json` 均存在，mtime 相同，auth valid |
| `sync-auth.py --check` | `认证有效` |
| `notebooklm use e87c0462-b512-40df-8d6a-a0f5d4d30c81` | 成功选中“计算机组成与体系结构 Notebook” |
| `notebooklm source list --json` | 成功，返回 `count: 86`，source 均为 ready |
| 极简 `notebooklm ask "请只回答：认证问答验证 OK。" --json` | 成功，返回 `answer: 认证问答验证 OK。` |

## 对课件04失败的判断

`collection-failure-report.md` 中记录的 v2 失败发生在认证恢复后，错误仍为空 `unknown`。结合本轮极简 ask 已成功，最合理判断是：

1. 不是计组 H 与 AI H 认证脚本不一致导致。
2. 不是当前认证不可用导致。
3. 旧失败仍可能来自当时 NotebookLM 提问 API 的空响应、限流/风控、临时服务状态，或 `nlm-collect.py` 对空异常没有抓到更多上下文。
4. `sync-auth.py --check` 确实不够充分，不能单独作为“采集一定可用”的判定；后续排错应至少增加 `use + source list + 极简 ask` 三段式验证。

## 后续建议

- 不要基于本诊断盲目补采课件04。
- 若再次补采，先只运行一个极短单 batch，并设置 `--fail-fast`；若再出现空 `unknown`，优先增强 `nlm-collect.py` 的异常捕获与日志，而不是重复登录。
- 可考虑把计组 troubleshooting 中的“认证检查”升级为三段式：`sync-auth.py --check` → `notebooklm use` → `source list/极简 ask`。
