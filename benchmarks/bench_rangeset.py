"""Micro-benchmarks for :mod:`ClusterShell.RangeSet`."""

from ClusterShell.RangeSet import RangeSet


class RangeSetParsing:
    """Measure parsing and folding independently from input preparation."""

    params = [1_000, 100_000]
    param_names = ["size"]
    repeat = 5
    sample_time = 0.05
    warmup_time = 0.1

    def setup(self, size):
        self.compact_pattern = "1-%d" % size
        self.fragmented_pattern = ",".join(str(index)
                                           for index in range(1, size, 3))
        self.fragmented = RangeSet(self.fragmented_pattern, autostep=3)

    def time_parse_compact(self, size):
        RangeSet(self.compact_pattern)

    def time_parse_fragmented(self, size):
        RangeSet(self.fragmented_pattern)

    def time_fold_autostep(self, size):
        str(self.fragmented)


class RangeSetOperations:
    """Measure common set operations on partially overlapping ranges."""

    params = [1_000, 100_000]
    param_names = ["size"]
    repeat = 5
    sample_time = 0.05
    warmup_time = 0.1

    def setup(self, size):
        self.left = RangeSet("1-%d" % size)
        self.right = RangeSet("%d-%d" % (size // 2, size + size // 2))

    def time_union_overlap(self, size):
        self.left.union(self.right)

    def time_intersection_overlap(self, size):
        self.left.intersection(self.right)

    def time_difference_overlap(self, size):
        self.left.difference(self.right)
