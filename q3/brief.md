# 第三问：训练诊断（10 分钟）

## 背景

第二问把 25 个窗口全部修成可训练样本。模型是**单 decoder 直接生成整段 JSON**（scene / is_quiet / caption / answer），不是多头；loss 只在目标 token 上算 CE。

## 材料

| 文件 | 内容 |
|---|---|
| `material/loss_structure.md` | 输出 JSON 各字段的 token 数 |
| `figures/loss_curve.png` | 训练/验证 loss |
| `figures/field_loss.png` | 分类字段 vs 文本字段的 token loss |
| `figures/lr_gradnorm.png` | grad norm 与学习率 |
| `material/model_shortlist.csv` | 4 个候选模型的音视频支持、延迟、成本、LoRA |
| `material/benchmark_seed.csv` | 30 条评测种子，含 `source` 与 `duplicate_of` |

## 交付

`answer.md` 四题，每题 ≤5 行，题目见文件。第 4 题要求每张图给出「现象 → 两个假设 → 区分实验」，只说现象不算完成。
