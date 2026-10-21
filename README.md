# 面试材料说明

三个问按顺序做，前一问的产物是后一问的输入。

| 目录 | 内容 | 产出 |
|---|---|---|
| `q1/` | `brief.md`、`answer.md`、`build.py`、`data/`、`example/` | `windows.json` |
| `q2/` | `brief.md`、`answer.md`、`build_jsonl.py`、`generate.py`、`generated.json` | `train.jsonl` |
| `q3/` | `brief.md`、`answer.md`、`material/`、`figures/` | 无代码，只写 answer |

每问先写 `answer.md` 的简答题，再动代码。

运行方式：

```bash
cd q1 && python3 build.py          # 先对 example/ 自检，再生成 windows.json
cd q2 && python3 build_jsonl.py ../q1/windows.json
```
