import random
from pprint import pprint


def print_random_state():
    """
    Prints the current state of the random
    number generator to be able to reproduce it if needed
    """
    print("Random state:")
    state = random.getstate()
    pprint(state)
