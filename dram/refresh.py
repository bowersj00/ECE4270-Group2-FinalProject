"""Refresh controller skeleton."""

class RefreshController:
    """Optional explicit refresh controller.

    Current starter uses BankState.tick() for refresh placeholder behavior.

    TODO(student):
    - move refresh logic here if preferred
    - ensure refresh has priority over normal scheduler requests
    - precharge open rows before refresh
    - block bank for tRFC cycles
    """

    def __init__(self, config):
        self.config = config

    def tick_bank(self, bank, cycle):
        bank.tick(cycle)
