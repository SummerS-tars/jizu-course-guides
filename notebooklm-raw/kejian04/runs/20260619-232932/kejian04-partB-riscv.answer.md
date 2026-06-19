根据**课件 04**、**Week3 笔记**及相关实验报告，RISC-V 指令集的核心架构与格式如下：

### 1. RV32I 子集与寄存器 ABI 约定

RV32I 是 RISC-V 的基础整数指令集，包含 32 个通用寄存器（x0–x31） [1, 2]。

*   **ABI 寄存器约定** [1, 3, 4]：
    *   **x0 (zero)**：硬编码为 0 [1, 5, 6]。
    *   **x1 (ra)**：返回地址，由**调用者保存** (Caller-saved) [1, 3, 7]。
    *   **x2 (sp)**：栈指针，由**被调用者保存** (Callee-saved) [1, 3, 7]。
    *   **x8 (s0/fp)**：保存寄存器/帧指针，由被调用者保存 [1, 6]。
    *   **x10–x11 (a0–a1)**：函数参数/返回值，由调用者保存 [1, 7]。
    *   **x5–x7, x28–x31 (t0–t6)**：临时寄存器，由调用者保存 [1, 3, 7]。

### 2. 六种基本指令格式 (R/I/S/B/U/J)

所有指令均为 **32 位定长**，寄存器索引位置（rs1, rs2, rd）固定以简化硬件译码 [1, 8]。

| 格式 | 31 | 30 | 25 | 24 | 21 | 20 | 19 | 15 | 14 | 12 | 11 | 8 | 7 | 6 | 0 | 典型指令 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **R** | \multicolumn{2}{c|}{funct7} | \multicolumn{3}{c|}{rs2} | \multicolumn{2}{c|}{rs1} | \multicolumn{2}{c|}{funct3} | \multicolumn{2}{c|}{rd} | \multicolumn{2}{c|}{opcode} | add, sub, slt [1, 8] |
| **I** | \multicolumn{5}{c|}{imm[11:0]} | \multicolumn{2}{c|}{rs1} | \multicolumn{2}{c|}{funct3} | \multicolumn{2}{c|}{rd} | \multicolumn{2}{c|}{opcode} | addi, lw, jalr [1, 8] |
| **S** | \multicolumn{2}{c|}{imm[11:5]} | \multicolumn{3}{c|}{rs2} | \multicolumn{2}{c|}{rs1} | \multicolumn{2}{c|}{funct3} | \multicolumn{2}{c|}{imm[4:0]} | \multicolumn{2}{c|}{opcode} | sw, sb, sh [1, 8] |
| **B** | imm[9] | imm[10:5] | \multicolumn{3}{c|}{rs2} | \multicolumn{2}{c|}{rs1} | \multicolumn{2}{c|}{funct3} | imm[4:1] | imm[10] | \multicolumn{2}{c|}{opcode} | beq, bne, blt [1, 8] |
| **U** | \multicolumn{10}{c|}{imm[31:12]} | \multicolumn{2}{c|}{rd} | \multicolumn{2}{c|}{opcode} | lui, auipc [1, 8] |
| **J** | imm[11] | \multicolumn{4}{c|}{imm[10:1]} | imm[10] | \multicolumn{4}{c|}{imm[19:12]} | \multicolumn{2}{c|}{rd} | \multicolumn{2}{c|}{opcode} | jal [1, 8] |

*注：B 型和 J 型的立即数需要乘以 2（左移 1位），因为指令地址是 16 位对齐的 [1, 7, 12]。*

### 3. 数值例：汇编与机器码转换

**任务：将 `addi x5, x5, 1` 翻译为 32 位机器码** [13]：

1.  **确定格式**：`addi` 属于 **I-type** [1, 8]。
2.  **查找编码** [1, 14, 15]：
    *   `opcode` = `0010011`
    *   `funct3` = `000`
    *   `rd` = `x5` (二进制 `00101`)
    *   `rs1` = `x5` (二进制 `00101`)
    *   `imm[11:0]` = `1` (12 位二进制 `000000000001`)
3.  **拼接二进制**：
    `000000000001` (imm) | `00101` (rs1) | `000` (funct3) | `00101` (rd) | `0010011` (opcode)
4.  **转换为十六进制**：`0x00128293` [13]。

关于 Lab 2–3 的指令完善，建议重点关注跳转地址计算和流水线冲刷（Flush）逻辑 [16, 17]。对于接下来的 Lab 4，你需要开始实现 CSR 特权指令，这部分清楚了吗？