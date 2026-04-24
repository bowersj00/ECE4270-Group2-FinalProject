"""Timing helper functions.

TODO(student):
- Add reusable checks for tRCD, tCL, tRP, tRAS, tRFC.
- Consider representing commands explicitly.
"""

def row_hit(req, bank):
    return bank.open_row is not None and bank.open_row == req.row_id


def row_miss(req, bank):
    return bank.open_row is not None and bank.open_row != req.row_id


def row_empty(bank):
    return bank.open_row is None
