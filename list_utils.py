from typing import Iterable


def find(list_to_search: Iterable, fn):
    for x in list_to_search:
        if fn(x):
            return x
    else:
        return None
