#!/usr/bin/env bash
# 计组课件轨 12 章 deep 采集顺序（--delay 8）
# 用法：在仓库根目录 bash notebooklm-raw/kejian/run-all-deep.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
NLM="python3 .cursor/skills/jizu-course-notebooklm/scripts/nlm-collect.py"
DELAY=8

log() { echo "[$(date -Iseconds)] $*"; }

# 续跑 cb7c572b 未完成批次
if [[ -d notebooklm-raw/kejian05b/runs/20260619-222348 ]]; then
  log "resume kejian05b"
  $NLM notebooklm-raw/manifests/kejian05b-deep.json \
    --resume notebooklm-raw/kejian05b/runs/20260619-222348 --delay "$DELAY"
fi
if [[ -d notebooklm-raw/kejian08/runs/20260619-222348 ]]; then
  log "resume kejian08"
  $NLM notebooklm-raw/manifests/kejian08-deep.json \
    --resume notebooklm-raw/kejian08/runs/20260619-222348 --delay "$DELAY"
fi

# 07b 已有完整 answer，跳过
ORDER=(01 04 05 06 02 03 07a 09 10)
for id in "${ORDER[@]}"; do
  mod="kejian${id}"
  manifest="notebooklm-raw/manifests/${mod}-deep.json"
  latest="notebooklm-raw/${mod}/runs/latest"
  if [[ -L "$latest" ]] && compgen -G "notebooklm-raw/${mod}/runs/latest/*-mistakes.answer.md" > /dev/null; then
    log "skip $mod (latest has mistakes batch)"
    continue
  fi
  log "collect $mod"
  $NLM "$manifest" --delay "$DELAY"
done

log "all deep collection done"
