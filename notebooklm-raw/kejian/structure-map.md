# 计组课件结构图（structure-map）

> **来源**：Phase 0.5 discovery，`manifests/kejian-discovery.json`  
> **采集 run**：`notebooklm-raw/kejian/runs/20260619-215358`（12/12 batch 完成）  
> **说明**：下表按章汇总 NotebookLM 归并的 Part 边界；slide 范围为 raw 中的近似标注，深采前需对照 PDF 校对。

## 总览：各章 Part 边界

| 编号 | 课件 PDF | Part 划分（顺序） | 主要 slide 范围（raw） | 期末/实验备注 |
|------|----------|-------------------|------------------------|---------------|
| 01 | `1_计算机系统概述.pdf` | A 导论与系统思维 → B 冯·诺依曼与硬件基础 → C 层次结构与 ISA → D 编译与执行流 → E 性能评价 | A:1–9；B:9–12；C:13–14,16；D:14–15；E:17–20 | C、E 为期末核心 |
| 02 | `2_数据的机器级表示.pdf` | A 定点编码 → B IEEE754 → C 特殊值 → D AI 低精度格式 → E 非数值/端序/校验 | 讲1+讲2 分块 | B/C（IEEE754）绝对重点 |
| 03 | `3_运算方法和运算部件.pdf` | 1 ALU 架构 → 2 加减与标志位 → 3 乘除法 → 4 浮点运算与舍入 | 讲1–3 各段 | 与 Lab1 ALU/EX 相关 |
| 04 | `4_指令系统.pdf` | A ISA 设计哲学 → B RISC-V 格式 → C MIPS/Load-Store → D 寻址与编码 | A:1–7；B:9；C:8,10–11；D:6,10–11 | B/D 极重要（Lab2–3） |
| 05 | `5_中央处理器.pdf` | A 单周期通路 → B 单周期控制 → C 多周期 FSM → D 微程序与异常 | A:≈1–15；B:≈16–25；C:≈26–40；D:≈41+ | Lab1 数据通路基础 |
| 5b | `5_指令级并行.pdf` | A ILP 基础 → B 静态调度 → C Tomasulo/保留站 → D ROB/推测 → E 超标量多发射 | 板块 1–7,12 | **C/D 期末笔试必考** |
| 06 | `6_指令流水线.pdf` | A 基础与性能 → B 五级实现 → C 数据冒险 → D 控制冒险 → E 高级技术 | A:1–6；B:7–19；C:20–22；D:23；E:24–25 | B/C/D 对应 Lab1–3 |
| 7a | `7_互连网络.pdf` | 1 分类与参数 → 2 互连函数 → 3 静态/动态拓扑 | 板块 1–4 | 参数计算（直径、对剖带宽等）重点 |
| 7b | `7_层次结构存储系统.pdf` | 1 物理与主存接口 → 2 Cache/AMAT → 3 Sv39/SATP/TLB | 四板块顺序 | **Lab4–6 核心** |
| 08 | `8_线程级并行.pdf` | A 并行分类 → B Cache 一致性 MESI → C 连贯性/Fence → D 同步与原子 | 全课件顺序 | B/C 期末高频 |
| 09 | `9_MIPS32流水线处理器.pdf` | 1 五级结构 → 2 访存流 → 3 控制冒险/Flush → 4 分支预测等 | 课件09-36/37 | 与 RISC-V Lab1–3 对照 |
| 10 | `10_向量体系结构.pdf` | 1 DLP 背景 → 2 向量硬件 → 3 存储/Stride → 4 执行优化 → 5 GPU | 板块 1–5 | Week15–16 背景；Part1/4 较重要 |

## 各章 Part 明细

### 01 计算机系统概述

| Part | 主题 | Slide（raw） | 重要程度 |
|------|------|--------------|----------|
| A | 导论与系统思维 | 1–9 | 了解 |
| B | 硬件基础与冯·诺依曼 | 9–12 | 重要 |
| C | 系统层次结构与 ISA | 13–14, 16 | **期末核心** |
| D | 程序编译与执行流 | 14–15 | 重要 |
| E | 性能评价与量化 | 17–20 | **期末核心** |

### 02 数据的机器级表示

| Part | 主题 | 重要程度 |
|------|------|----------|
| A | 定点编码与 C 整数类型 | 基础 |
| B | IEEE 754 浮点体系 | **绝对重点** |
| C | 特殊值（±0、∞、NaN、非规格化） | **绝对重点** |
| D | BFLOAT16/FP8 等前沿格式 | 了解 |
| E | 字符、端序、对齐、校验 | 重要 |

### 03 运算方法和运算部件

| Part | 主题 | 重要程度 |
|------|------|----------|
| 1 | ALU 架构（1-bit/串行/并行） | 核心 |
| 2 | 补码加减、标志位 OF/SF/ZF/CF | 核心 |
| 3 | Booth 乘法、恢复余数除法 | 重要 |
| 4 | 浮点运算、舍入与规格化 | 重要 |

