# Week 16 学习指南：期末复习指导（开卷）

> **课程**：计算机组成与体系结构（H）
> **覆盖周次**：Week 16（最后一周期末复习课）
> **主要来源**：Week 16 课程记录、复习 PPT、NotebookLM 分层问答
> **对应课件**：eLearning 复习 PPT、全学期课件回顾（`6_指令流水线`、`7_层次结构存储系统`、`8_线程级并行` 等）
> **教材章节**：唐朔飞《计算机组成原理》第 2 版 **第 5–8 章** 复习；Patterson RISC-V 版 **第 4–6 章**；参考《计算机体系结构：量化研究方法》
> **原始采集**：`notebooklm-raw/part8-week16/runs/20260619-171058/`（6 批）
> **知识图谱**：`notebooklm-raw/part8-week16/knowledge-graph.md`
> **课程记录**：`week16-周一-计组H.md`、`week16-周三-计组H.md`
> **整合日期**：2026-06-19（初版）
> **术语格式**：术语表及正文**首次出现**时，专业名词采用 **中文（English）**；英文缩写采用 **缩写（English full name，中文）**，便于对照英文课件、教材与开卷试题。

---

## 0. 术语表

| 术语 | 大白话 |
|------|--------|
| **TLB Reach (Translation Lookaside Buffer Reach)** | TLB 一次能「罩住」的虚拟地址范围 = 项数 × 页大小 |
| **保留站 RS (Reservation Station)** | Tomasulo 里暂存未执行指令的「工位」，带 Tag |
| **Qi** | 寄存器状态表：该寄存器的最新结果在哪个 RS 上 |
| **CDB (Common Data Bus)** | 公共数据总线，功能单元写回结果时广播 |
| **连贯性** | 不同地址的访存谁先谁后对多核可见 |
| **Fence** | 强制内存操作顺序的栅栏指令 |
| **周期挪用** | DMA（Direct Memory Access，直接内存访问）抢一个总线周期传一字再还给 CPU |

### 高频缩写速查

| 缩写 | 解释 |
|------|------|
| **ILP** | Instruction-Level Parallelism，指令级并行 |
| **RS** | Reservation Station，保留站 |
| **CDB** | Common Data Bus，公共数据总线 |
| **ROB** | Reorder Buffer，重排序缓冲区 |
| **TLB** | Translation Lookaside Buffer，地址转换后备缓冲 |
| **AMAT** | Average Memory Access Time，平均访存时间 |
| **MESI** | Modified-Exclusive-Shared-Invalid，四态缓存一致性协议 |
| **DMA** | Direct Memory Access，直接内存访问 |
| **NoC / PCIe** | Network-on-Chip / Peripheral Component Interconnect Express，片上网络 / 高速外设互连 |
| **RAID** | Redundant Array of Independent Disks，独立磁盘冗余阵列 |

---

## 1. 知识地图（L0）

### 1.1 这周在学什么？

Week 16 是**最后一周期末复习指导课**（06-15 周一内容完整，06-17 周三主要为考试/实验提醒）。老师明确：开卷考占 **30%**，复习重心在**体系结构**（实验已覆盖「组成」），勿只刷 Lab 不看书面概念。（来源：L0-w16-review-scope、week16-周一-计组H）

**学完你能**：

1. 对 `MUL.D`→`ADD.D` 同写 F0 填写 Qi 与 RS 的 Qj/Qk
2. 计算 64 项 DTLB、4KiB vs 2MiB 页的 TLB Reach 与扫 1GiB miss 次数
3. 用 AMAT 公式手算平均访存时间
4. 说明加锁后/解锁前 Fence 的原因及 MESI 四态含义
5. 写出单向环平均延迟直觉并对比 DMA 与中断 trade-off

### 1.2 五大复习板块

```mermaid
flowchart LR
    A[1. Tomasulo / ILP] --> B[2. Cache + 虚存]
    B --> C[3. 一致性 + 连贯性]
    C --> D[4. 互连网络]
    D --> E[5. 中断 + DMA]
```

| 板块 | 期末态度 | 详见 |
|------|----------|------|
| Tomasulo 动态调度 | **必考** | §2 |
| Cache / AMAT / 映射 | 计算题常客 | §3；Week 12 指南 |
| TLB Reach / 大页 | 量化对比 | §4；Week 10–11 指南 |
| MESI / Fence / 原子 | 概念 + 场景 | §5；Week 13–14 指南 |
| 互连参数 / 中断 / DMA | 易漏考点 | §6；Week 15 I/O 指南 |

### 1.3 推荐节奏（3–4 天）

每天围绕**一个板块串联**，刷往年随堂练习（≈ 真题难度），配合 Lab4–6 报告回顾特权/MMU/Trap。（来源：L0-w16-review-scope）

