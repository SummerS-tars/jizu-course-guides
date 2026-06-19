#!/usr/bin/env bash
# 续跑剩余 9 章 deep 采集（05b/07b/08 已完成则跳过）
set -euo pipefail
cd "$(dirname "$0")/../.."
NLM="python3 .cursor/skills/jizu-course-notebooklm/scripts/nlm-collect.py"
DELAY=8
LOG="notebooklm-raw/kejian/deep-collection.log"

log() { echo "[$(date -Iseconds)] $*" | tee -a "$LOG"; }

is_done() {
  local mod="$1"
  local latest="notebooklm-raw/${mod}/runs/latest"
  [[ -L "$latest" ]] && compgen -G "notebooklm-raw/${mod}/runs/latest/*-mistakes.answer.md" > /dev/null
}

ORDER=(01 04 05 06 02 03 07a 09 10)
for id in "${ORDER[@]}"; do
  mod="kejian${id}"
  if is_done "$mod"; then
    log "skip $mod (mistakes batch exists)"
    continue
  fi
  log "collect $mod"
  $NLM "notebooklm-raw/manifests/${mod}-deep.json" --delay "$DELAY" 2>&1 | tee -a "$LOG"
done
log "remaining deep collection done"
