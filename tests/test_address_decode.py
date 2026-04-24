from config import DEFAULT_CONFIG
from dram.request import decode_address


def test_decode_returns_valid_bank():
    bank, row, col = decode_address(0x1000, DEFAULT_CONFIG)
    assert 0 <= bank < DEFAULT_CONFIG.NUM_BANKS
    assert row >= 0
    assert col >= 0
