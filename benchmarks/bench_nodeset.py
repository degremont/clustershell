"""Micro-benchmarks for :mod:`ClusterShell.NodeSet`."""

from ClusterShell.NodeSet import NodeSet, RESOLVER_NOGROUP


class NodeSetParsing:
    """Measure parsing and folding without external group resolution."""

    params = [1_000, 100_000]
    param_names = ["size"]
    repeat = 5
    sample_time = 0.05
    warmup_time = 0.1

    def setup(self, size):
        self.compact_pattern = "node[1-%d]" % size
        axis = max(10, int(size ** 0.5))
        self.multidimensional_pattern = "rack[1-%d]node[1-%d]" % (axis, axis)
        self.nodeset = NodeSet(self.compact_pattern,
                               resolver=RESOLVER_NOGROUP)

    def time_parse_compact(self, size):
        NodeSet(self.compact_pattern, resolver=RESOLVER_NOGROUP)

    def time_parse_multidimensional(self, size):
        NodeSet(self.multidimensional_pattern, resolver=RESOLVER_NOGROUP)

    def time_fold(self, size):
        str(self.nodeset)


class NodeSetOperations:
    """Measure common operations on large, overlapping node sets."""

    params = [1_000, 100_000]
    param_names = ["size"]
    repeat = 5
    sample_time = 0.05
    warmup_time = 0.1

    def setup(self, size):
        self.left = NodeSet("node[1-%d]" % size,
                            resolver=RESOLVER_NOGROUP)
        self.right = NodeSet("node[%d-%d]" %
                             (size // 2, size + size // 2),
                             resolver=RESOLVER_NOGROUP)

    def time_union_overlap(self, size):
        self.left.union(self.right)

    def time_intersection_overlap(self, size):
        self.left.intersection(self.right)

    def time_difference_overlap(self, size):
        self.left.difference(self.right)
