# 课件04补采失败排查报告

> **排查日期**：2026-06-24  
> **manifest**：`notebooklm-raw/manifests/kejian04-supplement-machine-representation.json`  
> **失败 run**：`notebooklm-raw/kejian04-supplement-machine-representation/runs/20260624-154046`（已删除，避免提交失败 raw）  
> **处理原则**：已停止补采进程；不再运行 `nlm-collect`；不再重试 NotebookLM。

---

## 1. 哪些 batch 失败

本次正式运行开始于 15:40:46。`run.meta.json` 在停止前记录：

| batch | 状态 | error_kind | elapsed |
|-------|------|------------|---------|
| `kejian04-supp-mips-isa-example` | error | `unknown` | 213.85s |
| `kejian04-supp-mips-fields` | error | `unknown` | 213.51s |
| `kejian04-supp-program-memory-register` | pending / interrupted | - | 已开始提问后被停止 |
| `kejian04-supp-mips-vs-riscv-boundary` | pending | - | 未执行 |
| `kejian04-supp-question-types` | pending | - | 未执行 |

因此严格说不是 5 个 batch 都完整失败，而是前 2 个 batch 均连续失败；第 3 个刚开始后按用户要求停止。由于前两个短 prompt 都呈现同类错误，继续跑剩余 batch 没有价值。

---

## 2. 错误表现

日志关键现象：

1. 认证阶段成功：`同步认证…` 后显示 `认证 OK`。
2. Notebook 选择成功：显示 `选定 Notebook: e87c0462-b512-40df-8d6a-a0f5d4d30c81`。
3. 每个 batch 都能进入 `清空会话上下文` 和 `提问`。
4. 失败发生在提问阶段，均为 `尝试 N 失败 [unknown]:`，错误消息为空。
5. 每次失败大约 28-30 秒返回，不是 prompt 长度导致的 120s 超时。
6. `dry-run` 已通过，说明 manifest JSON 可解析、batch id/title/prompt 基本格式无问题。

---

## 3. 最可能原因排序

| 排名 | 可能原因 | 判断 |
|------|----------|------|
| 1 | NotebookLM / API 当前状态异常或上游返回空错误 | 最可能。认证、选 notebook、清上下文都成功，失败集中在提问 API；同一错误跨两个 batch 稳定复现，且错误体为空。 |
| 2 | API 限流或临时风控 | 较可能。历史 deep 采集刚密集运行过，本次每次约 30s 后 `unknown`，像上游拒绝/无响应被脚本归类为 unknown。 |
| 3 | 脚本对当前 NotebookLM 返回格式兼容性问题 | 较可能。`error_kind=unknown` 且 `error=""` 说明脚本没拿到可解释错误；若 NotebookLM 页面/API 返回结构变了，也会表现为 unknown。 |
| 4 | source 名称或 Notebook source 匹配问题 | 可能性中等偏低。旧 `kejian04-deep.json` 使用过 `课件04-指令系统`、`4_指令系统.pdf`，本 manifest 也沿用；source 名不匹配通常不应导致提问 API 空错误，而是回答质量差或引用不到资料。 |
| 5 | manifest 格式问题 | 低。`dry-run` 成功，正式运行能解析 5 个 batch 并生成 snapshot/meta/log。 |
| 6 | prompt 太长 | 低。失败 prompt 约 190-212 中文字，明显短于已有成功 deep prompt；且不是 120s 超时。 |
| 7 | 认证失败 | 低。日志明确 `认证 OK` 并选中 Notebook；但仍可单独做只读认证检查来排除“认证刚过期/权限半失效”。 |
| 8 | 代理问题 | 低到中等。若代理抖动也可能导致提问阶段失败，但认证和选 notebook 成功说明网络不是完全不可用。 |

---

## 4. 如何验证

后续验证应按“最小、只验证一个变量”的原则，不要直接跑 5 batch：

1. **只做认证/环境检查**：用脚本文档支持的认证检查命令或只读检查确认 token、代理和 Notebook 可达，不发起采集。
2. **检查 Notebook source 名称**：核对 NotebookLM source list 中是否仍有 `课件04-指令系统` / `4_指令系统.pdf`，并确认没有被重命名。
3. **用旧成功 manifest 对比**：只比较 `kejian04-deep.json` 与本补采 manifest 的字段结构，不运行采集；确认 module、notebook_id、workflow、clear_conversation 写法一致。
4. **人工/单 batch 最小 prompt 验证**：待 NotebookLM 状态稳定后，只运行一个极短 batch，例如“请列出课件04第二讲标题，标注来源”，不要直接跑完整补采。
5. **检查脚本错误分类**：如果仍是 `[unknown]:` 空错误，应优先看 `nlm-collect.py` 对 NotebookLM CLI/API stderr/stdout 的捕获逻辑，确认是否吞掉了真实错误。

---

## 5. 建议的最小下一步

当前不要继续补采。建议下一次只做：

```bash
python3 .cursor/skills/jizu-course-notebooklm/scripts/nlm-collect.py \
  notebooklm-raw/manifests/kejian04-supplement-machine-representation.json \
  --dry-run
```

确认 manifest 仍可解析后，先人工或用脚本跑 **一个极短、单 batch、单问** 的临时验证 manifest；若仍返回 `[unknown]:` 空错误，则问题在 NotebookLM/API/脚本兼容性，而不是课件04补采 prompt 本身。

本次已保留：

- `notebooklm-raw/kejian04/review-notes.md`
- `notebooklm-raw/manifests/kejian04-supplement-machine-representation.json`
- `notebooklm-raw/kejian04/collection-failure-report.md`

本次已删除：

- `notebooklm-raw/kejian04-supplement-machine-representation/runs/20260624-154046`
