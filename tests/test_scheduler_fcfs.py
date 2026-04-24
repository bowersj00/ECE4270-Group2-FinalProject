from config import DEFAULT_CONFIG
from dram.bank import BankState
from dram.request import make_request
from schedulers.fcfs import FCFSScheduler


def test_fcfs_selects_oldest_ready():
    banks = [BankState(i, DEFAULT_CONFIG) for i in range(DEFAULT_CONFIG.NUM_BANKS)]
    r1 = make_request(10, 0x1000, "READ", 1, DEFAULT_CONFIG)
    r2 = make_request(20, 0x2000, "READ", 1, DEFAULT_CONFIG)
    selected = FCFSScheduler().select([r2, r1], banks, 20)
    assert selected == r1
