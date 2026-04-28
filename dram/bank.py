"""DRAM bank model starter.

This file contains a simplified BankState placeholder.
Students must complete the cycle-accurate finite-state machine.
"""

from dataclasses import dataclass, field
from enum import Enum, auto


class BankFSMState(Enum):
    IDLE = auto()
    ACTIVATING = auto()
    ACTIVE = auto()
    PRECHARGING = auto()
    REFRESHING = auto()


# Class which tracks the current state of a given DRAM bank
# Each bank has a unique bank_id
# Timer keeps the number of cycles remaining in the current state
@dataclass
class BankState:
    bank_id: int
    config: object
    state: BankFSMState = BankFSMState.IDLE
    open_row: int | None = None
    timer: int = 0
    busy_until: int = 0
    last_activate_cycle: int | None = None
    refresh_timer: int = field(init=False)
    active_cycles: int = 0
    stats: dict = field(default_factory=lambda: {"hits": 0, "misses": 0, "empties": 0})

    # Post init, initialize the refresh timer
    def __post_init__(self):
        self.refresh_timer = self.config.tREFI

    # Function which returns True if the bank is not currently busy, and not refreshing
    def is_ready(self, cycle: int) -> bool:
        """Return True if bank can accept a new normal request."""
        return cycle >= self.busy_until and self.state != BankFSMState.REFRESHING

    # Function which implements timing constraints for each bank
    # self.timer tracks number of cycles left in current state
    # refreah_timer tracks when a refresh is necessary
    def tick(self, cycle: int):
        """Advance one cycle.

        Starter behavior only decrements refresh timer.

        TODO(student):
        - decrement current command timer
        - transition FSM state when timer reaches zero
        - force refresh when refresh_timer reaches zero
        - if open row exists before refresh, precharge first
        """

        # Decrement time remaining in current state
        self.timer -= 1

        # Check for transition from ACTIVATING to ACTIVE
        if self.timer <= 0 and self.state == BankFSMState.ACTIVATING:
            self.state = BankFSMState.ACTIVE

        # Decrement refresh timer
        self.refresh_timer -= 1

        # Check for refresh needed
        if self.refresh_timer <= 0:
            # Placeholder: mark refresh busy window.
            # Students should implement accurate refresh command behavior.
            self.state = BankFSMState.REFRESHING
            self.busy_until = max(self.busy_until, cycle + self.config.tRFC)
            self.refresh_timer = self.config.tREFI

        # If bank is refreshing, and no longer busy_until, the bank is done refreshing
        # and can return to the idle state
        if self.state == BankFSMState.REFRESHING and cycle >= self.busy_until:
            self.state = BankFSMState.IDLE
            self.open_row = None

    # Fuction which checks if bank is able to enter precharge, given the current cycle
    # This occurs when the last lactive cycle was tRAS cycles or more ago
    def can_precharge(self, cycle: int) -> bool:
        """Check tRAS before precharge."""
        if self.last_activate_cycle is None:
            return True
        return (cycle - self.last_activate_cycle) >= self.config.tRAS

    # The following methods are intentionally incomplete.

    # Function to enter the ACTIVATE state
    def issue_activate(self, row_id: int, cycle: int):
        """TODO(student): implement ACTIVATE command."""
        self.state = BankFSMState.ACTIVATING
        self.open_row = row_id
        self.last_activate_cycle = cycle
        self.timer = self.config.tRCD

    # Function to incur a READ/WRITE, for which the bank state must first be
    # ACTIVE with the requested address in the row buffer
    def issue_read_or_write(self, cycle: int):
        """TODO(student): implement READ/WRITE command and data return."""
        self.timer = self.config.tCL

    # Function to enter the precharge state
    # Must resprect the minimum row open time, tRAS
    def issue_precharge(self, cycle: int):
        """TODO(student): enforce tRAS and implement PRECHARGE."""
        if not self.can_precharge(cycle):
            raise RuntimeError("tRAS violation: cannot precharge yet")
        self.state = BankFSMState.PRECHARGING
        self.open_row = None
        self.timer = self.config.tRP