> **与 Week 15 指南关系**：Week 15 已收 I/O/磁盘/RAID 与全学期优先级；Week 16 深化 **Tomasulo、TLB Reach 计算、互连/DMA**，请两章对照使用。

### 1.4 课本与课件速查

| 指南节 | 对应周次 | 课件 | 唐朔飞（第 2 版） | P&H RISC-V |
|--------|----------|------|-------------------|------------|
| §2 Tomasulo | Week 8 | **5b** 指令级并行 | **第 5 章** ILP | **第 5 章** §5.1–5.3 |
| §3 Cache/AMAT | Week 12 | **07** 层次存储 | **第 7 章** §7.2 | **第 5 章** §5.1–5.3 |
| §4 TLB Reach | Week 10–11 | **07** | **第 7 章** §7.3.3 | **第 5 章** §5.7 |
| §5 MESI/Fence | Week 13–14 | **08** 线程级并行 | **第 8 章** §8.4 | **第 6 章** §6.4–6.5 |
| §6 互连/DMA | Week 15–16 | **7a** 互连、**10** I/O | **第 9 章** §9.1 | **第 5 章** §5.5 |

---

## 2. Tomasulo 算法（必考）

> **本节要回答**：保留站如何消除 WAR/WAW？时序表怎么填？

| 来源 | 位置 | 本节对应主题 |
|------|------|-------------|
| **课件 5b** | Tomasulo、CDB | 保留站、Qi |
| **唐朔飞** | **第 5 章** 动态调度 | RAW/WAR/WAW |
| **P&H RISC-V** | **第 5 章** §5.2–5.3 | Tomasulo 算法 |
| **课程记录** | `week16-周一-计组H.md` | 必考、时序表 |

### 2.1 三类相关

| 类型 | 能否消除 | Tomasulo 做法 |
|------|----------|---------------|
| **RAW** | 否（真依赖） | RS 中 Qj/Qk≠0 则等待源操作数 |
| **WAR** | 是（假相关） | 发射时把就绪操作数拷入 Vj/Vk，后续写不覆盖 RS 内旧值 |
| **WAW** | 是（假相关） | Qi 始终指向**最后发射**写该寄存器的 RS |

（来源：w16-tomasulo）

### 2.2 分析模板（MUL → ADD 同写 F0）

指令（乘法 6 周期，加法 2 周期）：
1. `MUL.D F0, F2, F4`
2. `ADD.D F0, F0, F6`

**发射后关键状态**（MUL 执行中、ADD 已发射）：

| 寄存器 Qi | F0 | F2 | F4 | F6 |
|-----------|-----|-----|-----|-----|
| 指向 | **Add1** | 0 | 0 | 0 |

| RS | Busy | Op | Qj | Qk |
|----|------|-----|-----|-----|
| Mult1 | Yes | MUL | 0 | 0 |
| Add1 | Yes | ADD | **Mult1** | 0 |

**要点**：F0 的 Qi 指向 Add1（后发射者），消除 WAW；Add1 的 Qj=Mult1 等待 RAW。（来源：w16-tomasulo）

### 2.3 考试时序表思路

1. **发射**：每周期最多发射一条（视 RS 空闲）
2. **执行**：Qj=Qk=0 且功能单元空闲才开始
3. **写回**：上 CDB 广播；**同一周期 CDB 通常只能服务一条** → 注意竞争

```mermaid
sequenceDiagram
    participant I as 发射
    participant E as 执行
    participant W as 写回 CDB
    I->>E: MUL 操作数就绪
    E->>W: MUL 完成
    W->>E: ADD 获得 MUL 结果
    E->>W: ADD 完成
```

> **直观理解**：不必纠结某一格信号是否与标准答案完全一致；展现「等操作数 → CDB 广播 → Qi 更新」逻辑即得分。

> **小结 → 下一节**：动态调度提高 ILP；**Cache/AMAT** 是另一类必算题型。

---

## 3. Cache 与 AMAT

> **本节要回答**：AMAT 怎么算？LFU 替换怎么模拟？

| 来源 | 位置 | 本节对应主题 |
|------|------|-------------|
| **课件 07** | AMAT、替换策略 | 映射与缺失 |
| **唐朔飞** | **第 7 章** §7.2 | Cache 性能 |
| **P&H RISC-V** | **第 5 章** §5.1–5.3 | AMAT |
| **课程记录** | `week16-周一-计组H.md` | LFU 序列练习 |

**公式**：$AMAT = HitTime + MissRate \times MissPenalty$

