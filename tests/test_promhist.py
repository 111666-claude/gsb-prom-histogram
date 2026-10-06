import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from promhist import core


class PromhistTest(unittest.TestCase):
    def test_add_and_get(self):
        hist = core.Histogram()
        hist.add(1, 2, core.Counter())
        self.assertEqual(hist.get(1, core.Counter()), 2)

    def test_order_single(self):
        hist = core.Histogram()
        hist.add(1, 2, core.Counter())
        self.assertEqual(hist.order(core.Counter()), ["1"])

    def test_total_single(self):
        hist = core.Histogram()
        hist.add(1, 2, core.Counter())
        self.assertEqual(hist.total(core.Counter()), 2)

    def test_bucket_count_single(self):
        hist = core.Histogram()
        hist.add(1, 2, core.Counter())
        self.assertEqual(hist.count_buckets(), 1)

    def test_empty_quantile_none(self):
        self.assertIsNone(core.Histogram().quantile(0.5, core.Counter()))

    def test_counter_counts(self):
        counter = core.Counter()
        core.Histogram().add(1, 1, counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
