# 课件04采集审计：指令系统第二讲

> **审计日期**：2026-06-24  
> **对象**：`guides/计组-课件04-学习指南.md`、`notebooklm-raw/kejian/runs/latest/kejian04-structure.answer.md`、`notebooklm-raw/kejian/structure-map.md`、`notebooklm-raw/manifests/kejian04-deep.json`、`notebooklm-raw/kejian04/runs/latest/*.answer.md`  
> **结论**：课件04确实应按“两讲/两大部分”理解：第一讲是 **ISA 的设计**，第二讲是 **程序的机器级表示**。现有 deep 采集对第二讲拆分过粗，导致 MIPS ISA 例子、程序到机器指令/内存/寄存器的多层映射没有被充分采出；现有指南在 Part C 对该问题有少量整合，但主要受 raw 粒度限制。

---

## 1. 课件04应有结构（推定/来源）

| 层级 | 应有板块 | 证据 | 审计判断 |
|------|----------|------|----------|
| 第一讲 | 指令系统的设计 | discovery raw 明确列出“第一讲：指令系统的设计”，包括 ISA 设计原则、软硬件界面、设计目标、MIPS 特征与缺陷、RISC-V 子集和六种格式。 | 现有指南 Part A/B 覆盖较充分。 |
| 第二讲 | 程序的机器级表示 | discovery raw 明确列出“第二讲：程序的机器级表示”，包括指令格式类型、CISC/RISC、MIPS 指令格式/寄存器/操作数/寻址方式、目标文件链接、高级语言与机器语言转换。 | 现有 raw 和指南均偏薄，尤其缺“以 MIPS ISA 逐层讲程序如何落到机器级表示”。 |

辅助来源：

- `guides/计组课程-16周内容梳理.md` §1.2 确认课件 04 是 `4_指令系统.pdf`，主题为“RISC-V 指令集、寻址方式”。
- `notebooklm-raw/kejian/README.md` 确认本地 `4_指令系统.pdf` 对应 NotebookLM source `课件04-指令系统`。
- 仓库内未找到 PDF 原件，因此本审计以 discovery raw、structure-map、课程索引和 deep raw 为依据。

---

## 2. 现有分块与指南映射

| discovery / structure-map | deep manifest batch | deep raw 实际内容 | 指南映射 | 审计 |
|---------------------------|---------------------|------------------|----------|------|
| Part A：ISA 理论基础与设计哲学（Slide 1-7） | `kejian04-partA-isa` | ISA 定义、设计目标、CISC/RISC 权衡。 | Part A | 覆盖充分。 |
| Part B：RISC-V 指令集架构（Slide 9） | `kejian04-partB-riscv` | RV32I、ABI、六种格式、`addi` 机器码例。 | Part B | 覆盖较充分，且指南已补 Lab2-3 译码视角。 |
| Part C：指令风格与 MIPS 实例（Slide 8, 10-11） | `kejian04-partC-loadstore` | 仅约三段：Load/Store 特征、MIPS vs RISC-V 格式对照、链接/机器级表示要点。 | Part C | **采集明显过粗**：一个 batch 同时问 Load/Store、MIPS、链接和机器级表示，回答被压缩，没有展开 MIPS 例子。 |
| Part D：寻址方式与编码技术（Slide 6, 10-11） | `kejian04-partD-addressing` | 常见寻址、定长/扩展操作码、MIPS `lw` 和 `beq` 手算。 | Part D | 有 MIPS 寻址例，但定位是“寻址题”，没有补足第二讲的程序机器级表示主线。 |
| 易混概念 | `kejian04-mistakes` | 格式、ABI、寻址、CISC/RISC、ISA/ABI 对比。 | 易混概念、追问 | 可用，但不能替代第二讲深采。 |

---

## 3. 缺口清单

### 3.1 raw 缺口（主要问题）

