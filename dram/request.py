"""Memory request representation and address decoding."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MemoryRequest:
    arrival_cycle: int
    address: int
    req_type: str
    priority: int
    bank_id: int
    row_id: int
    col_id: int
    thread_id: int = 0
    service_start: Optional[int] = None
    completion: Optional[int] = None

    @property
    def latency(self):
        if self.completion is None:
            return None
        return self.completion - self.arrival_cycle

    @property
    def wait_time(self):
        if self.service_start is None:
            return None
        return self.service_start - self.arrival_cycle


def decode_address(address: int, config):
    """Decode physical address into bank, row, column.

    Interleaved mapping:
        bank_id = (address >> CACHE_LINE_BITS) & (NUM_BANKS - 1)
        row_id = (address >> (CACHE_LINE_BITS + BANK_BITS)) & ((1 << ROW_BITS) - 1)

    TODO(student):
    - compare this mapping with row-interleaving as an optional extension.
    """
    bank_bits = config.NUM_BANKS.bit_length() - 1
    bank_id = (address >> config.CACHE_LINE_BITS) & (config.NUM_BANKS - 1)
    row_id = (address >> (config.CACHE_LINE_BITS + bank_bits)) & ((1 << config.ROW_BITS) - 1)
    col_id = address & ((1 << config.CACHE_LINE_BITS) - 1)
    return bank_id, row_id, col_id


def make_request(cycle: int, address: int, req_type: str, priority: int, config, thread_id: int = 0):
    bank_id, row_id, col_id = decode_address(address, config)
    return MemoryRequest(
        arrival_cycle=cycle,
        address=address,
        req_type=req_type,
        priority=priority,
        bank_id=bank_id,
        row_id=row_id,
        col_id=col_id,
        thread_id=thread_id,
    )