**数值例**：Hit 1ns，Miss penalty 100ns，Miss rate 2% → $AMAT = 1 + 0.02 \times 100 = 3ns$。（来源：w16-cache-amat）

| 映射 | 冲突缺失 | 比较器成本 | 命中时间 |
|------|----------|------------|----------|
| 直接映射 | 高 | 最低 | 最短 |
| 组相联 | 中 | 中 | 中 |
| 全相联 | 最低 | 最高 | 最长 |

**LFU + LRU 退化**：每块维护 `freq`，命中则 +1；替换时淘汰 freq 最小者；freq 并列则按 LRU 选牺牲块。（来源：w16-cache-amat、week16-周一-计组H 序列 A,B,C,…）

> **小结 → 下一节**：Cache 加速数据访问；**虚存/TLB** 解决地址翻译开销与大页 Reach。

---

## 4. 虚拟内存与 TLB Reach

> **本节要回答**：大页为何能少 TLB miss？代价是什么？

| 来源 | 位置 | 本节对应主题 |
|------|------|-------------|
| **课件 07** | TLB、大页 | Reach 计算 |
| **唐朔飞** | **第 7 章** §7.3.3 | TLB |
| **P&H RISC-V** | **第 5 章** §5.7 | 页大小与 TLB |
| **课程记录** | `week16-周一-计组H.md` | 1GiB 扫描例题 |

$$\text{TLB Reach} = \text{TLB 项数} \times \text{页面大小}$$

**64 项 DTLB**：
- 4KiB 页：Reach = 256KiB；扫 1GiB 数组 ≈ **262,144** 次 TLB miss
- 2MiB 大页：Reach = 128MiB；同场景 ≈ **512** 次 miss

**大页缺点**：内部碎片；OS 管理复杂；**不减少** 64B Cache 行访问次数。（来源：w16-vm-tlb）

> **小结 → 下一节**：多核下即使 TLB/Cache 都命中，仍须 **一致性 + 连贯性 + Fence** 保证正确同步。

---

## 5. 一致性、连贯性与 MESI

> **本节要回答**：一致性 vs 连贯性差在哪？锁为什么要 Fence？

| 来源 | 位置 | 本节对应主题 |
|------|------|-------------|
| **课件 08** | MESI、Fence、AMO | 多核同步 |
| **唐朔飞** | **第 8 章** §8.4 | MESI |
| **P&H RISC-V** | **第 6 章** §6.4–6.5 | 内存模型 |
| **课程记录** | `week16-周一-计组H.md` | 自旋锁 |

| 概念 | 解决什么 |
|------|----------|
| **一致性** | 同一地址多副本是否同一值 |
| **连贯性** | 不同地址操作的**全局可见顺序** |

**MESI**：

| 状态 | 含义 |
|------|------|
| M | 独占且已改，与主存不一致 |
| E | 独占且干净 |
| S | 多核共享且干净 |
| I | 无效 |

**自旋锁 + Fence**（宽松模型下访存可乱序）：
- **加锁后** Fence：临界区代码不能排到 Lock 之前
- **解锁前** Fence：临界区写必须在 Unlock 之前对其他核可见

**AMO / LR-SC**：硬件保证读-改-写不可分割。（来源：w16-coherence-fence）

> **小结 → 下一节**：互连拓扑与 **DMA/中断** 补全 I/O 链——易漏但可能考概念。

---

## 6. 互连网络、中断与 DMA

| 来源 | 位置 | 本节对应主题 |
|------|------|-------------|
| **课件 7a** | 环、Mesh 拓扑 | 延迟参数 |
| **课件 10**、**唐第 9 章** | DMA、中断 | I/O 路径 |
| **P&H** | **第 5 章** §5.5 | I/O |
| **课程记录** | `week16-周一-计组H.md` | 关-开-关-开 |

### 6.1 互连拓扑

| 拓扑 | 平均延迟直觉（n 节点） |
|------|------------------------|
| 单向环 | ≈ n/4 |
| 双向环 | ≈ n/8 |
| 2D 网格 | 曼哈顿距离：行向 + 列向平均路径之和 |

**参数**：节点度、直径、对剖带宽、平均延迟。（来源：w16-interconnect-dma）

### 6.2 中断「关-开-关-开」

1. 进入：硬件**关中断** → 保存现场  
2. 服务中（若嵌套）：保存完后可**开中断**  
3. 退出前：**关中断** → 恢复上下文  
4. 返回：**开中断**

```mermaid
flowchart LR
    A[硬件关中断] --> B[保存现场]
    B --> C[服务 ISR]
    C --> D{嵌套?}
    D -->|是| E[开中断继续]
    D -->|否| F[关中断]
    F --> G[恢复上下文]
    G --> H[开中断返回]
```

### 6.3 DMA

