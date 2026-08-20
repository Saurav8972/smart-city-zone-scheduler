# Smart City Zone Scheduler

## Project Overview

This project implements a scheduling and safety engine for three smart-city
zones: Zone-A, Zone-B and Zone-C.

The same fixed set of eight sensor-processing jobs is used throughout Part 1.
The project covers CPU scheduling, synchronization, deadlock avoidance, and
memory address translation.

Part 2 uses this same Part 1 engine as the compute layer for the proposed
cloud and IoT deployment.

---

# Part 1 - Zone Job Scheduler and Deadlock-Safety Engine

## Files

- `jobs.py` - contains the fixed list of 8 jobs.
- `scheduling.py` - implements FCFS, non-preemptive SJF and SRTF.
- `round_robin.py` - implements Round Robin with quantum 3 and quantum 6.
- `priority.py` - implements priority scheduling with and without aging.
- `peterson.py` - demonstrates the race condition and Peterson's Algorithm.
- `bankers.py` - implements Banker's Algorithm and resource-request checking.
- `memory.py` - implements paging and segmentation address translation.

## Output Files

- `task2_scheduling_output.txt`
- `task3_round_robin_output.txt`
- `task4_priority_output.txt`
- `task5_peterson_output.txt`
- `task6_bankers_output.txt`
- `task7_memory_output.txt`

## How to Run

Python 3 is required.

Run the scheduling algorithms:

```bash
python scheduling.py
Run Round Robin:

```bash
python round_robin.py
```

Run priority scheduling:

```bash
python priority.py
```

Run Peterson's Algorithm:

```bash
python peterson.py
```

Run Banker's Algorithm:

```bash
python bankers.py
```

Run the paging and segmentation translator:

```bash
python memory.py
```

---

# Task 8 - Production Algorithm Choice
After comparing the measured results from Part 1, I would choose
**Round Robin with a quantum of 6** for the production zone-controller
workload.

## Why Round Robin?

For this fixed job list, Round Robin with quantum 3 gave an average
waiting time of **22.625** and **16 context switches**. With quantum 6,
the average waiting time was **20.375** and the number of context
switches reduced to **10**.

Therefore, between the two Round Robin configurations tested, quantum 6
gave better waiting-time performance and fewer context switches.

## Why not FCFS?

FCFS gave an average waiting time of **17.125**. Although this is lower
than the Round Robin result in this particular test, FCFS can make later
jobs wait behind a long job that arrived earlier. In this workload,
`Z2-J01` has a burst time of **9**, which can delay later jobs.

For continuously arriving sensor jobs, Round Robin gives ready jobs
repeated opportunities to run instead of following only arrival order.

## Why not SJF/SRTF?

Non-preemptive SJF gave an average waiting time of **13.000**, while
SRTF gave **11.500**. Both produced lower waiting times than Round Robin
for this fixed workload.

However, SRTF can interrupt a running job when a shorter job becomes
ready. SJF and SRTF also depend heavily on knowing job burst times in
advance.

For this project, predictable CPU sharing is more useful than selecting
only the shortest job.

## Why not Priority Scheduling?

Priority scheduling without aging gave an average waiting time of
**14.125**, and its longest-waiting job was `Z3-J02` with **33** units of
waiting.

With aging, the longest-waiting job changed to `Z2-J03`. This shows that
the scheduling order can change as jobs wait.

Round Robin does not depend on the fixed priority value of a job and
gives each ready job a regular turn.

## Final Decision

I would deploy **Round Robin with a quantum of 6** for these
zone-controller jobs.

My measured results were:

| Algorithm / Setting | Average Waiting Time | Context Switches |
|---|---:|---:|
| FCFS | 17.125 | — |
| SJF | 13.000 | — |
| SRTF | 11.500 | — |
| Round Robin, q=3 | 22.625 | 16 |
| Round Robin, q=6 | 20.375 | 10 |
| Priority without aging | 14.125 | — |

Although SRTF, SJF, FCFS and priority scheduling produced lower waiting
times on this fixed eight-job sample, I choose Round Robin q=6 because
it provides predictable time sharing for the continuously arriving
zone-controller workload and required only **10 context switches**,
compared with **16** for q=3.

---

# Part 2 - Cloud, Security and IoT Deployment Blueprint

The detailed deployment design for Tasks 9-14 will be provided in:

`docs/architecture_blueprint.md`

The blueprint will describe how the scheduler and safety engine from
Part 1 would operate as the cloud platform layer of the Smart City IoT
system.
