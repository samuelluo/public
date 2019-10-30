import itertools
from test_cases import test_cases


threshold = 2


def f(indices, prices):
    """
    Maximize the profit.
    profit = prices[sell_index] - prices[buy_index]
    max(profit)

    Parameters
    ----------
    indices : List[int]

    Returns
    -------
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
    if len(indices) == 0:
        result = (low_index, low, high_index, high, buy_index, sell_index, max_gain)
        return result

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

    result = (low_index, low, high_index, high, buy_index, sell_index, max_gain)
    return result


def combine(results_1, results_2):
    low_index_1, low_1, \
        high_index_1, high_1, \
        buy_index_1, sell_index_1, max_gain_1 = results_1
    low_index_2, low_2, \
        high_index_2, high_2, \
        buy_index_2, sell_index_2, max_gain_2 = results_2

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

    results = (low_index, low, high_index, high, buy_index, sell_index, max_gain)
    return results


def _f2(indices, prices):
    """
    Parameters
    ----------
    indices : List[int]
    prices : List[float]

    Returns
    -------
    results : Tuple[]
        low, low_index, max_gain, buy_index, sell_index
    """
    if len(indices) > threshold:
        split_index = len(indices)//2
        indices_1 = indices[:split_index]
        indices_2 = indices[split_index:]
        results_1 = _f2(indices_1, prices)
        results_2 = _f2(indices_2, prices)
        results = combine(results_1, results_2)

        print(
            list(
                zip(indices_1, [p for p in prices if p in indices_1])
            ),
            list(
                zip(indices_2, [p for p in prices if p in indices_2])
            ),
            sep="  "
        )
        # print(results_1, results_2)
        # print(results)
        print('\n')

        return results
    else:
        results = f(indices, prices)
        return results


def f2(prices):
    length = len(prices)
    indices = list(range(length))
    low_index, low, high_index, high, buy_index, sell_index, max_gain = _f2(indices, prices)
    return buy_index, sell_index


def process_test_case(prices, expected):
    # print(prices)
    output = f2(prices)
    if (output != expected) and \
       (prices[output[1]] - prices[output[0]] != prices[expected[1]] - prices[expected[0]]):
        raise Exception("output `{}` != expected `{}`".format(output, expected))
    # print('\n')


if __name__ == '__main__':
    for prices, max_gain, expected in test_cases:
        process_test_case(prices, expected)

    length = 5
    indices = range(length)
    prices_list = itertools.permutations(indices, length)
    for prices in prices_list:
        expected = f(indices, prices)
        low_index, low, high_index, high, buy_index, sell_index, max_gain = expected
        expected = (buy_index, sell_index)
        process_test_case(prices, expected)
