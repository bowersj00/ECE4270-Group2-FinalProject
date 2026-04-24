"""Metric helper functions."""

import numpy as np


def mean(values):
    values = list(values)
    return float(np.mean(values)) if values else 0.0


def percentile(values, p):
    values = list(values)
    return float(np.percentile(values, p)) if values else 0.0


def jains_fairness(xs):
    """Jain's fairness index.

    J = (sum(x_i)^2) / (N * sum(x_i^2))
    """
    xs = np.array(list(xs), dtype=float)
    if len(xs) == 0 or np.sum(xs ** 2) == 0:
        return 0.0
    return float((np.sum(xs) ** 2) / (len(xs) * np.sum(xs ** 2)))


def row_buffer_hit_rate(banks):
    hits = sum(b.stats["hits"] for b in banks)
    misses = sum(b.stats["misses"] for b in banks)
    empties = sum(b.stats["empties"] for b in banks)
    total = hits + misses + empties
    return hits / total if total else 0.0
