# 计组课件轨 — NotebookLM 采集目录

> **用途**：按 **12 章课件 PDF** 顺序梳理（双轨工作流的课件轨），与周次 part 采集（`part1-week1-3` 等）并行。  
> **索引**：`guides/计组-课件梳理索引.md`  
> **Manifest**：`notebooklm-raw/manifests/kejian-discovery.json`（L0 结构发现）

---

## 流水线

```
kejian-discovery.json (L0, 12 batch)
        ↓ nlm-collect.py
kejian/runs/<ts>/*.answer.md
        ↓ Agent 通读
kejian/structure-map.md          ← 汇总 12 章 Part 边界与覆盖索引
        ↓ 按 Part 编写
manifests/kejian{NN}-deep.json (L1+, 待生成)
        ↓
guides/计组-课件{NN}-学习指南.md
```

| 阶段 | 产出 | 说明 |
|------|------|------|
| **discovery** | `kejian/runs/<ts>/kejian*-structure.answer.md` | 仅结构：Part/Slide/重要度/课堂覆盖/讲解不足 |
| **structure-map** | `kejian/structure-map.md` | discovery 完成后由 Agent 汇总 |
| **deep** | `kejian/runs/<ts>/` + `kejian{NN}-deep.json` | 按 Part 单问深采（待 structure-map） |
| **整合** | `guides/计组-课件{NN}-学习指南.md` | 见 `docs/integration-guide.md` §课件指南整合规范 |

---

## 采集命令

在仓库根目录执行（采集前确认 NotebookLM 认证，见 auth-sop.md）：

```bash
NLM=.cursor/skills/jizu-course-notebooklm/scripts/nlm-collect.py

# 预览 12 个 batch
python $NLM notebooklm-raw/manifests/kejian-discovery.json --dry-run

# L0：12 份课件结构发现（Phase 0.5，先跑这个）
python $NLM notebooklm-raw/manifests/kejian-discovery.json --delay 8

# 续跑 / 单 batch 补采
python $NLM notebooklm-raw/manifests/kejian-discovery.json \
  --resume notebooklm-raw/kejian/runs/latest

python $NLM notebooklm-raw/manifests/kejian-discovery.json \
  --only kejian05-structure --resume notebooklm-raw/kejian/runs/latest
```

**Notebook ID**：`e87c0462-b512-40df-8d6a-a0f5d4d30c81`

---

## NotebookLM Source 与本地 PDF 对照

| 本地 PDF | NotebookLM Source（常见） |
|----------|---------------------------|
| `1_计算机系统概述.pdf` | `课件01-计算机系统概述` |
| `2_数据的机器级表示.pdf` | `课件02-数据的机器级表示` |
| `3_运算方法和运算部件.pdf` | `课件03-运算方法和运算部件` |
| `4_指令系统.pdf` | `课件04-指令系统` |
| `5_中央处理器.pdf` | `课件05-中央处理器` |
| `5_指令级并行.pdf` | `课件06-指令级并行` |
| `6_指令流水线.pdf` | `课件07-指令流水线` |
| `7_互连网络.pdf` | `课件08-互连网络` |
| `7_层次结构存储系统.pdf` | `课件09-层次结构存储系统` |
| `8_线程级并行.pdf` | `课件10-线程级并行` |
| `9_MIPS32流水线处理器.pdf` | `课件12-MIPS32` |
| `10_向量体系结构.pdf` | `课件11-向量体系结构` |

> PDF 文件名编号与 NotebookLM source 编号不完全一致（5b→06、7a→08 等），prompt 中已双写。

---

## 目录结构（预期）

```
notebooklm-raw/kejian/
├── README.md                 ← 本文件
├── structure-map.md          ← discovery 后产出（待）
└── runs/
    └── <timestamp>/
        ├── run.meta.json
        ├── kejian01-structure.answer.md
        └── …
```
