from itertools import chain


def flatten_chain(obj: list[list]):
    return list(chain.from_iterable(obj))