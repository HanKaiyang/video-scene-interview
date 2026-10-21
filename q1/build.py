"""从切片和问题生成训练窗口。

视频只有路径、没有实体文件，时长用下面的 get_video_duration() 探测（真实环境里是 ffprobe）。
把 build_windows 补完；写好后 `python3 build.py` 会拿 example/ 的期望输出逐窗口对照。
"""
import csv
import json
import os

MOCK_DURATIONS = {
    "/data/video/V1001.mp4": 1200,
    "/data/video/V1002.mp4": 720,
    "/data/video/V1003.mp4": 900,
    "/data/video/V1004.mp4": 600,
    "/data/video/V1005.mp4": 480,
    "/data/video/V1006.mp4": 250,
    "/data/video/V9001.mp4": 420,
}


def get_video_duration(video_path):
    """返回视频时长（秒）；探测失败返回 None。"""
    return MOCK_DURATIONS.get(video_path)


def build_windows(video_rows, clip_rows, question_rows):
    """
    输入是 CSV 解析后的 list[dict]，空字符串表示缺失值。

    返回 list[dict]，每条是一个 3 分钟窗口：
        window_id   str      "{video_id}:{start_sec}"
        video_id    str
        input       dict     {"video": {"path", "start_sec", "end_sec"},
                              "text":  {"question": str | None, "ask_at_sec": int | None}}
        label       dict     {"scene": list[str] | None, "is_quiet": int | None}
        to_generate list[str]  还需要模型生成的字段
        usable      bool     标签是否够训练
    """
    raise NotImplementedError


def _load(folder, name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder, name + ".csv")
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [{k: ("" if v is None else v) for k, v in row.items()}
                for row in csv.DictReader(fh)]


def _check_example(rows):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "example", "expected.json"), encoding="utf-8") as fh:
        expected = json.load(fh)
    got = {r.get("window_id"): r for r in rows}
    bad = 0
    for want in expected:
        key = want["window_id"]
        have = got.get(key)
        if have is None:
            print("MISS  %s" % key)
            bad += 1
            continue
        diffs = []
        for path, want_value in (("input.video.start_sec", want["input"]["video"]["start_sec"]),
                                 ("input.text.question", want["input"]["text"]["question"]),
                                 ("label.is_quiet", want["label"]["is_quiet"])):
            node = have
            for part in path.split("."):
                node = (node or {}).get(part)
            if node != want_value:
                diffs.append(path)
        if sorted(have.get("label", {}).get("scene") or []) != sorted(want["label"]["scene"] or []):
            diffs.append("label.scene")
        if sorted(have.get("to_generate") or []) != sorted(want["to_generate"]):
            diffs.append("to_generate")
        print(("OK    " if not diffs else "DIFF  ") + key + ("" if not diffs else "  " + ",".join(diffs)))
        bad += 1 if diffs else 0
    print("windows=%d, mismatched=%d" % (len(rows), bad))
    return bad


if __name__ == "__main__":
    try:
        rows = build_windows(_load("example", "video_level"),
                             _load("example", "clip_level"),
                             _load("example", "question_level"))
    except NotImplementedError:
        print("build_windows 还没实现")
        raise SystemExit(2)
    bad = _check_example(rows)

    here = os.path.dirname(os.path.abspath(__file__))
    full = build_windows(_load("data", "video_level"), _load("data", "clip_level"),
                         _load("data", "question_level"))
    with open(os.path.join(here, "windows.json"), "w", encoding="utf-8") as fh:
        json.dump(full, fh, ensure_ascii=False, indent=2)
    print("windows.json: %d 个窗口，usable=%d" % (
        len(full), sum(1 for w in full if w.get("usable"))))
    raise SystemExit(1 if bad else 0)
