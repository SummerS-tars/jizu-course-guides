# 计组 H — 本学期采集模块（Part）划分

> **用途**：Phase 1 采集时，每个 part 对应一个 `manifests/<module>.json` 与一个 `notebooklm-raw/<module>/` 目录。
> **准入**：2026-06-19 NotebookLM 来源已核对完备（含 Week 16；见 `guides/计组课程-16周内容梳理.md` §7）。
> **命名**：`partN-weekX-Y` 或简写 `weekX-Y`（与 AI H 仓库 `week1-2` 风格一致）。

---

## 划分原则

1. **知识连贯**：同一 part 内主题可互相引用，跨 part 用 L4 衔接 batch 显式串联。
2. **授课节奏**：计组每周 2~3 次课，part 按**周次块**而非单课切分。
3. **Lab 耦合**：Lab1–3 跟前半 CPU 块、Lab4–6 跟后半存储/异常块；manifest `sources_hint` 须列出对应 Wiki + report。
4. **期末权重**：Part 4–6 为期末重点，manifest 中 Lab 交叉引用 batch 优先级 `critical`。
5. **体量控制**：每 part 目标 4–8 个 batch（参照 AI H `week1-2.json`），单问单答。

---

## Part 总览

| # | module id | 周次 | 主题 | 期末权重 | Lab |
|---|-----------|------|------|----------|-----|
| 1 | `part1-week1-3` | W1–3 | 系统概述 + 数据通路 + ISA | 低 | Lab1–3 |
| 2 | `part2-week4-6` | W4–6 | 数据表示 + 多周期 CPU | 低 | — |
| 3 | `part3-week7-9` | W7–9 | 流水线 + ILP + 五一短周 | 低（期中界） | —；课件12-MIPS32 可选 |
| 4 | `part4-week10-11` | W10–11 | 虚拟存储 + SATP/TLB | **高** | Lab4–5 |
| 5 | `part5-week12` | W12 | 多核与 Cache 组织 | **高** | Lab6 |
| 6 | `part6-week13-14` | W13–14 | 缓存一致性 + 分布式 | **高** | — |
| 7 | `part7-week15` | W15 | I/O + 期末总复习（第一版） | 中 | Lab4–6 回顾 |
| 8 | `part8-week16` | W16 | 期末复习指导（Tomasulo/量化考点） | **高** | Lab4–6 + 开卷 |

**采集顺序建议**：Part 4 → 6 → 7 → **8** → 1 → 3 → 2 → 5（先期末重点，再补前半学期）。

---

## 各 Part 详情

### Part 1 — `part1-week1-3`

**核心问题**：为什么要做 CPU 项目？五级流水数据通路怎么搭？RISC-V ISA 设计哲学是什么？

| 维度 | 内容 |
|------|------|
| 周次 | Week 1（概述+xv6 项目）、Week 2（单周期通路）、Week 3（CISC/RISC） |
| 课件 | 课件01-计算机系统概述、课件04-指令系统、课件05-中央处理器 |
| 笔记 | 笔记-Week01；笔记-Week02-1/2；笔记-week03-* |
| Lab | Wiki-Lab1–3 + 报告-Lab1–3-朱文凯 |
| 指南产出 | `guides/计组-Week1-3-学习指南.md` |

**manifest 侧重点**：L0 项目定位；L2 数据通路/控制信号；L2 ISA 格式；L4 与 Week 4+ 回溯关系。

---

### Part 2 — `part2-week4-6`

**核心问题**：数据在机器里怎么表示？单周期为何不够，多周期如何复用硬件？

| 维度 | 内容 |
|------|------|
| 周次 | Week 4（整数表示）、Week 5（IEEE 754/FP16）、Week 6（多周期 FSM） |
| 课件 | 课件02-数据的机器级表示、课件03-运算方法和运算部件、课件05-中央处理器 |
| 笔记 | 笔记-week04-*、笔记-week05-*、笔记-week06-* |
| Lab | —（概念块，可与 Part 1 Lab 做 L4 回顾） |
| 指南产出 | `guides/计组-Week4-6-学习指南.md` |

**manifest 侧重点**：L2 补码/IEEE754 数值例；L2 多周期 CPI；L3 大小端/NaN/特殊值易混。

---

### Part 3 — `part3-week7-9`

**核心问题**：流水线如何加速？三类冒险怎么解？ILP 与动态调度入门。

