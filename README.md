# DRAM Controller & Memory Scheduling Simulator Starter

This starter project is for the Comp Arch DRAM Controller and Memory Scheduling Policy Evaluation project.

It intentionally provides:
- project structure
- runnable simulation skeleton
- request/queue/trace/config utilities
- partial scheduler and bank-model code
- TODO markers for students

It does **not** fully complete the simulator. Students must implement the timing-accurate FSM, refresh integration, scheduler details, metric validation, experiments, figures, and paper.

## Quick Start

```bash
pip install -r requirements.txt
python run_experiment.py --trace data/sample_trace.txt --policy fcfs
```

Run starter tests:

```bash
python -m pytest tests
```

Generate a sample trace:

```bash
python -m trace.generator --output data/generated_seq.txt --kind sequential --n 1000
```

## Main TODOs for Students

1. Complete DRAM bank finite-state machine.
2. Enforce timing constraints: tRCD, tCL, tRP, tRAS, tRFC.
3. Complete FCFS, FR-FCFS, and Priority scheduler logic.
4. Integrate refresh controller correctly.
5. Validate metrics.
6. Run sensitivity experiments.
7. Generate required figures.
8. Write the IEEE-style report.