- **动机**：大批量 I/O 若每字节中断，CPU 开销爆炸  
- **流程**：CPU 初始化 → DMA 直传主存 → 完成时**中断**通知 CPU  
- **周期挪用**：DMA 与 CPU 争总线时抢 1 周期传 1 字

（来源：w16-interconnect-dma；与 `guides/计组-Week15-学习指南.md` §2 I/O 衔接）

---

## 7. 易混淆概念

| 对比组 | 正确理解 |
|--------|----------|
| 组成 vs 体系结构 | Lab 练通路/流水；期末偏 Cache/VM/多核/互连 |
| TLB miss vs Page Fault | 前者走页表；后者 OS 调入页 |
| 一致性 vs 连贯性 | 同地址 vs 访存顺序 |
| 大页 vs 大 Cache 行 | 大页减地址转换 miss；访存仍按 64B 行 |
| 中断 vs DMA | 中断逐事件响应；DMA 块传后一次中断 |
| Tomasulo Qi vs Qj/Qk | Qi 在寄存器表；Qj/Qk 在 RS 等操作数 |

---

## 8. 与全课程衔接

- **Week 7–8** 流水线/ILP 理论 → Week 16 **Tomasulo 手算**落地  
- **Week 10–12** 虚存/TLB/Cache → Week 16 **Reach/AMAT 量化**  
- **Week 13–14** MESI → Week 16 **Fence/原子**补连贯性  
- **Week 15** 磁盘/RAID → Week 16 **DMA/中断**补 I/O 链  
- **Lab4–6**：开卷时对照 report 中的 SATP、Trap、SFENCE.VMA

---

## 9. 自检问题

1. 写出 64 项 DTLB、4KiB vs 2MiB 页的 Reach，并估算扫 1GiB 的 miss 次数  
2. 对 `MUL.D F0,…` 后接 `ADD.D F0,…` 填写 Qi 与 Add1 的 Qj  
3. AMAT：Hit 2ns、Penalty 80ns、Miss 5% → AMAT=?  
4. 说明加锁后、解锁前各放一条 Fence 的原因  
5. 单向 n 节点环的平均延迟表达式？双向环如何变化？

---

## 10. 追问块

> **追问 1**：若同一周期 MUL 和 ADD 都完成，CDB 只能写回一条，时序表如何顺延？对 ADD 的 RAW 等待有何影响？
>
> **答**：两条结果**分两个周期**上 CDB（通常 MUL 优先或按 ROB 序）。ADD 若等 MUL 的 RAW，须多等 **1 个周期**才能捕获 MUL 结果并开始执行/写回。

> **追问 2**：2MiB 大页让 TLB miss 大降，为何数据库 OLTP 不一定适合全用大页？
>
> **答**：OLTP 工作集分散、分配粒度小，大页导致严重**内部碎片**与物理页浪费；且巨页分配/回收复杂，TLB 收益可能被内存压力抵消。

> **追问 3**：DMA 周期挪用频繁时，CPU 有效 CPI 如何恶化？与中断逐字节方案相比 trade-off 是什么？
>
> **答**：周期挪用使 CPU 频繁停顿等待总线 → **有效 CPI 上升**、吞吐下降。相对中断逐字节（CPU 参与每次传输），DMA 把 CPU 解放出来处理批量，总线争用是代价——适合大块连续 I/O。

---

## 11. 资料索引

| 类型 | 文件 / 路径 | 说明 |
|------|-------------|------|
| 课程记录 | `week16-周一/周三-计组H.md` | 期末复习指导 |
| 课件 | eLearning 复习 PPT；`3_课件/5b`、`07`、`08`、`7a`、`10` | 分板块对照 |
| 教材 | 唐朔飞第 2 版 **第 5–9 章** | Tomasulo 至 I/O |
| 教材 | Patterson RISC-V **第 4–6 章** | 处理器至多核 |
| 参考 | 《计算机体系结构：量化研究方法》 | 课堂提及 |
| 前序指南 | `guides/计组-Week15-学习指南.md` 等 | 全学期串联 |
| 实验 | `4_Lab/Lab{4..6}/`、`26-Arch/Doc/Lab*/` | 开卷对照 |
| 知识图谱 | `notebooklm-raw/part8-week16/knowledge-graph.md` | 整合前置 |
| 原始问答 | `notebooklm-raw/part8-week16/runs/latest/*.answer.md` | 6 批 raw |
| 周次索引 | `guides/计组课程-16周内容梳理.md` | 课纲对照 |

*本指南由 NotebookLM 分层问答（6 batch）+ Week 16 FiCS 记录整合。规则见 `.cursor/skills/jizu-course-notebooklm/SKILL.md`。*
