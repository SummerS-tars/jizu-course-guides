# 计组课件轨 — NotebookLM 采集目录

> **用途**：按 **12 章课件 PDF** 顺序梳理（双轨工作流的课件轨），与周次 part 采集（`part1-week1-3` 等）并行。  
> **索引**：`guides/计组-课件梳理索引.md`  
> **进度**：12/12 deep manifest ✅；deep 采集 3/12 完成（07b、05b、08）；其余待 NotebookLM API 恢复后续跑

---

## 流水线

```
kejian-discovery.json (L0, 12 batch)  ✅
        ↓
kejian/runs/latest/*-structure.answer.md
        ↓
kejian/structure-map.md               ✅
        ↓
manifests/kejian{NN}-deep.json (12)    ✅
        ↓ nlm-collect.py --delay 8
kejian{NN}/runs/<ts>/*.answer.md
        ↓
guides/计组-课件{NN}-学习指南.md
```

| 阶段 | 产出 | 说明 |
|------|------|------|
| **discovery** | `kejian/runs/20260619-215358/` | 12/12 L0 结构 ✅ |
| **structure-map** | `kejian/structure-map.md` | Part 边界汇总 ✅ |
| **deep** | `manifests/kejian{NN}-deep.json` | 12 份 manifest ✅ |
| **整合** | `guides/计组-课件{NN}-学习指南.md` | 见索引 §五 |

---

## Deep Manifest 清单（12/12）

| 编号 | Manifest | 模块目录 | batches |
|------|----------|----------|---------|
| 01 | `manifests/kejian01-deep.json` | `kejian01/` | 6 |
| 02 | `manifests/kejian02-deep.json` | `kejian02/` | 6 |
| 03 | `manifests/kejian03-deep.json` | `kejian03/` | 5 |
| 04 | `manifests/kejian04-deep.json` | `kejian04/` | 5 |
| 05 | `manifests/kejian05-deep.json` | `kejian05/` | 5 |
| 5b | `manifests/kejian05b-deep.json` | `kejian05b/` | 6 |
| 06 | `manifests/kejian06-deep.json` | `kejian06/` | 6 |
| 7a | `manifests/kejian07a-deep.json` | `kejian07a/` | 4 |
| 7b | `manifests/kejian07b-deep.json` | `kejian07b/` | 4 |
| 08 | `manifests/kejian08-deep.json` | `kejian08/` | 5 |
| 09 | `manifests/kejian09-deep.json` | `kejian09/` | 5 |
| 10 | `manifests/kejian10-deep.json` | `kejian10/` | 6 |

**Notebook ID**：`e87c0462-b512-40df-8d6a-a0f5d4d30c81`

---

## 采集命令

在仓库根目录执行（采集前确认 NotebookLM 认证，见 auth-sop.md）：

```bash
NLM=python3 .cursor/skills/jizu-course-notebooklm/scripts/nlm-collect.py

# L0 结构发现（已完成）
python3 $NLM notebooklm-raw/manifests/kejian-discovery.json --delay 8

# 单章 deep
python3 $NLM notebooklm-raw/manifests/kejian07b-deep.json --delay 8

# 续跑失败 run
python3 $NLM notebooklm-raw/manifests/kejian01-deep.json \
  --resume notebooklm-raw/kejian01/runs/20260619-223616 --delay 8

# 仅补采单个 batch
python3 $NLM notebooklm-raw/manifests/kejian01-deep.json \
  --only kejian01-partA-intro \
  --resume notebooklm-raw/kejian01/runs/20260619-223616 --delay 8
```

### 建议采集顺序（全 12 章）

```
01 → 04 → 05 → 06 → 02 → 03 → 05b → 07b → 07a → 08 → 09 → 10
```

或使用批量脚本（跳过已有 `*-mistakes.answer.md` 的章）：

```bash
bash notebooklm-raw/kejian/run-all-deep.sh      # 首次全量（含续跑 05b/08）
bash notebooklm-raw/kejian/run-remaining-deep.sh  # 仅未完成的 9 章
```

> **注**：`nlm-collect` 不支持 meta-manifest 合并执行；以上 shell 脚本顺序调用 12 个 JSON。

---

## Deep 采集状态（2026-06-19）

| 章 | Run 路径 | 状态 |
|----|----------|------|
| 07b | `kejian07b/runs/20260619-221235/` | ✅ 4/4 |
| 05b | `kejian05b/runs/20260619-222348/` | ✅ 6/6 |
| 08 | `kejian08/runs/20260619-222348/` | ✅ 5/5 |
| 01 | `kejian01/runs/20260619-223616/` | ❌ 0/6（API unknown 超时，待 `--resume`） |
| 02–06, 07a, 09, 10 | — | 待采 |

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

## 目录结构

```
notebooklm-raw/kejian/
├── README.md                 ← 本文件
├── structure-map.md          ← discovery 汇总 ✅
├── run-all-deep.sh           ← 12 章顺序采集
├── run-remaining-deep.sh     ← 跳过已完成章
├── deep-collection.log       ← 采集日志
└── runs/
    └── 20260619-215358/      ← discovery（latest → 此目录）
```
