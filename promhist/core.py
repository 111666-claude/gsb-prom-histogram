"""累计桶的合并与分位。"""

import bisect


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def _label(le):
    if le == int(le):
        return str(int(le))
    return repr(le)


class Histogram:
    def __init__(self):
        self._values = {}
        self._les = []
        self._cums = []

    def add(self, le, count, counter):
        counter.scanned += 1
        key = float(le)
        if key in self._values:
            count += self._values[key]
            self._values[key] = count
            self._cums[bisect.bisect_left(self._les, key)] = count
        else:
            self._values[key] = count
            idx = bisect.bisect_left(self._les, key)
            self._les.insert(idx, key)
            self._cums.insert(idx, count)

    def get(self, le, counter):
        counter.scanned += 1
        return self._values.get(float(le), 0.0)

    def count_buckets(self):
        return len(self._les)

    def order(self, counter):
        return [_label(le) for le in self._les]

    def total(self, counter):
        if not self._les:
            return 0.0
        counter.scanned += 1
        return float(self._values[self._les[-1]])

    def quantile(self, q, counter):
        les = self._les
        if not les:
            return None
        values = self._values
        counter.scanned += 1
        total = values[les[-1]]
        rank = q * total
        cums = self._cums
        idx = bisect.bisect_left(cums, rank)
        if idx >= len(les):
            return les[-1]
        counter.scanned += 1
        cum = cums[idx]
        le = les[idx]
        if idx == 0:
            prev_le = 0.0
            prev_cum = 0.0
        else:
            counter.scanned += 1
            prev_le = les[idx - 1]
            prev_cum = cums[idx - 1]
        if cum == prev_cum:
            return le
        frac = (rank - prev_cum) / (cum - prev_cum)
        return prev_le + frac * (le - prev_le)
