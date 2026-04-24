"""Statistics collector starter."""

from collections import Counter
from stats.metrics import mean, percentile, jains_fairness, row_buffer_hit_rate


class StatisticsCollector:
    def __init__(self, config):
        self.config = config
        self.completed = []
        self.dropped_requests = 0

    def record_completed(self, req):
        self.completed.append(req)

    def finalize(self, banks, total_cycles):
        latencies = [r.latency for r in self.completed if r.latency is not None]
        waits = [r.wait_time for r in self.completed if r.wait_time is not None]

        completed_count = len(self.completed)
        throughput = completed_count / total_cycles if total_cycles > 0 else 0.0

        per_thread = Counter()
        for r in self.completed:
            per_thread[r.thread_id] += 1

        fairness = jains_fairness(per_thread.values())
        util = {
            f"bank_{b.bank_id}": b.active_cycles / total_cycles
            for b in banks
        }

        return {
            "completed_requests": completed_count,
            "dropped_requests": self.dropped_requests,
            "avg_latency_cycles": round(mean(latencies), 4),
            "p95_latency_cycles": round(percentile(latencies, 95), 4),
            "avg_wait_cycles": round(mean(waits), 4),
            "throughput_req_per_cycle": round(throughput, 8),
            "throughput_req_per_kcycle": round(throughput * 1000, 4),
            "row_buffer_hit_rate": round(row_buffer_hit_rate(banks), 4),
            "jains_fairness": round(fairness, 4),
            "bank_utilization": util,
        }
