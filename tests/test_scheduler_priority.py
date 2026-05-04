from config import DEFAULT_CONFIG
from dram.bank import BankState
from dram.request import make_request
from schedulers.priority import PriorityScheduler


def test_read_priority_over_write():
    banks = [BankState(i, DEFAULT_CONFIG) for i in range(DEFAULT_CONFIG.NUM_BANKS)]
    read_req = make_request(20, 0x1000, "READ", 1, DEFAULT_CONFIG)
    write_req = make_request(10, 0x2000, "WRITE", 1, DEFAULT_CONFIG)
    selected = PriorityScheduler().select([write_req, read_req], banks, 20)

    assert selected == read_req
