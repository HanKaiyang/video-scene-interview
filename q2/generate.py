"""模型生成函数（模拟）：generate(window_id, attempt) 返回第 attempt 次生成结果。

真实环境里每次 attempt 都是一次模型调用；这里用 generated.json 里的预生成结果代替。
返回 None 表示这次生成失败。
"""
import copy
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_HERE, "generated.json"), encoding="utf-8") as _fh:
    _RESULTS = json.load(_fh)


def generate(window_id, attempt=1):
    attempts = _RESULTS.get(window_id) or []
    if attempt < 1 or attempt > len(attempts):
        return None
    return copy.deepcopy(attempts[attempt - 1])
