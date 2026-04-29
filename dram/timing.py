"""Timing helper functions.

TODO(student):
- Add reusable checks for tRCD, tCL, tRP, tRAS, tRFC.
- Consider representing commands explicitly.

tRCD: RAS-to-CAS delay — time from ACTIVATE to READ/WRITE
tCL: CAS latency — time from READ command to data
tRP: Row Precharge — time to close a row
tRAS: Active-to-Precharge delay (min row open time)
tRC: Row Cycle time = tRAS + tRP 61 cycles tRAS + tRP
tREFI: Average refresh interval
tRFC: Refresh cycle time
BL: Burst length — columns transferred per access
"""

def row_hit(req, bank):
    return bank.open_row is not None and bank.open_row == req.row_id


def row_miss(req, bank):
    return bank.open_row is not None and bank.open_row != req.row_id


def row_empty(bank):
    return bank.open_row is None
