# 第一问：构建训练窗口（10 分钟）

## 背景

三连问的第一问。你要把长视频切成 3 分钟训练窗口，产出的 `windows.json` 是第二问的输入。

## 输入

`data/` 下三个 CSV，空值即缺失。视频只有路径，时长用 `build.py` 里的 `get_video_duration(path)` 探测。

| 表 | 列 |
|---|---|
| `video_level` | `video_id`、`video_path`、`recorded_at` |
| `clip_level` | `clip_id`、`video_id`、`clip_seq`（第几分钟，从 1 开始）、`start_sec`、`end_sec`、`scene`、`is_quiet` |
| `question_level` | `question_id`、`video_id`、`ask_at_sec`、`question` |

`scene` 有 9 类：公共场合 / 交通 / 图书馆 / 餐厅 / 办公室 / 商场 / 户外 / 居家 / 其他。

## 交付

**1. `answer.md`** — 先答 4 道简答（3 分钟，每题 ≤3 行），题目见文件。

**2. `build.py`** — 实现

```python
build_windows(video_rows, clip_rows, question_rows) -> list[dict]
```

```python
{"window_id": "V1001:0", "video_id": "V1001",
 "input": {"video": {"path": "...", "start_sec": 0, "end_sec": 180, "padded": False},
           "text":  {"question": "...", "ask_at_sec": 22}},
 "label": {"scene": ["办公室"], "is_quiet": 1},
 "to_generate": ["caption", "answer"],
 "usable": True}
```

运行 `python3 build.py`：先对 `example/` 自检，再生成 `windows.json`。

## 口径

- 从 0 秒起每 180 秒一段，不重叠；最后一段不足 180 秒补零，`padded=true`
- 标签由窗口覆盖的切片合成；缺值不能当 0，凑不齐就是 `None`、`usable=false`
- `scene` 可多选、`is_quiet` 是单值，具体怎么合成由你定，写进 answer
- `caption`/`answer` 没有现成值，用 `to_generate` 标出还缺哪些

## 规则

- 可以用 agent，但要在 answer 里说明采纳与否决
- 不联网查答案
