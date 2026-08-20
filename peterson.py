import threading
import time


def unsafe_test():
    counter = 100

    def subtract():
        nonlocal counter

        old_value = counter
        time.sleep(0.001)
        counter = old_value - 40

    def add():
        nonlocal counter

        old_value = counter
        time.sleep(0.001)
        counter = old_value + 25

    t1 = threading.Thread(target=subtract)
    t2 = threading.Thread(target=add)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return counter


def peterson_test():
    counter = 100

    flag = [False, False]
    turn = 0

    def enter(i):
        nonlocal turn

        other = 1 - i

        flag[i] = True
        turn = other

        while flag[other] and turn == other:
            pass

    def leave(i):
        flag[i] = False

    def subtract():
        nonlocal counter

        enter(0)

        old_value = counter
        time.sleep(0.001)
        counter = old_value - 40

        leave(0)

    def add():
        nonlocal counter

        enter(1)

        old_value = counter
        time.sleep(0.001)
        counter = old_value + 25

        leave(1)

    t1 = threading.Thread(target=subtract)
    t2 = threading.Thread(target=add)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return counter


if __name__ == "__main__":

    print("=" * 60)
    print("WITHOUT SYNCHRONIZATION")
    print("=" * 60)

    for i in range(5):
        print(f"Run {i + 1}: {unsafe_test()}")

    print()
    print("=" * 60)
    print("WITH PETERSON'S ALGORITHM")
    print("=" * 60)

    for i in range(5):
        print(f"Run {i + 1}: {peterson_test()}")

    print()
    print("Expected correct result: 85")
