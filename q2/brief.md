# 第二问：把数据修成能训练（10 分钟）

## 背景

上一问产出 25 个窗口：18 个有分类标签，7 个没有；生成结果里还有空值、超长、答非所问。这一问要把它们**全部修成可训练样本**。

## 输入

面试官会给你 `windows.json`（上一问的输出，或标准版）。本目录提供：

| 文件 | 内容 |
|---|---|
| `generate.py` | `generate(window_id, attempt)` → 第 attempt 次生成结果，或 `None` |
| `generated.json` | 上面函数读取的预生成结果 |

生成结果含 `caption`、`answer`、`scene`、`is_quiet`、`review`、`confidence`——分类标签缺失时可以用它补。

## 交付

**1. `answer.md`** — 先答 3 道简答（3 分钟，每题 ≤3 行），题目见文件：

1. 除了长度和值域，还用什么信号判断生成质量？
2. 生成 caption / answer 的 prompt 怎么写？
3. 分类标签允许用模型补，风险是什么、怎么控制？

**2. `build_jsonl.py`**

```python
quality_issues(window, generated) -> list[str]   # 空列表 = 这次生成可用
build_jsonl(windows, generate) -> (records, rejected)
```

问题码：`generate_missing` / `review_pending` / `review_rejected` / `empty_caption` / `too_long` / `empty_answer` / `unexpected_answer` / `missing_scene` / `missing_is_quiet`。

训练样本：

```python
{"id": "V1001:0",
 "video": {"path": "...", "start_sec": 0, "end_sec": 180, "padded": False},
 "question": "...",
 "label": {"scene": ["办公室"], "is_quiet": 1, "caption": "...", "answer": "..."},
 "meta": {"model_version": "omni-0.3", "confidence": 0.9,
          "attempts": 1, "inferred_labels": False}}
```

运行 `python3 build_jsonl.py <windows.json>` 写出 `train.jsonl`。

## 规则

- 每个窗口最多生成 2 次；第 2 次仍不合格才放弃，并写进 `rejected`
- 分类标签缺失时用生成结果补；已有标签不覆盖
- 只收 `review=accepted`；`caption` 非空且 ≤200 字
- 有问题的窗口必须带 answer，没问题的窗口不能有 answer
- `meta` 要写清用了几次生成、标签是否模型补的

## 追问

生成通过率只有 78%，你怎么调这条链路？
