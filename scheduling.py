from jobs import JOBS


def show_result(name, result):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("Job ID     Arrival   Burst   Start   Finish   Waiting   Turnaround")

    total_wait = 0
    total_turn = 0

    for job in JOBS:
        job_id = job["job_id"]
        data = result[job_id]

        wait = data["waiting"]
        turn = data["turnaround"]

        total_wait += wait
        total_turn += turn

        print(
            f"{job_id:<10}"
            f"{job['arrival_time']:<10}"
            f"{job['burst_time']:<8}"
            f"{data['start']:<8}"
            f"{data['finish']:<9}"
            f"{wait:<10}"
            f"{turn}"
        )

    print("-" * 70)
    print(f"Average waiting time   : {total_wait / len(JOBS):.2f}")
    print(f"Average turnaround time : {total_turn / len(JOBS):.2f}")


def get_result(order):
    result = {}

    for job_id, start, finish in order:
        job = next(j for j in JOBS if j["job_id"] == job_id)

        turnaround = finish - job["arrival_time"]
        waiting = turnaround - job["burst_time"]

        result[job_id] = {
            "start": start,
            "finish": finish,
            "waiting": waiting,
            "turnaround": turnaround
        }

    return result


def fcfs():
    jobs = sorted(
        JOBS,
        key=lambda j: (j["arrival_time"], j["job_id"])
    )

    time = 0
    order = []

    for job in jobs:
        if time < job["arrival_time"]:
            time = job["arrival_time"]

        start = time
        time += job["burst_time"]

        order.append((job["job_id"], start, time))

    return get_result(order)


def sjf():
    left = JOBS.copy()
    time = 0
    order = []

    while left:
        ready = [
            job for job in left
            if job["arrival_time"] <= time
        ]

        if not ready:
            time = min(job["arrival_time"] for job in left)
            continue

        job = min(
            ready,
            key=lambda j: (
                j["burst_time"],
                j["arrival_time"],
                j["job_id"]
            )
        )

        start = time
        time += job["burst_time"]

        order.append((job["job_id"], start, time))
        left.remove(job)

    return get_result(order)


def srtf():
    remaining = {}

    for job in JOBS:
        remaining[job["job_id"]] = job["burst_time"]

    start_time = {}
    finish_time = {}

    time = 0

    while len(finish_time) < len(JOBS):

        ready = [
            job for job in JOBS
            if job["arrival_time"] <= time
            and remaining[job["job_id"]] > 0
        ]

        if not ready:
            time += 1
            continue

        job = min(
            ready,
            key=lambda j: (
                remaining[j["job_id"]],
                j["arrival_time"],
                j["job_id"]
            )
        )

        job_id = job["job_id"]

        if job_id not in start_time:
            start_time[job_id] = time

        remaining[job_id] -= 1
        time += 1

        if remaining[job_id] == 0:
            finish_time[job_id] = time

    result = {}

    for job in JOBS:
        job_id = job["job_id"]

        turnaround = finish_time[job_id] - job["arrival_time"]
        waiting = turnaround - job["burst_time"]

        result[job_id] = {
            "start": start_time[job_id],
            "finish": finish_time[job_id],
            "waiting": waiting,
            "turnaround": turnaround
        }

    return result


if __name__ == "__main__":
    show_result("FCFS", fcfs())
    show_result("Non-Preemptive SJF", sjf())
    show_result("SRTF", srtf())
