import types

# Einfaches Stub-Modul für NumPy

float32 = float


class DummyArray(list):
    def transpose(self, *args):
        return self

    def __truediv__(self, other):
        return self

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            x = self
            for i in idx:
                x = x[i]
            return x
        return list.__getitem__(self, idx)


def asarray(obj, dtype=None):
    if isinstance(obj, list):
        return DummyArray(obj)
    return DummyArray([0.0])


array = asarray


def argsort(seq):
    return sorted(range(len(seq)), key=lambda i: seq[i])


def maximum(a, b):
    return [max(x, y) for x, y in zip(a, b)]


def minimum(a, b):
    return [min(x, y) for x, y in zip(a, b)]


def clip(arr, a_min, a_max):
    result = []
    for x in arr:
        if a_min is not None and x < a_min:
            x = a_min
        if a_max is not None and x > a_max:
            x = a_max
        result.append(x)
    return result


def where(cond):
    return ([i for i, c in enumerate(cond) if c],)