| 缺口 | 表现 | 影响 |
|------|------|------|
| MIPS ISA 示例缺少逐层展开 | Part C 只说 MIPS 有 R/I/J 三类格式，没有展开寄存器编号、opcode/funct/rs/rt/rd/shamt/imm/address 字段如何承载程序语义。 | 学生无法从课件第二讲理解“程序如何变成机器指令”。 |
| 程序到机器级表示链条不完整 | raw 只概括“高级语言经编译、汇编生成二进制机器指令序列”，没有把 C 语句、汇编、机器码、指令内存、数据内存和寄存器状态连起来。 | 指南 Part C 只能画源程序到 `.o`/可执行的流程，缺少 ISA 层面的执行视角。 |
| MIPS 寻址/访存和内存布局未形成单独 batch | Part D 有 `lw`/`beq` 手算，但没有把 base+offset、寄存器堆、数据段/栈、指令地址统一到 MIPS 程序模型。 | 第二讲被拆散到 Part C/D，读者难以形成完整图景。 |
| RISC-V Lab 主线边界未被单独澄清 | manifest 频繁引入 Lab2-3 和 RISC-V，导致第二讲中的 MIPS 教学例子被 RISC-V 主线稀释。 | 容易把 MIPS 课件例题与 RISC-V Lab 位域/偏移口径混用。 |
| 常见题型不足 | deep raw 只有 `addi`、MIPS `lw`、MIPS `beq` 三个零散例子，没有 MIPS R/I/J 编码、数组访问、分支目标、链接/重定位类题型清单。 | 开卷复习缺可照抄模板。 |

### 3.2 整合缺口（次要问题）

| 缺口 | 表现 | 责任判断 |
|------|------|----------|
| Part C 篇幅过薄 | 指南 Part C 仅 C.1-C.3，主要是 Load/Store、MIPS/RISC-V 格式对照、链接装入流程。 | 有整合遗漏，但 raw 本身不足是主因。 |
| 第二讲标题没有显性保留 | 指南顶层结构按 A/B/C/D，不明显呈现“两讲：ISA 设计 / 程序的机器级表示”。 | 可在补采后调整 Part 结构或覆盖索引。 |
| MIPS 作为“程序机器级表示例子”的定位不够清楚 | 指南多次提醒 Lab 以 RISC-V 为主，但没有正面说明 MIPS 在课件04第二讲中的教学作用。 | 需要补采后回写边界说明。 |

---

## 4. 归因

本轮审计判断：**raw 分块不足为主，整合遗漏为辅**。

原因是 discovery raw 已经明确识别第二讲“程序的机器级表示”，但 `kejian04-deep.json` 没有按第二讲的内部层次继续拆 batch，而是把第二讲核心塞进：

- `kejian04-partC-loadstore`：Load/Store、MIPS 格式、链接、机器级表示混问；
- `kejian04-partD-addressing`：把 MIPS 例题归入寻址方式；
- `kejian04-mistakes`：只做概念对比。

因此 NotebookLM 输出自然偏摘要，指南 Part C/D 的压缩不是单纯写作遗漏，而是缺少足够 raw 素材支撑。

---

## 5. 建议补采方案

新增补采 manifest：

`notebooklm-raw/manifests/kejian04-supplement-machine-representation.json`

建议 5 个单问 batch：

| batch | 单问主题 | 目的 |
|-------|----------|------|
| `kejian04-supp-mips-isa-example` | MIPS ISA 如何作为程序机器级表示的教学例子 | 单独抽出 MIPS 在第二讲中的角色。 |
| `kejian04-supp-mips-fields` | MIPS 汇编到机器码字段映射 | 补 R/I/J 字段、寄存器编号、opcode/funct/imm/address。 |
| `kejian04-supp-program-memory-register` | 程序如何映射为指令序列、寄存器状态和内存访问 | 建立源程序→汇编→机器码→指令/数据内存→寄存器的链条。 |
| `kejian04-supp-mips-vs-riscv-boundary` | MIPS 课件例子与 RISC-V Lab 主线边界 | 防止 MIPS/RISC-V 位域、偏移、寄存器名混用。 |
| `kejian04-supp-question-types` | 第二讲常见题型/例题 | 产出开卷可用的题型模板。 |

执行建议：

```bash
NLM=.cursor/skills/jizu-course-notebooklm/scripts/nlm-collect.py
python $NLM notebooklm-raw/manifests/kejian04-supplement-machine-representation.json --dry-run
python $NLM notebooklm-raw/manifests/kejian04-supplement-machine-representation.json --delay 8
```

补采成功后，建议最小回写：

1. 在 `guides/计组-课件04-学习指南.md` 覆盖索引中显式加入“第二讲：程序的机器级表示”。
2. 扩展 Part C 为“程序的机器级表示与 MIPS 例子”，拆出 MIPS 字段、程序/内存/寄存器映射、链接装入与边界说明。
3. 在 Part D 保留寻址题，但明确 MIPS `beq/lw` 是第二讲例题的一部分，RISC-V Lab 是迁移口径。
