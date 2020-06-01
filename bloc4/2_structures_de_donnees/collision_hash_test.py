"""Minimal working example to check if Python dicts recheck equality on hash collision"""

from functools import wraps

# pylint: disable=no-member

def traced(func):
    """Un décorateur qui trace et compte les exécutions"""
    @wraps(func)
    def wrapped(*args):
        print(f'Calling {func.__name__}({[(id(x), x.val) for x in args] })')
        wrapped.invocations += 1
        return func(*args)
    wrapped.invocations = 0
    return wrapped

class Dummy:
    """A dummy class with a custom hash fct that collides"""
    def __init__(self, val):
        self.val = val

    @traced
    def __hash__(self):
        return 42

    @traced
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.val == other.val

if __name__ == '__main__':
    dummy_0 = Dummy(0)
    print(f"**** Dummmy(0)'s id = {id(dummy_0)} ****")
    dummy_1 = Dummy(1)
    print(f"**** Dummmy(1)'s id = {id(dummy_1)} ****")
    a_dict = {}

    print("**** Adds Dummmy(0) ****")
    a_dict[dummy_0] = "A"

    print(dummy_0 in a_dict)
    print(a_dict[dummy_0])
    print(dummy_1 in a_dict)

    print("**** Adds Dummmy(1) with same hash****")
    a_dict[dummy_1] = "B"

    print(dummy_0 in a_dict)
    print(a_dict[dummy_0])
    print(dummy_1 in a_dict)
    print(a_dict[dummy_1])

