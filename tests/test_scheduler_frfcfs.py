from config import DEFAULT_CONFIG
from dram.bank import BankState
from dram.request import make_request
from schedulers.frfcfs import FRFCFSScheduler


def test_frfcfs_selects_oldest_ready():
    banks = [BankState(i, DEFAULT_CONFIG) for i in range(DEFAULT_CONFIG.NUM_BANKS)]
    r1 = make_request(10, 0x1000, "READ", 1, DEFAULT_CONFIG)
    r2 = make_request(20, 0x2000, "READ", 1, DEFAULT_CONFIG)
    banks[0].open_row = r2.row_id  # make r2 a row hit
    selected = FRFCFSScheduler().select([r2, r1], banks, 20)
    
    assert selected == r1