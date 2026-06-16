# notebooklm-raw

NotebookLM 原始采集数据目录（与学习指南 `guides/` 分离）。

**完整说明**（目录结构、git 策略、采集命令、整合流程）：

`.cursor/skills/jizu-course-notebooklm/docs/raw-data.md`

**工作流入口**：`.cursor/skills/jizu-course-notebooklm/SKILL.md`

**NotebookLM 认证 SOP**：`~/service/openclaw/workspace/skills/notebooklm-integration/docs/auth-sop.md`

**Part 划分**：`parts.md`

## 模块命名规范

按 **part** 组织（见 `parts.md`）：`part1-week1-3`、`part4-week10-11` 等。

也支持单周：`week1`、`midterm-review`。

每个模块包含：
```
notebooklm-raw/<module>/
├── runs/
│   └── <timestamp>/         ← 采集运行记录
│       ├── run.meta.json
│       ├── run.log
│       ├── *.prompt.txt     ← 提问原文
│       └── *.answer.md      ← NotebookLM 回答
├── runs/latest → <timestamp>  ← 符号链接到最近完成 run
├── knowledge-graph.md       ← Phase 1.5 产物
├── topics-map.md            ← 知识点分布（可选）
└── 课程总结-week<N>-周<X>-计组H.md  ← 原始课堂笔记（参考用）
```

## Git 策略

- `manifests/` → 提交（JSON，轻量）
- `runs/` → 提交（.md / .txt，可读可 diff）
- `课程总结-week*.md` → 提交
- `knowledge-graph.md` → 提交
