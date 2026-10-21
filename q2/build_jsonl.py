"""把每个窗口修成可训练的 JSONL。"""
import json
import os
import sys

MAX_ATTEMPTS = 2


def quality_issues(window, generated):
    """
    判断一次生成结果能不能用。返回问题码列表，空列表 = 可用。
    问题码：generate_missing / review_pending / review_rejected /
            empty_caption / too_long / empty_answer / unexpected_answer /
            missing_scene / missing_is_quiet
    """
    raise NotImplementedError


def build_jsonl(windows, generate):
    """
    windows:  上一问产出的窗口
    generate: generate(window_id, attempt) -> dict 或 None，attempt 从 1 开始

    每个窗口最多试 MAX_ATTEMPTS 次；分类标签缺失时用生成结果补。
    返回 (records, rejected)；record 的 meta 里要有 attempts 与 inferred_labels。
    """
    raise NotImplementedError


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    windows_path = sys.argv[1] if len(sys.argv) > 1 else "windows.json"
    windows = json.load(open(windows_path, encoding="utf-8"))
    from generate import generate

    try:
        records, rejected = build_jsonl(windows, generate)
    except NotImplementedError:
        print("build_jsonl 还没实现")
        raise SystemExit(2)
    print("records=%d rejected=%d" % (len(records), len(rejected)))
    with open("train.jsonl", "w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