| 维度 | 内容 |
|------|------|
| 周次 | Week 7（流水线）、Week 8（ILP/记分牌/Tomasulo）、Week 9（五一短周） |
| 课件 | 课件06-指令级并行、课件07-指令流水线 |
| 笔记 | 笔记-week07-*、笔记-week08-*、笔记-week09-*；**笔记-期中复习-计组H** |
| Lab | 报告-Lab1–3（转发/阻塞与课堂对照） |
| 指南产出 | `guides/计组-Week7-9-学习指南.md` |

**manifest 侧重点**：L2 冒险/转发/阻塞；L2 记分牌/Tomasulo；L0 期末「前半非重点」定位；可引用期中复习笔记。

---

### Part 4 — `part4-week10-11` ★期末

**核心问题**：虚拟地址如何映射到物理地址？SATP/TLB/SFENCE.VMA 如何协作？

| 维度 | 内容 |
|------|------|
| 周次 | Week 10（虚存/页表）、Week 11（SATP/ASID/SFENCE.VMA） |
| 课件 | 课件09-层次结构存储系统 |
| 笔记 | 笔记-week10-*、笔记-week11-* |
| Lab | Wiki-Lab4–5 + 报告-Lab4–5-朱文凯 |
| 指南产出 | `guides/计组-Week10-11-学习指南.md` |

**manifest 侧重点**：L2 Sv39 页表遍历；L2 SATP 位域；**L5 Lab↔课堂对照**（WARL、ECALL、MMU）；mermaid 地址转换图。

---

### Part 5 — `part5-week12` ★期末

**核心问题**：多核下 Cache 如何组织？写策略与映射方式？

| 维度 | 内容 |
|------|------|
| 周次 | Week 12（多核 + Cache） |
| 课件 | 课件09-层次结构存储系统、课件08-互连网络（补充） |
| 笔记 | 笔记-week12-* |
| Lab | Wiki-Lab6 + 报告-Lab6-朱文凯 |
| 指南产出 | `guides/计组-Week12-学习指南.md`（或并入 Part 6） |

**manifest 侧重点**：L2 Cache 映射/写策略；L5 Lab6 中断/异常与 Cache 访问；数值例（命中率/CPI）。

---

### Part 6 — `part6-week13-14` ★期末

**核心问题**：多核 Cache 不一致怎么办？目录法 vs 监听法？MESI？

| 维度 | 内容 |
|------|------|
| 周次 | Week 13（一致性协议）、Week 14（分布式/目录式/MESI） |
| 课件 | 课件10-线程级并行 |
| 笔记 | 笔记-week13-*、笔记-week14-* |
| Lab | — |
| 指南产出 | `guides/计组-Week13-14-学习指南.md` |

**manifest 侧重点**：L2 写更新 vs 写作废；L2 目录法/监听法对比；L3 MESI 状态易混；mermaid 一致性协议时序。

---

### Part 7 — `part7-week15`

**核心问题**：I/O 性能怎么衡量？期末考什么、怎么与 Lab 结合复习？

| 维度 | 内容 |
|------|------|
| 周次 | Week 15（磁盘/RAID + 期末复习） |
| 课件 | 课件11-向量体系结构（周一 I/O 相关）；全课件总复习 |
| 笔记 | 笔记-week15-* |
| Lab | 报告-Lab4–6 回顾 batch |
| 指南产出 | `guides/计组-Week15-学习指南.md` + 可选 `guides/计组-期末复习-学习指南.md` |

**manifest 侧重点**：L2 RAID/磁盘访问时间；L0 期末范围与策略；**L5 全学期 Lab↔考点对照表**。

---

## 与 manifest / raw 目录的对应

```
notebooklm-raw/
├── parts.md                          ← 本文件
├── manifests/
│   ├── part1-week1-3.json            ← 待编写
│   ├── part2-week4-6.json
│   ├── ...
│   └── part7-week15.json
├── part1-week1-3/
│   ├── runs/<ts>/
│   └── knowledge-graph.md
└── ...
```

## 下一步

1. ~~按采集顺序完成 7 个 part 的 manifest 采集~~ ✅ 2026-06-16（39 batch）
2. ~~各 part 初版学习指南~~ ✅ 2026-06-16（`guides/计组-Week*-学习指南.md`）
3. **Phase 4–5**：用户 Review 迭代 → 定稿（`checklist.md`）
