"""Experiment sweep skeleton.

TODO(student):
- Run all policies on all workloads.
- Sweep queue depth: 4, 8, 16, 32, 64.
- Sweep bank count: 2, 4, 8, 16.
- Sweep refresh interval: 50%, 75%, 100%, 125%, 150%.
- Sweep thread count: 1, 2, 4, 8.
- Save results as CSV for plotting.
"""

import csv
import os
import subprocess
import sys

count = 0
num_sweeps = 0

def run_experiment(policy, workload, queue_depth, bank_count, refresh_interval, thread_count):
    global count
    count += 1
    print(f"Running sweep {count} of {num_sweeps}: policy={policy}, workload={workload}, queue_depth={queue_depth}, bank_count={bank_count}, refresh_interval={refresh_interval}, thread_count={thread_count}")
    # Call run_experiment.py with the current combination of parameters and save results to CSV.
    subprocess_args = [
        sys.executable, "run_experiment.py",
        "--trace", f"data/{workload}",
        "--policy", policy,
        "--queue_depth", str(queue_depth),
        "--bank_count", str(bank_count),
        "--refresh_interval", str(refresh_interval),
        "--thread_count", str(thread_count)
    ]
    results = subprocess.run(subprocess_args, capture_output=True, text=True, check=True)
    # Parse results from stdout (assuming it's in the format "key: value\n")
    result_dict = {}
    for line in results.stdout.splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            result_dict[key.strip()] = value.strip()
    # Save result to CSV
    with open('sweep_results.csv', mode='a', newline='') as csv_file:
        fieldnames = ['policy', 'workload', 'queue_depth', 'bank_count', 'refresh_interval', 'thread_count'] + list(result_dict.keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if csv_file.tell() == 0:
            writer.writeheader()  # Write header only if file is new
        writer.writerow({
            'policy': policy,
            'workload': workload,
            'queue_depth': queue_depth,
            'bank_count': bank_count,
            'refresh_interval': refresh_interval,
            'thread_count': thread_count,
            **result_dict
        })


def main():
    # Sweep all combinations of policies, workloads, and parameters, run simulations, and save results to CSV.
    queue_depths = [4, 8, 16, 32, 64]
    bank_counts = [2, 4, 8, 16]
    refresh_intervals = [0.5, 0.75, 1.0, 1.25, 1.5]
    thread_counts = [1, 2, 4, 8]
    policies = ["fcfs", "frfcfs", "priority"]
    workloads = ["workload1_random.txt", "workload2_sequential.txt", "workload3_zipf.txt"]

    global num_sweeps
    num_sweeps = len(policies) + len(workloads) + len(queue_depths) + len(bank_counts) + len(refresh_intervals) + len(thread_counts)
    print(f"Running {num_sweeps} experiments...")

    for policy in policies:
        for workload in workloads:
            for queue_depth in queue_depths:
                run_experiment(policy, workload, queue_depth, bank_counts[2], refresh_intervals[2], thread_counts[0])
            for bank_count in bank_counts:
                run_experiment(policy, workload, queue_depths[3], bank_count, refresh_intervals[2], thread_counts[0])
            for refresh_interval in refresh_intervals:
                run_experiment(policy, workload, queue_depths[3], bank_counts[2], refresh_interval, thread_counts[0])
            for thread_count in thread_counts:
                run_experiment(policy, workload, queue_depths[3], bank_counts[2], refresh_intervals[2], thread_count)

if __name__ == "__main__":
    main()
