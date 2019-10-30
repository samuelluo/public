import multiprocessing
import random


manager = multiprocessing.Manager()
key_queue = multiprocessing.Queue()
key_to_result = manager.dict()
procs = []


def f(indices, prices, l_r_chain):
    """
    Maximize the profit.
    profit = prices[sell_index] - prices[buy_index]
    max(profit)

    Parameters
    ----------
    indices : Tuple[int]
    prices : List[float]
    l_r_chain : tuple
        'L' or 'R', or None.

    Returns
    -------
    result : tuple
        low_index : int
        low : float
        high_index : int
        high : float
        buy_index : int
        sell_index : int
        max_gain : float
    """
    low_index = None
    low = None
    high_index = None
    high = None
    buy_index = 0
    sell_index = 0
    max_gain = 0
    if len(indices) == 0:    # TODO?
        return

    low_index = indices[0]
    low = prices[indices[0]]
    high_index = indices[0]
    high = prices[indices[0]]
    buy_index = indices[0]
    sell_index = indices[0]
    for index in indices:
        price = prices[index]
        if price < low:
            low_index = index
            low = price
        if price > high:
            high_index = index
            high = price
        gain = price - low
        if gain > max_gain:
            sell_index = index
            buy_index = low_index
            max_gain = gain

    key = (tuple(indices), tuple(l_r_chain))
    result = (low_index, low, high_index, high, buy_index, sell_index, max_gain)
    key_queue.put(key)
    key_to_result[key] = result


def combine():
    while not key_queue.empty():
        key = key_queue.get()
        if key not in key_to_result.keys():
            continue

        indices, l_r_chain = key
        result = key_to_result.pop(key)
        if len(l_r_chain) == 0:
            return result

        left_or_right = l_r_chain[-1]

        other_keys = key_to_result.keys()
        if left_or_right == 'L':
            other_keys = \
                [i for i in other_keys
                 if i[0][0] == indices[-1] + 1]
        elif left_or_right == 'R':
            other_keys = \
                [i for i in other_keys
                 if i[0][-1] == indices[0] - 1]

        if len(other_keys) == 1:
            other_key = other_keys[0]
            other_indices, other_l_r_chain = other_key
            other_result = key_to_result.pop(other_key)
            if left_or_right == 'L':
                indices = indices + other_indices
                result = _combine(result, other_result)
            elif left_or_right == 'R':
                indices = other_indices + indices
                result = _combine(other_result, result)

        key = (indices, l_r_chain[:-1])
        key_queue.put(key)
        key_to_result[key] = result


def _combine(result_1, result_2):
    """
    Parameters
    ----------
    result_1 : tuple
        This needs to be the left-side result.
    result_2 : tuple
        This needs to be the right-side result.

    Returns
    -------
    result : tuple
        low_index : int
        low : float
        high_index : int
        high : float
        buy_index : int
        sell_index : int
        max_gain : float
    """
    low_index_1, low_1, \
        high_index_1, high_1, \
        buy_index_1, sell_index_1, max_gain_1 = result_1
    low_index_2, low_2, \
        high_index_2, high_2, \
        buy_index_2, sell_index_2, max_gain_2 = result_2

    if low_1 < low_2:
        low_index = low_index_1
        low = low_1
    else:
        low_index = low_index_2
        low = low_2

    if high_1 > high_2:
        high_index = high_index_1
        high = high_1
    else:
        high_index = high_index_2
        high = high_2

    if max_gain_1 > max_gain_2:
        buy_index = buy_index_1
        sell_index = sell_index_1
        max_gain = max_gain_1
    else:
        buy_index = buy_index_2
        sell_index = sell_index_2
        max_gain = max_gain_2

    if (high_2 - low_1) > max_gain:
        buy_index = low_index_1
        sell_index = high_index_2
        max_gain = high_2 - low_1

    if max_gain == 0:
        buy_index = 0
        sell_index = 0

    result = (low_index, low, high_index, high, buy_index, sell_index, max_gain)
    return result


def _f2(indices, prices, l_r_chain=None):
    """
    Parameters
    ----------
    indices : List[int]
    prices : List[float]
    l_r_chain : str
        'L' or 'R', or None.

    Returns
    -------
    result : Tuple
        low_index, low, high_index, high, buy_index, sell_index, max_gain
    """
    if l_r_chain is None:
        l_r_chain = tuple()

    threshold = length//multiprocessing.cpu_count()
    if len(indices) > threshold:
        split_index = len(indices)//2
        indices_1 = indices[:split_index]
        indices_2 = indices[split_index:]
        _f2(indices_1, prices, l_r_chain + ('L',))
        _f2(indices_2, prices, l_r_chain + ('R',))
    else:
        proc = multiprocessing.Process(target=f, args=(indices, prices, l_r_chain))
        procs.append(proc)
        proc.start()


def f2(prices):
    length = len(prices)
    indices = list(range(length))

    _f2(indices, prices)
    for proc in procs:
        proc.join()

    result = combine()
    return result


def process_test_case(prices, expected):
    # print(prices)
    output = f2(prices)
    if (output != expected) and \
       (prices[output[1]] - prices[output[0]] != prices[expected[1]] - prices[expected[0]]):
        raise Exception("output `{}` != expected `{}`".format(output, expected))
    # print('\n')


if __name__ == '__main__':
    length = 10
    indices = range(length)
    prices = list(range(length))
    random.shuffle(prices)
    print(prices)
    f2(prices)
