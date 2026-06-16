# 环境与排错

## 认证

### Windows→WSL 同步

1. Windows 侧用 Edge 浏览器登录 Google 账号（`fix_login_edge.py`）
2. WSL 侧运行同步脚本：
   ```bash
   cd ~/service/openclaw/workspace/skills/notebooklm-integration
   source .venv/bin/activate
   python3 scripts/sync-auth.py
   ```
3. 验证：`notebooklm list` 应正常显示 notebook 列表

### 认证过期症状
- `notebooklm` 命令报 AuthError / 401
- `nlm-collect.py` 卡住不返回

**修复**：重新在 Windows 侧运行 `fix_login_edge.py`，再同步。

## 代理

WSL 内访问 Google 需要代理。`nlm-collect.py` 默认使用 `http://127.0.0.1:7897`。

```bash
# 确认代理可用
curl -x http://127.0.0.1:7897 https://www.google.com -o /dev/null -w "%{http_code}"
```

## 常见问题

### notebooklm use 报短 UUID 错误

`notebooklm use e87c0462` 可能失败。需要完整 UUID（格式：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）。

获取完整 UUID：
```bash
notebooklm list
# 或
notebooklm notebook list
```

### nlm-collect.py 超时

增加 `--delay` 值（默认建议 8~12 秒），或设置环境变量：
```bash
export NLM_DELAY=15
```

### NotebookLM 返回空答案

可能是 prompt 太复杂或 source 不足。排查：
1. 检查 `run.log` 中的 HTTP 状态
2. 手动在 NotebookLM Web UI 验证该问题
3. 拆分 prompt 为更小的子问题
