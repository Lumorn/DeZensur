class Progress:
    def __init__(self, *a, **k):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        pass

    def add_task(self, *a, **k):
        return 0

    def update(self, *a, **k):
        pass


class BarColumn:
    def __init__(self, *a, **k):
        pass


class TimeRemainingColumn:
    def __init__(self, *a, **k):
        pass