### 04 指令系统

| Part | 主题 | Slide（raw） | 重要程度 |
|------|------|--------------|----------|
| A | ISA 理论与设计目标 | 1–7 | 基础 |
| B | RISC-V 子集与六种格式 | 9 | **极重要** |
| C | Load/Store、MIPS 机器级表示 | 8, 10–11 | 基础 |
| D | 寻址方式与编码 | 6, 10–11 | **重要** |

### 05 中央处理器

| Part | 主题 | Slide（raw） | 重要程度 |
|------|------|--------------|----------|
| A | 单周期数据通路 | ≈1–15 | 基石 |
| B | 单周期控制器 | ≈16–25 | 基石 |
| C | 多周期与 FSM | ≈26–40 | 重要 |
| D | 微程序、异常/中断 | ≈41+ | Lab5/6 铺垫 |

### 5b 指令级并行

| Part | 主题 | 重要程度 |
|------|------|----------|
| A | ILP、相关性与冒险分类 | 基础 |
| B | 循环展开、静态调度 | 基础 |
| C | Tomasulo、保留站、CDB | **期末必考** |
| D | ROB、推测、精确异常 | **期末必考** |
| E | 超标量、多发射 | 重要 |

### 06 指令流水线

| Part | 主题 | Slide（raw） | 重要程度 |
|------|------|--------------|----------|
| A | 流水线概念与性能 | 1–6 | 基础 |
| B | 五级数据通路与控制 | 7–19 | **极高（Lab1–2）** |
| C | 数据冒险、转发、阻塞 | 20–22 | **极高（Lab1）** |
| D | 控制冒险、分支延迟 | 23 | 高（Lab3） |
| E | 超流水、多发射综述 | 24–25 | 中 |

### 7a 互连网络

| Part | 主题 | 重要程度 |
|------|------|----------|
| 1 | 分类、定时/交换/控制、特性参数 | **极重要（计算）** |
| 2 | Cube/Shuffle/Butterfly 等互连函数 | 重要 |
| 3 | 静态拓扑与 MIN/Omega/Crossbar | 重要 |

### 7b 层次结构存储系统

| Part | 主题 | 重要程度 |
|------|------|----------|
| 1 | 存储元、主存与 Load/Store 流程 | 基础 |
| 2 | Cache 映射、局部性、AMAT | **期末重点** |
| 3 | Sv39、PTE、SATP、TLB、页表遍历 | **期末核心（Lab4–6）** |

### 08 线程级并行

| Part | 主题 | 重要程度 |
|------|------|----------|
| A | Flynn、TLP、共享/非共享存储 | 基础 |
| B | MSI/MESI/MOESI、伪共享 | **核心** |
| C | 顺序一致性、弱模型、Fence | **核心** |
| D | 锁、原子指令、LR/SC | 重要 |

### 09 MIPS32 流水线处理器

| Part | 主题 | 对照 |
|------|------|------|
| 1 | 五级流水 IF–WB | RISC-V Lab1 |
| 2 | lw/sw 数据流 | Lab2 |
| 3 | 分支 Flush、控制冒险 | Lab3 |
| 4 | 分支预测等优化 | Bonus/进阶 |

### 10 向量体系结构

| Part | 主题 | 重要程度 |
|------|------|----------|
| 1 | DLP 动机、SISD vs SIMD | 高（复习） |
| 2 | 向量寄存器、Lane、功能部件 | 中 |
| 3 | 交叉存储、Stride、Gather-Scatter | 中 |
| 4 | Convoy/Chime、Strip-mining、Mask | 高 |
| 5 | GPU、SIMT | 中（背景） |

## 下一步（Phase 1 deep）

- 按上表 Part 边界编写 `manifests/kejian{NN}-deep.json`（P0 章优先：5b、7b、08）。
- 深采后在本文件追加「覆盖审计」列，并对照 `guides/计组-课件梳理索引.md` 更新 structure-map 列。

## Raw 索引

| Batch ID | Answer 文件 |
|----------|-------------|
| kejian01-structure | `runs/latest/kejian01-structure.answer.md` |
| kejian02-structure | `runs/latest/kejian02-structure.answer.md` |
| kejian03-structure | `runs/latest/kejian03-structure.answer.md` |
| kejian04-structure | `runs/latest/kejian04-structure.answer.md` |
| kejian05-structure | `runs/latest/kejian05-structure.answer.md` |
| kejian05b-structure | `runs/latest/kejian05b-structure.answer.md` |
| kejian06-structure | `runs/latest/kejian06-structure.answer.md` |
| kejian07a-structure | `runs/latest/kejian07a-structure.answer.md` |
| kejian07b-structure | `runs/latest/kejian07b-structure.answer.md` |
| kejian08-structure | `runs/latest/kejian08-structure.answer.md` |
| kejian09-structure | `runs/latest/kejian09-structure.answer.md` |
| kejian10-structure | `runs/latest/kejian10-structure.answer.md` |
