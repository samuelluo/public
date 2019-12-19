"""
DONE
- Resolve power_set
- Build f3(), dynamic programming & memoization
- count iterations in f2 & f3
"""
import collections
import random
from typing import List


def build_power_set(s: List[int]) -> List[int]:
    power_set = [[]]
    for e in s:
        power_set_2 = [i + [e] for i in power_set]
        power_set = power_set + power_set_2
    return power_set


def f1(L1, L2):
    """
    If L1 can be reduced to L2, return True.

    N1 = number of elements in L1
    N2 = number of elements in L2
    N1 >> N2
    -> O(N2)
    """
    if len(L2) == 0:
        return True
    if len(L1) == 0:
        return False

    i1 = 0
    i2 = 0
    while i1 < len(L1) and i2 < len(L2):
        if L1[i1] == L2[i2]:
            i1 += 1
            i2 += 1
        else:
            i1 += 1

    return i2 == len(L2)


def test_f1():
    L2 = [1, 2, 3]
    test_cases = [
        ([2, 1, 4], L2, False),
        ([1, 2, 3, 4], L2, True),
        ([1, 2, 1, 3], L2, True),
    ]
    for L1, L2, expected in test_cases:
        output = f1(L1, L2)
        assert output == expected


def f2(L1, L2):
    """
    How many ways can we remove elements from L1, to match L2?
    N1 = number of elements in L1
    power_set = O(2^N1)
    for i in s: = O(N1)
    -> O(2^N1 * N2)

    Returns
    -------
    count : int
    """
    s = range(len(L1))
    power_set = build_power_set(s)
    count = 0
    print(f'f2 loops: {len(power_set)}')

    for s in power_set:
        L1_prime = []
        for i in s:
            L1_prime.append(L1[i])
        if L1_prime == L2:
            count += 1
    return count


def f3(L1, L2):
    """
    An element on `q` is a set of indexes to remove.

    N1 = number of elements in L1
    N2 = number of elements in L2
    N1 > N2
    Check tuples with a len of maximum of: N1-N2
    len(visited) = O(2^(N1-N2))
    validate: O(N2)
    -> O(2^(N1-N2) * N2)

    """
    count = 0
    q = set([frozenset()])    # List[frozenset[int]]
    solved = set()            # set[frozenset[int]]
    n_loops = 0

    while len(q) != 0:
        # Only process unsolved
        n_loops += 1
        s = q.pop()
        if s in solved:
            continue
        else:
            solved.add(s)

        # If L1_prime is equal, increment count; if invalid, prune branch
        L1_prime = []
        for i, val in enumerate(L1):
            if i not in s:
                L1_prime.append(val)
        if L1_prime == L2:
            count += 1
        elif not f1(L1_prime, L2):
            continue

        # If valid, explore children nodes
        for i in range(len(L1)):
            new_s = s | frozenset([i])
            if new_s not in q and new_s not in solved:
                q.add(new_s)

    print(f'f3 loops: {n_loops}')
    return count



def build_test_cases():
    L1 = [1, 2, 2, 3, 4, 5, 6]
    L2 = [1, 2, 3]
    test_cases = [
        (
            L1, L2,
            2,
        ),
        (
            [1, 1, 2, 2, 3, 3], L2,
            8,
        ),
        (
            [1, 2, 1, 2, 3, 2, 3], L2,
            8,
        ),
        (
            [1, 2, 4], L2,
            0
        ),
        (
            [3, 4, 8, 7, 6, 4, 7, 5, 1, 3, 8, 2, 4, 2, 1, 9, 3],
            L2,
            2
        ),
        (
            [random.randint(0, 10) for i in range(19)], L2,
            None,
        ),
    ]
    return test_cases


def main():
    test_f1()
    test_cases = build_test_cases()
    for L1, L2, expected in test_cases:
        output_2 = f2(L1, L2)
        output_3 = f3(L1, L2)

        print(L1, L2)
        print([
            'f2', output_2, expected,
            'f3', output_3, expected,
        ])
        print('')
        if expected is not None:
            assert output_2 == expected
            assert output_3 == expected


if __name__ == '__main__':
    main()
