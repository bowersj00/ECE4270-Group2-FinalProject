"""Refresh controller — Phase 4."""

from dram.bank import BankFSMState


class RefreshController:
    """Per-bank refresh sequencing with precharge-before-refresh."""

    def __init__(self, config):
        self.config = config
        # Track per-bank refresh countdown independently of BankState
        self._refresh_timers = {}      # bank_id -> cycles until next refresh due
        self._precharge_pending = {}   # bank_id -> True if waiting on tRAS before precharge

    def _get_timer(self, bank):
        """Lazily initialise per-bank timer."""
        if bank.bank_id not in self._refresh_timers:
            self._refresh_timers[bank.bank_id] = self.config.tREFI
        return self._refresh_timers[bank.bank_id]

    def tick_bank(self, bank, cycle: int):
        """
        Called once per cycle per bank, before the scheduler runs.

        Sequence:
          1. Decrement this bank's tREFI countdown.
          2. If countdown hits 0 and bank is not already refreshing:
               a. If a row is open → issue precharge (blocks for tRP).
               b. Once bank is idle → issue refresh (blocks for tRFC).
          3. Transition bank out of REFRESHING when tRFC window expires.
        """
        # Tick the bank's internal FSM (handles ACTIVATING → ACTIVE transitions)
        bank.tick(cycle)

        # Manage our own refresh timer (independent of bank.refresh_timer)
        bid = bank.bank_id
        if bid not in self._refresh_timers:
            self._refresh_timers[bid] = self.config.tREFI

        self._refresh_timers[bid] -= 1

        # --- Refresh due ---
        if self._refresh_timers[bid] <= 0:
            if bank.state == BankFSMState.REFRESHING:
                # Already refreshing from a previous overdue tick — reset and wait
                self._refresh_timers[bid] = self.config.tREFI
                print(f"[Cycle {cycle}] REFRESH bank {bid}")
                print(f"[Cycle {cycle}] PRECHARGE before REFRESH bank {bid}")
                return

            if bank.open_row is not None:
                # Row is open: must precharge first
                if bank.can_precharge(cycle):
                    bank.issue_precharge(cycle)
                    # After precharge completes (busy_until = cycle + tRP),
                    # we need to come back and issue the refresh.
                    # We keep the timer at 0 so we re-enter this branch next cycle.
                    self._precharge_pending[bid] = True
                else:
                    # tRAS not yet satisfied — stall one more cycle
                    pass
                return

            # No open row (or precharge just completed) → issue refresh
            if bank.state == BankFSMState.IDLE and cycle >= bank.busy_until:
                bank.state = BankFSMState.REFRESHING
                bank.busy_until = cycle + self.config.tRFC
                bank.open_row = None
                self._refresh_timers[bid] = self.config.tREFI
                self._precharge_pending.pop(bid, None)
