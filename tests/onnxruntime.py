from types import SimpleNamespace


class InferenceSession:
    def __init__(self, *args, **kwargs):
        pass

    def get_inputs(self):
        return [SimpleNamespace(name="input")]

    def run(self, *_):
        # Das echte onnxruntime liefert NumPy-Arrays. Im Test reicht eine
        # einfache Python-Liste mit den erwarteten Werten.
        return [[[0, 0, 640, 640, 0.9, 0]]]
