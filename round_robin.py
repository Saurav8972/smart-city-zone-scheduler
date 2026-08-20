from jobs import JOBS
from collections import deque


def run_round_robin(quantum):
    remaining = {}

    for job in JOBS:
        remaining[job["job_id"]] = job["burst_time"]

    ready = deque()
    time = 0
    next_job = 0

    first_start = {}
    finish_time = {}
    slices = []

    while len(finish_time) < len(JOBS):

        # Add jobs that have arrived
        while next_job < len(JOBS) and JOBS[next_job]["arrival_time"] <= time:
            ready.append(JOBS[next_job]["job_id"])
            next_job += 1

        # If no job is ready, move time to the next arrival
        if not ready:
            time = JOBS[next_job]["arrival_time"]
            continue

        job_id = ready.popleft()

        if job_id not in first_start:
            first_start[job_id] = time

        run_time = min(quantum, remaining[job_id])

        start = time
        time += run_time
        remaining[job_id] -= run_time

        slices.append((job_id, start, time))

        # New arrivals are added before the expired job
        while next_job < len(JOBS) and JOBS[next_job]["arrival_time"] <= time:
            ready.append(JOBS[next_job]["job_id"])
            next_job += 1

        # Put the unfinished job back into the queue
        if remaining[job_id] > 0:
            ready.append(job_id)
        else:
            finish_time[job_id] = time

    result = {}

    for job in JOBS:
        job_id = job["job_id"]

        turnaround = finish_time[job_id] - job["arrival_time"]
        waiting = turnaround - job["burst_time"]

        result[job_id] = {
            "start": first_start[job_id],
            "finish": finish_time[job_id],
            "waiting": waiting,
            "turnaround": turnaround
        }

    # Count a context switch when the running job changes
    switches = 0

    for i in range(1, len(slices)):
        if slices[i][0] != slices[i - 1][0]:
            switches += 1

    return result, switches, slices


def show_result(quantum, result, switches):
    print("\n" + "=" * 70)
    print("ROUND ROBIN - QUANTUM", quantum)
    print("=" * 70)

    print("Job ID     Arrival   Burst   Start   Finish   Waiting   Turnaround")

    total_wait = 0
    total_turnaround = 0

    for job in JOBS:
        job_id = job["job_id"]
        data = result[job_id]

        total_wait += data["waiting"]
        total_turnaround += data["turnaround"]

        print(
            f"{job_id:<10}"
            f"{job['arrival_time']:<10}"
            f"{job['burst_time']:<8}"
            f"{data['start']:<8}"
            f"{data['finish']:<9}"
            f"{data['waiting']:<10}"
            f"{data['turnaround']}"
        )

    print("-" * 70)
    print(f"Average waiting time    : {total_wait / len(JOBS):.2f}")
    print(f"Average turnaround time : {total_turnaround / len(JOBS):.2f}")
    print(f"Context switches        : {switches}")


if __name__ == "__main__":
    result3, switches3, slices3 = run_round_robin(3)
    result6, switches6, slices6 = run_round_robin(6)

    show_result(3, result3, switches3)
    show_result(6, result6, switches6)
