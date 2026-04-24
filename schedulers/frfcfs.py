"""First-Ready First-Come First-Serve scheduler starter."""

from schedulers.base import Scheduler, bank_ready_for_request


class FRFCFSScheduler(Scheduler):
    def select(self, queue, banks, current_cycle):
        """Prioritize row-buffer hits, then FCFS.

        Starter implementation is intentionally simple.

        TODO(student):
        - make sure bank readiness is checked correctly
        - compare global FR-FCFS vs per-bank FR-FCFS behavior
        - validate starvation/tail-latency behavior
        """
        ready = [r for r in queue if bank_ready_for_request(banks[r.bank_id], current_cycle)]
        if not ready:
            return None

        hits = [
            r for r in ready
            if banks[r.bank_id].open_row is not None
            and banks[r.bank_id].open_row == r.row_id
        ]

        if hits:
            return min(hits, key=lambda r: r.arrival_cycle)

        return min(ready, key=lambda r: r.arrival_cycle)
