"""Priority scheduler starter."""

from schedulers.base import Scheduler, bank_ready_for_request


class PriorityScheduler(Scheduler):
    PRIORITY_LEVELS = [0, 1, 2]  # 0=high, 1=normal, 2=low

    def select(self, queue, banks, current_cycle):
        """Serve highest priority ready request first.

        Within a priority level, this starter applies row-hit preference.

        TODO(student):
        - define and justify priority assignment scheme
        - implement write urgency aging if needed
        - study fairness impact
        """
        for p in self.PRIORITY_LEVELS:
            candidates = [
                r for r in queue
                if r.priority == p and bank_ready_for_request(banks[r.bank_id], current_cycle)
            ]
            if not candidates:
                continue

            hits = [
                r for r in candidates
                if banks[r.bank_id].open_row is not None
                and banks[r.bank_id].open_row == r.row_id
            ]
            pool = hits if hits else candidates
            return min(pool, key=lambda r: r.arrival_cycle)

        return None
