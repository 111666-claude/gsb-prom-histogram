"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "order":
        hist = core.Histogram()
        hist.add(5, 1, core.Counter())
        hist.add(10, 3, core.Counter())
        _line({"order": hist.order(core.Counter())})
        return 0
    if name == "merge":
        hist = core.Histogram()
        hist.add(1, 2, core.Counter())
        hist.add(1, 3, core.Counter())
        _line({"value": hist.get(1, core.Counter())})
        return 0
    if name == "normalize":
        hist = core.Histogram()
        hist.add(1, 2, core.Counter())
        hist.add("1.0", 3, core.Counter())
        _line({"buckets": hist.count_buckets()})
        return 0
    if name == "total":
        hist = core.Histogram()
        hist.add(1, 1, core.Counter())
        hist.add(2, 3, core.Counter())
        _line({"total": hist.total(core.Counter())})
        return 0
    if name == "work":
        hist = core.Histogram()
        for i in range(800):
            hist.add(i + 1, i + 1, core.Counter())
        counter = core.Counter()
        for i in range(800):
            hist.quantile((i + 1) / 800.0, counter)
        _line({"buckets": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
