# 环境与排错

> **认证权威 SOP**：`~/service/openclaw/workspace/skills/notebooklm-integration/docs/auth-sop.md`

## 认证（Windows 登录 + WSL 同步）

WSL **不能**登录。认证只在 Windows 完成，WSL 只同步文件。

### 1. Windows 登录（用户手动）

桌面快捷：`C:\Users\Sum\Desktop\notebooklm-login.ps1`

或 PowerShell：

```powershell
cd E:\_WSL\Cowork\notebooklm-py_Prepare
.\venv\Scripts\Activate.ps1
python fix_login_edge.py
```

- Edge 弹出 → 登录 Google → NotebookLM 首页后自动保存
- 首次登录若卡在等待：脚本会自动刷新；仍不行则再运行一次脚本

### 2. WSL 同步（Agent 可执行）

```bash
cd ~/service/openclaw/workspace/skills/notebooklm-integration
source .venv/bin/activate
export https_proxy=http://127.0.0.1:7897 http_proxy=http://127.0.0.1:7897

python3 scripts/sync-auth.py --force
python3 scripts/sync-auth.py --check
```

`nlm-collect.py` 采集前会自动跑 `sync-auth.py`（无 `--refresh`）。

### Agent 认证失败时

1. **停止**采集，不要尝试 `notebooklm login` 或 WSL 浏览器
2. 告知用户按上文 Windows 步骤登录
3. 用户确认后执行 `sync-auth.py --force` 并 `--check`
4. 再继续 `nlm-collect.py`

### 认证过期症状

- `notebooklm` 报 token fetch / Authentication expired
- `nlm-collect.py` 在 sync-auth 阶段失败
- CLI 提示 `Run 'notebooklm login'` → **不适用**，走 Windows + sync-auth

## 代理

默认 `http://127.0.0.1:7897`（`sync-auth` 与 `nlm-collect` 已内置）。

## 常见问题

### notebooklm use 短 UUID

`chat.ask()` 需要完整 UUID。用 `notebooklm list` 查看并更新 manifest。

### nlm-collect 超时

增加 `--delay` 或 `export NLM_DELAY=15`；默认 `--nlm-timeout 120`、`--retries 3`。

### 部分 batch 失败

`--only <batch-id> --resume notebooklm-raw/<module>/runs/latest` 或 `merge-runs`。
