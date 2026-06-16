# notebooklm-raw 目录规范

> **Skill**：`.cursor/skills/jizu-course-notebooklm/SKILL.md`

## 目录结构

```
notebooklm-raw/
├── manifests/                    ← 采集任务定义（JSON）
│   ├── week1.json                ← 范例
│   └── ...
├── week1/                        ← 按周/模块组织
│   ├── runs/
│   │   └── <YYYYMMDD-HHMMSS>/   ← 每次采集运行
│   │       ├── run.meta.json     ← 运行元数据（notebook id、时间、batch 数）
│   │       ├── run.log           ← 终端输出日志
│   │       ├── <batch-id>.prompt.txt   ← 发给 NotebookLM 的 prompt
│   │       └── <batch-id>.answer.md    ← NotebookLM 的答复
│   ├── runs/latest → <ts>/       ← 符号链接，指向最近 completed run
│   ├── knowledge-graph.md        ← Phase 1.5 产物
│   └── 课程总结-week<N>-周<X>-计组H.md  ← 原始课堂笔记（参考用）
└── README.md
```

## Manifest 文件规范

```json
{
  "notebookId": "e87c0462-b512-40df-8d6a-a0f5d4d30c81",
  "module": "week1-2",
  "description": "计组 Week 1-2: 计算机系统概述 + 数据表示",
  "created": "2026-06-16",
  "batches": [
    {
      "id": "w1-overview",
      "layer": "L0",
      "priority": 1,
      "title": "计算机系统概述全景",
      "prompt": "…",
      "clear_conversation": true
    }
  ]
}
```

## Git 策略

| 路径 | 是否提交 | 原因 |
|------|----------|------|
| `manifests/*.json` | ✅ 提交 | 轻量、文本、可 review |
| `runs/<ts>/*.answer.md` | ✅ 提交 | 可读、可 diff |
| `runs/<ts>/*.prompt.txt` | ✅ 提交 | 可复现 |
| `runs/<ts>/run.log` | ✅ 提交 | 排查用 |
| `runs/<ts>/run.meta.json` | ✅ 提交 | 元数据 |
| `runs/latest` | ❌ 忽略 | 符号链接，自动生成 |
| `课程总结-*.md` | ✅ 提交 | 原始笔记参考 |

## 命名规范

### Module 命名
- 按周次：`week1`、`week2-3`（跨两到三周的模块）
- 按主题：`midterm-review`、`final-review`

### Batch ID 命名
- `w<N>-<topic>`：如 `w1-von-neumann`、`w3-booth`
- `supplement-<topic>`：追加追问
- `bridge-w<N>`：跨模块串联
