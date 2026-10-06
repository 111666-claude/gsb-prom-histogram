"""累计桶的合并与分位。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Histogram:
    def __init__(self):
        self.buckets = {}

    def add(self, le, count, counter):
        counter.scanned += 1
        self.buckets[str(le)] = count

    def get(self, le, counter):
        counter.scanned += 1
        return self.buckets.get(str(le), 0.0)

    def count_buckets(self):
        return len(self.buckets)

    def order(self, counter):
        return sorted(self.buckets)

    def total(self, counter):
        total = 0.0
        for label in self.buckets:
            counter.scanned += 1
            total += self.buckets[label]
        return total

    def quantile(self, q, counter):
        order = sorted(self.buckets)
        if not order:
            return None
        rank = q * self.total(counter)
        prev_le = 0.0
        prev_cum = 0.0
        for label in order:
            counter.scanned += 1
            cum = self.buckets[label]
            if cum >= rank:
                le = float(label)
                if cum == prev_cum:
                    return le
                frac = (rank - prev_cum) / (cum - prev_cum)
                return prev_le + frac * (le - prev_le)
            prev_le = float(label)
            prev_cum = cum
        return prev_le
