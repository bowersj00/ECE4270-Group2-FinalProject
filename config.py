"""Global configuration for the DRAM simulator starter."""

from dataclasses import dataclass


@dataclass
class DRAMConfig:
    # Architecture
    NUM_BANKS: int = 8
    ROW_BITS: int = 15
    CACHE_LINE_BITS: int = 6
    COL_BITS: int = 6

    # Queue / simulation
    QUEUE_DEPTH: int = 32
    MAX_CYCLES: int = 100_000
    WARMUP_CYCLES: int = 10_000

    # DDR4-like timing parameters, in memory cycles
    tRCD: int = 18
    tCL: int = 18
    tRP: int = 18
    tRAS: int = 43
    tRC: int = 61
    tREFI: int = 7800
    tRFC: int = 350
    BURST_LENGTH: int = 8

    # Priority thresholds
    WRITE_URGENCY_THRESHOLD: int = 200


DEFAULT_CONFIG = DRAMConfig()
