"""累计桶的合并与分位。"""

from bisect import bisect_left


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def _label(le):
    if le == int(le):
        return str(int(le))
    return str(le)


class Histogram:
    def __init__(self):
        self.buckets = {}
        self._sorted = None

    def _keys(self, counter):
        if self._sorted is None:
            self._sorted = sorted(self.buckets)
            counter.scanned += len(self._sorted)
        return self._sorted

    def add(self, le, count, counter):
        counter.scanned += 1
        key = float(le)
        if key in self.buckets:
            self.buckets[key] += count
        else:
            self.buckets[key] = count
        self._sorted = None

    def get(self, le, counter):
        counter.scanned += 1
        return self.buckets.get(float(le), 0.0)

    def count_buckets(self):
        return len(self.buckets)

    def order(self, counter):
        return [_label(le) for le in self._keys(counter)]

    def total(self, counter):
        counter.scanned += 1
        keys = self._keys(counter)
        if not keys:
            return 0.0
        return float(self.buckets[keys[-1]])

    def quantile(self, q, counter):
        keys = self._keys(counter)
        if not keys:
            return None
        rank = q * self.total(counter)
        cums = [self.buckets[le] for le in keys]
        counter.scanned += 1
        idx = bisect_left(cums, rank)
        if idx >= len(keys):
            return keys[-1]
        le = keys[idx]
        cum = cums[idx]
        prev_le = keys[idx - 1] if idx > 0 else 0.0
        prev_cum = cums[idx - 1] if idx > 0 else 0.0
        if cum == prev_cum:
            return le
        frac = (rank - prev_cum) / (cum - prev_cum)
        return prev_le + frac * (le - prev_le)
