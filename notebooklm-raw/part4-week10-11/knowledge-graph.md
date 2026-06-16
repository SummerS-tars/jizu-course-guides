# Part 4（Week 10–11）知识图谱

> **run**：`notebooklm-raw/part4-week10-11/runs/20260616-144926/`（6/6）
> **指南**：`guides/计组-Week10-11-学习指南.md`
> **生成**：2026-06-16

## 通读审计

| 项 | 结论 |
|----|------|
| batch | 6/6 完成 |
| 期末权重 | **极高** — 虚存/TLB/SATP 为笔试核心 |
| 素材质量 | Sv39 数值例、Lab4-5 对照表完整；L0 将 W11 部分写成「指令扩展」略偏，以 FiCS 记录为准（SATP/TLB 为主） |
| 必读 batch | `w10-sv39-page-table`、`w11-satp-tlb-sfence`、`lab45-crossref`、`w1011-mistakes-bridge` |

## 认知阶梯

```
L0 定位（存储层次转折、期末为何考） 
  → L1 虚存动机（存储墙、按需分页）
  → L2 Sv39 页表遍历 + PTE 位域
  → L2 SATP/TLB/SFENCE.VMA
  → L5 Lab4-5 对照
  → L3+L4 易混 + 衔接 Lab6/Week12
```

## 节点 → raw 映射

| 指南节 | raw batch |
|--------|-----------|
| §1 知识地图 | L0-positioning |
| §2.1 虚存 | w10-virtual-memory |
| §2.2 Sv39 | w10-sv39-page-table |
| §2.3 SATP/TLB | w11-satp-tlb-sfence |
| §3 Lab 对照 | lab45-crossref |
| §4 易错/衔接 | w1011-mistakes-bridge |

## 叙事承接

- **前接**：Week 9 ILP 挖掘见顶 → 转向数据/存储效率
- **后接**：Week 12 Cache 容量与速度；Lab6 页错误异常
