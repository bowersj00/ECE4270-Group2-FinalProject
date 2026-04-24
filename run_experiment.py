"""Top-level executable simulation skeleton.

Example:
    python run_experiment.py --trace data/sample_trace.txt --policy fcfs
"""

import argparse
from config import DEFAULT_CONFIG
from dram.bank import BankState
from dram.queue import BoundedQueue
from trace.reader import TraceReader
from schedulers.fcfs import FCFSScheduler
from schedulers.frfcfs import FRFCFSScheduler
from schedulers.priority import PriorityScheduler
from stats.collector import StatisticsCollector


def build_scheduler(name: str):
    name = name.lower()
    if name == "fcfs":
        return FCFSScheduler()
    if name == "frfcfs":
        return FRFCFSScheduler()
    if name == "priority":
        return PriorityScheduler()
    raise ValueError(f"Unknown scheduler policy: {name}")


def issue_request_skeleton(req, bank, cycle, config):
    """Starter service model.

    This is deliberately simplified so the project runs.
    Students must replace this with timing-accurate command sequencing.

    TODO(student):
    - model ACTIVATE, READ/WRITE, PRECHARGE as multi-cycle commands
    - enforce tRAS before precharge
    - set service_start when the first command is issued
    - set completion after data return
    """
    if req.service_start is None:
        req.service_start = cycle

    if bank.open_row is None:
        bank.stats["empties"] += 1
        bank.open_row = req.row_id
        latency = config.tRCD + config.tCL
    elif bank.open_row == req.row_id:
        bank.stats["hits"] += 1
        latency = config.tCL
    else:
        bank.stats["misses"] += 1
        bank.open_row = req.row_id
        latency = config.tRP + config.tRCD + config.tCL

    req.completion = cycle + latency
    bank.busy_until = req.completion
    bank.active_cycles += latency
    return req.completion


def run_simulation(trace_file, policy, config):
    banks = [BankState(bank_id=i, config=config) for i in range(config.NUM_BANKS)]
    queue = BoundedQueue(max_depth=config.QUEUE_DEPTH)
    reader = TraceReader(trace_file, config)
    scheduler = build_scheduler(policy)
    stats = StatisticsCollector(config)

    inflight = []

    for cycle in range(config.MAX_CYCLES):
        # 1. Retire completed requests
        still_inflight = []
        for req in inflight:
            if req.completion is not None and req.completion <= cycle:
                stats.record_completed(req)
            else:
                still_inflight.append(req)
        inflight = still_inflight

        # 2. Inject trace requests due this cycle
        for req in reader.requests_due(cycle):
            if not queue.enqueue(req):
                # Starter behavior: drop when full.
                # TODO(student): implement back-pressure/stall instead of drop.
                stats.dropped_requests += 1

        # 3. Tick banks / refresh skeleton
        for bank in banks:
            bank.tick(cycle)

        # 4. Select next request
        selected = scheduler.select(queue.items(), banks, cycle)
        if selected is not None:
            bank = banks[selected.bank_id]
            if bank.is_ready(cycle):
                queue.remove(selected)
                issue_request_skeleton(selected, bank, cycle, config)
                inflight.append(selected)

    final_stats = stats.finalize(banks=banks, total_cycles=config.MAX_CYCLES)
    return final_stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", default="data/sample_trace.txt")
    parser.add_argument("--policy", default="fcfs", choices=["fcfs", "frfcfs", "priority"])
    args = parser.parse_args()

    results = run_simulation(args.trace, args.policy, DEFAULT_CONFIG)
    print("\n=== DRAM Simulator Starter Results ===")
    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
