"""First-Come First-Serve scheduler starter."""

from schedulers.base import Scheduler, bank_ready_for_request


class FCFSScheduler(Scheduler):
    def select(self, queue, banks, current_cycle):
        """Select oldest request whose target bank is ready.

        This is mostly complete and can be used as a correctness baseline.
        Students should verify behavior with unit tests.
        """
        ordered = sorted(queue, key=lambda r: r.arrival_cycle)
        for req in ordered:
            bank = banks[req.bank_id]
            if bank_ready_for_request(bank, current_cycle):
                return req
        return None
