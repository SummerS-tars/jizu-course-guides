# Manifests 索引

每个 JSON 对应 `parts.md` 中的一个 part。采集命令：

```bash
NLM=.cursor/skills/jizu-course-notebooklm/scripts/nlm-collect.py
python $NLM notebooklm-raw/manifests/<module>.json --delay 8
```

| module | 状态 | 指南产出 |
|--------|------|----------|
| `part1-week1-3` | ✅ raw 6/6（2026-06-16） | `guides/计组-Week1-3-学习指南.md` |
| `part2-week4-6` | ✅ raw 5/5 | `guides/计组-Week4-6-学习指南.md` |
| `part3-week7-9` | ✅ raw 6/6 | `guides/计组-Week7-9-学习指南.md` |
| `part4-week10-11` | ✅ raw 6/6 | `guides/计组-Week10-11-学习指南.md` |
| `part5-week12` | ✅ raw 5/5 | `guides/计组-Week12-学习指南.md` |
| `part6-week13-14` | ✅ raw 6/6 | `guides/计组-Week13-14-学习指南.md` |
| `part7-week15` | ✅ raw 5/5 | `guides/计组-Week15-学习指南.md` |

模板：`.cursor/skills/jizu-course-notebooklm/templates/manifest-template.json`
