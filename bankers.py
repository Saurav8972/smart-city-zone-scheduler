AVAILABLE = [3, 3, 2]

MAX_NEED = {
    "P0": [7, 5, 3],
    "P1": [3, 2, 2],
    "P2": [9, 0, 2],
    "P3": [2, 2, 2]
}

ALLOCATION = {
    "P0": [0, 1, 0],
    "P1": [2, 0, 0],
    "P2": [3, 0, 2],
    "P3": [2, 1, 1]
}


def calculate_need():
    need = {}

    for process in MAX_NEED:
        need[process] = []

        for i in range(3):
            value = MAX_NEED[process][i] - ALLOCATION[process][i]
            need[process].append(value)

    return need


def check_safe(available, allocation, need):
    work = available.copy()
    finished = set()
    sequence = []

    while len(finished) < len(allocation):
        found = False

        for process in allocation:
            if process in finished:
                continue

            possible = True

            for i in range(3):
                if need[process][i] > work[i]:
                    possible = False
                    break

            if possible:
                for i in range(3):
                    work[i] += allocation[process][i]

                finished.add(process)
                sequence.append(process)
                found = True

        if not found:
            return False, sequence

    return True, sequence


def check_request(process, request):
    need = calculate_need()

    print()
    print("Checking request from", process)
    print("Request:", request)

    for i in range(3):
        if request[i] > need[process][i]:
            print("Request denied: request is greater than the process Need.")
            return

    for i in range(3):
        if request[i] > AVAILABLE[i]:
            print("Request denied: resources are not currently Available.")
            return

    new_available = AVAILABLE.copy()
    new_allocation = {
        p: ALLOCATION[p].copy()
        for p in ALLOCATION
    }
    new_need = {
        p: need[p].copy()
        for p in need
    }

    for i in range(3):
        new_available[i] -= request[i]
        new_allocation[process][i] += request[i]
        new_need[process][i] -= request[i]

    safe, sequence = check_safe(
        new_available,
        new_allocation,
        new_need
    )

    if safe:
        print("Request GRANTED.")
        print("Resulting state is SAFE.")
        print("Safe sequence:", " -> ".join(sequence))
    else:
        print("Request DENIED.")
        print("Granting this request would leave the system in an UNSAFE state.")


if __name__ == "__main__":

    need = calculate_need()

    print("=" * 65)
    print("BANKER'S ALGORITHM")
    print("=" * 65)

    print()
    print("Available:", AVAILABLE)

    print()
    print("Need Matrix:")
    for process in need:
        print(process, ":", need[process])

    safe, sequence = check_safe(
        AVAILABLE,
        ALLOCATION,
        need
    )

    print()
    print("Initial state safe:", safe)

    if safe:
        print("One safe sequence:", " -> ".join(sequence))

    check_request("P1", [1, 0, 2])

    check_request("P0", [2, 0, 2])
