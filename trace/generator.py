"""Synthetic trace generator.

Examples:
    python -m trace.generator --output data/generated_seq.txt --kind sequential --n 1000
    python -m trace.generator --output data/generated_random.txt --kind random --n 1000
    python -m trace.generator --output data/generated_zipf.txt --kind zipf --n 1000
"""

import argparse
import numpy as np


def write_trace(path, cycles, addresses, req_types=None, priorities=None, thread_ids=None):
    n = len(addresses)
    req_types = req_types if req_types is not None else ["R"] * n
    priorities = priorities if priorities is not None else [1] * n
    thread_ids = thread_ids if thread_ids is not None else [0] * n

    with open(path, "w") as f:
        for c, addr, rt, p, tid in zip(cycles, addresses, req_types, priorities, thread_ids):
            f.write(f"{int(c)} 0x{int(addr):x} {rt} {int(p)} {int(tid)}\n")


def sequential_trace(n, start=0x1000, stride=64):
    cycles = np.arange(n)
    addresses = start + np.arange(n) * stride
    return cycles, addresses


def random_trace(n, address_space=1 << 24, seed=0):
    rng = np.random.default_rng(seed)
    cycles = np.arange(n)
    addresses = rng.integers(0, address_space, size=n)
    addresses = (addresses // 64) * 64
    return cycles, addresses


def zipf_trace(n, n_rows=32768, s=0.8, n_banks=8, seed=0):
    rng = np.random.default_rng(seed)
    ranks = np.arange(1, n_rows + 1)
    weights = 1.0 / (ranks ** s)
    weights /= weights.sum()

    rows = rng.choice(n_rows, size=n, p=weights)
    banks = rng.integers(0, n_banks, size=n)
    cols = rng.integers(0, 64, size=n)

    bank_bits = int(np.log2(n_banks))
    addresses = (rows << (6 + bank_bits)) | (banks << 6) | cols
    addresses = (addresses // 64) * 64
    cycles = np.arange(n)
    return cycles, addresses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--kind", choices=["sequential", "random", "zipf"], default="sequential")
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    if args.kind == "sequential":
        cycles, addresses = sequential_trace(args.n)
    elif args.kind == "random":
        cycles, addresses = random_trace(args.n, seed=args.seed)
    else:
        cycles, addresses = zipf_trace(args.n, seed=args.seed)

    write_trace(args.output, cycles, addresses)
    print(f"Wrote {args.n} requests to {args.output}")


if __name__ == "__main__":
    main()
