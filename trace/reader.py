"""Trace reader.

Expected line format:
    <cycle> <hex_address> <R|W> <priority> [thread_id]

Example:
    0 0x1000 R 1 0
"""

from dram.request import make_request


class TraceReader:
    def __init__(self, trace_file, config):
        self.config = config
        self.requests = []
        self._load(trace_file)
        self._idx = 0

    def _load(self, trace_file):
        with open(trace_file, "r") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) < 4:
                    raise ValueError(f"Invalid trace line {line_no}: {line}")

                cycle = int(parts[0])
                address = int(parts[1], 16)
                req_type = "READ" if parts[2].upper().startswith("R") else "WRITE"
                priority = int(parts[3])
                thread_id = int(parts[4]) if len(parts) >= 5 else 0

                req = make_request(cycle, address, req_type, priority, self.config, thread_id)
                self.requests.append(req)

        self.requests.sort(key=lambda r: r.arrival_cycle)

    def requests_due(self, cycle):
        due = []
        while self._idx < len(self.requests) and self.requests[self._idx].arrival_cycle <= cycle:
            due.append(self.requests[self._idx])
            self._idx += 1
        return due
