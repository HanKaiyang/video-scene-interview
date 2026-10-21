# 视频场景训练数据面试题

## 背景

我们要训一个多模态模型，输入是**一段 3 分钟视频 + 一句问题**，输出一段结构化 JSON：

```json
{"scene": ["图书馆", "户外"], "is_quiet": 1, "caption": "…", "answer": "…"}
```

- `scene`：视频里出现了哪些场景，取自 9 类，可多选——同一段画面里可能从图书馆走到室外
- `is_quiet`：这 3 分钟是否安静
- `caption`：这段画面的描述
- `answer`：针对这句问题的回答

难的不是模型，是**数据怎么来**。

原始数据只有三张表：视频表、切片表（每 60 秒一片，带分钟级标签）、问题表（带提问时刻）。标签存在缺失，视频长度不一定能被 180 秒整除，`caption`/`answer` 则根本没有现成值，需要模型生成、人工审核后回填。

这道题就是把这条链路走一遍：**从原始表构建训练样本 → 用模型和规则把数据修成可训练 → 再诊断训练中出现的问题。**

## 三问

| 题目 | 要解决的问题 | 产出 |
|---|---|---|
| **Q1** 构建训练窗口 | 怎么把连续视频切成固定的 3 分钟窗口，怎么把分钟级标签和问题对齐上去，缺值和补零怎么处理 | `q1/windows.json` |
| **Q2** 生成与修复数据 | 怎么用模型生成的内容和质量规则，把标签缺失、生成错误的窗口全部修成可训练样本 | `q2/train.jsonl` |
| **Q3** 训练诊断 | loss 为什么会被长文本字段主导、模型怎么选、benchmark 怎么建、三条训练曲线怎么归因 | `q3/answer.md` |

每问都是**先写 `answer.md` 里的简答题，再动代码**。三问合计约 30 分钟，按顺序做，前一问的产物是后一问的输入。

## 目录

```
q1/   brief.md  answer.md  build.py  data/  example/
q2/   brief.md  answer.md  build_jsonl.py  generate.py  generated.json
q3/   brief.md  answer.md  material/  figures/
```

## 运行

```bash
cd q1 && python3 build.py
cd q2 && python3 build_jsonl.py ../q1/windows.json
```

只需要 Python 3，不需要装任何第三方库，也不需要联网。
