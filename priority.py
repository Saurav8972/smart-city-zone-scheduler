from jobs import JOBS


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


def priority_without_aging():
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

        # Smaller priority number means higher priority
        job = min(
            ready,
            key=lambda j: (
                j["priority"],
                j["arrival_time"],
                j["job_id"]
            )
        )

        start = time
        time += job["burst_time"]

        order.append((job["job_id"], start, time))
        left.remove(job)

    return get_result(order)


def priority_with_aging():
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

        best_job = None
        best_priority = None

        for job in ready:
            waited = time - job["arrival_time"]

            effective_priority = max(
                1,
                job["priority"] - (waited // 3)
            )

            if best_job is None:
                best_job = job
                best_priority = effective_priority
            elif effective_priority < best_priority:
                best_job = job
                best_priority = effective_priority
            elif effective_priority == best_priority:
                if job["arrival_time"] < best_job["arrival_time"]:
                    best_job = job
                elif (
                    job["arrival_time"] == best_job["arrival_time"]
                    and job["job_id"] < best_job["job_id"]
                ):
                    best_job = job

        start = time
        time += best_job["burst_time"]

        order.append(
            (best_job["job_id"], start, time)
        )

        left.remove(best_job)

    return get_result(order)


def show_result(title, result):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    print("Job ID     Priority   Waiting   Turnaround")

    total_wait = 0
    total_turnaround = 0

    for job in JOBS:
        job_id = job["job_id"]
        data = result[job_id]

        total_wait += data["waiting"]
        total_turnaround += data["turnaround"]

        print(
            f"{job_id:<10}"
            f"{job['priority']:<11}"
            f"{data['waiting']:<10}"
            f"{data['turnaround']}"
        )

    print("-" * 70)
    print(f"Average waiting time    : {total_wait / len(JOBS):.2f}")
    print(
        f"Average turnaround time : "
        f"{total_turnaround / len(JOBS):.2f}"
    )

    longest_job = max(
        result,
        key=lambda job_id: result[job_id]["waiting"]
    )

    print(f"Longest waiting job     : {longest_job}")


if __name__ == "__main__":
    normal = priority_without_aging()
    aging = priority_with_aging()

    show_result(
        "Priority Scheduling - Without Aging",
        normal
    )

    show_result(
        "Priority Scheduling - With Aging",
        aging
    )
