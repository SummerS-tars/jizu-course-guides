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

---

## 6. v2 拆小补采记录（2026-06-24）

原补采 run：

`notebooklm-raw/kejian04-supplement-machine-representation/runs/diagnostic-20260624-1553-first/`

其中前两个 batch 已成功，并已整合到 `guides/计组-课件04-学习指南.md` Part C：

| batch | 主题 | 结果 | 指南回写 |
|-------|------|------|----------|
| `kejian04-supp-mips-isa-example` | MIPS ISA 作为机器级表示例子 | 成功 | Part C.2 |
| `kejian04-supp-mips-fields` | MIPS R/I/J 字段与编码例 | 成功 | Part C.3/C.4 |
| `kejian04-supp-program-memory-register` | 程序、机器码、指令/数据内存、寄存器状态链路 | 失败：`unknown` | 未回写，改由 v2 拆小尝试 |

为避免原 `kejian04-supp-program-memory-register` 综合 prompt 过大导致 unknown 失败，已新增更细粒度 manifest：

`notebooklm-raw/manifests/kejian04-supplement-machine-representation-v2.json`

v2 将剩余问题拆为 4 个单问 batch：

| batch | 主题 | 结果 |
|-------|------|------|
| `kejian04-supp-program-to-instructions` | 程序/高级语言/汇编/机器码之间的一条链路 | **失败**：`unknown`，`--retries 1` 后仍为空错误 |
| `kejian04-supp-register-vs-memory` | MIPS 中寄存器、内存与 load/store 搬运 | 未运行：fail-fast 在第 1 个 batch 后停止 |
| `kejian04-supp-mips-vs-riscv-boundary` | MIPS 示例与 RISC-V/Lab 主线边界 | 未运行：fail-fast 在第 1 个 batch 后停止 |
| `kejian04-supp-question-types` | 第二讲常见考法/题型 | 未运行：fail-fast 在第 1 个 batch 后停止 |

执行记录：

```bash
python3 .cursor/skills/jizu-course-notebooklm/scripts/nlm-collect.py \
  notebooklm-raw/manifests/kejian04-supplement-machine-representation-v2.json \
  --dry-run --delay 10 --nlm-timeout 240 --retries 0 \
  --proxy http://127.0.0.1:7897

python3 .cursor/skills/jizu-course-notebooklm/scripts/nlm-collect.py \
  notebooklm-raw/manifests/kejian04-supplement-machine-representation-v2.json \
  --delay 10 --nlm-timeout 240 --retries 1 --fail-fast \
  --proxy http://127.0.0.1:7897
```

失败 run：

`notebooklm-raw/kejian04-supplement-machine-representation-v2/runs/20260624-161029/`

本次 v2 未产生任何成功 `*.answer.md`，因此只回写了原补采前两个成功 batch 能支撑的内容：MIPS 作为机器级表示教学例子、MIPS R/I/J 字段表与 `add $t0, $s1, $s2` 编码例。指南中以下内容仍应视为待补采：程序→汇编→机器码完整链路、寄存器 vs 内存状态、load/store 搬运、MIPS 与 RISC-V 迁移边界、常见题型。

### 6.1 failure report：脚本层 vs NotebookLM 层

本次排查没有发现 prompt 过长、source citation 解析或落盘逻辑能解释失败。`nlm-collect.py` 的日志路径显示：

1. `sync-auth.py` 在采集开始时返回“认证 OK”。
2. `notebooklm use e87c0462-b512-40df-8d6a-a0f5d4d30c81` 成功。
3. `notebooklm clear` 成功。
4. 失败发生在 `NotebookLMClient.chat.ask(notebook_id, prompt, conversation_id=None)` 调用内部；异常字符串为空，`classify_error("")` 被归类为 `unknown`。

随后做了最小低风险 NotebookLM 层诊断（未做 WSL 浏览器登录，未大规模重复请求）：

| 诊断 | 结果 | 判断 |
|------|------|------|
| `sync-auth.py --status` | Windows/WSL `storage_state.json` 均存在且 mtime 一致；曾显示 `auth: valid` | 文件同步本身存在，但不能证明 NotebookLM token fetch 稳定可用 |
| `notebooklm auth check --test --json` | `token_fetch: false`，`error: "Token fetch failed: "` | NotebookLM 认证 token/RPC 前置阶段异常，且错误信息为空 |
| `notebooklm -vv source list --json` | cookie 提取成功，停在 `Fetching CSRF and session tokens from NotebookLM` 后返回空 `ERROR` | source 列表尚未进入 source 解析层，失败更靠前 |
| `notebooklm -vv ask "请只回答：OK" --json` | 同样停在 token/session fetch 后返回空 `ERROR` | 与 prompt 内容、回答长度、citation 解析无关 |

综合判断：当前失败主要在 **NotebookLM token/session 获取或 NotebookLM 后端访问层**，不是 `nlm-collect.py` 的 batch 调度/落盘层，也不像是 v2 prompt 本身过大。由于 `sync-auth.py --status` 与 `notebooklm auth check --test --json` 的结果出现不一致，建议下一步按 SOP 由用户在 Windows 侧重新登录 NotebookLM，再在 WSL 执行：

```bash
cd ~/service/openclaw/workspace/skills/notebooklm-integration
python3 scripts/sync-auth.py --force
python3 scripts/sync-auth.py --check
notebooklm auth check --test --json
```

只有当 `token_fetch: true` 且极简 `notebooklm ask "请只回答：OK" --json` 成功后，再继续用 v2 manifest 从 `kejian04-supp-program-to-instructions` 起补采；否则继续重试 batch 只会消耗请求次数。
