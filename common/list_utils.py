from typing import Iterable


def find(list_to_search: Iterable, fn):
    for x in list_to_search:
        if fn(x):
            return x
    else:
        return None


def count_times(list_to_search: Iterable, fn):
    return sum(1 for item in list_to_search if fn(item))
