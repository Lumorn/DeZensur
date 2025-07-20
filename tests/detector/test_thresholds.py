"""Tests fuer die Schwellenwert-Logik im Zensurdetektor."""

import importlib
import sys
from pathlib import Path

# Stubs fuer Abhaengigkeiten einbinden
sys.modules["PIL"] = importlib.import_module("tests.PIL")
sys.modules["numpy"] = importlib.import_module("tests.numpy")
sys.modules["requests"] = importlib.import_module("tests.requests_stub")
sys.modules["huggingface_hub"] = importlib.import_module("tests.huggingface_hub")
sys.modules["tqdm"] = importlib.import_module("tests.tqdm")
sys.modules["loguru"] = importlib.import_module("tests.loguru")
sys.modules["onnxruntime"] = importlib.import_module("tests.onnxruntime")
sys.modules["torch"] = importlib.import_module("tests.torch")

from core import censor_detector


class DummySession:
    def get_inputs(self):
        from types import SimpleNamespace

        return [SimpleNamespace(name="input")]

    def run(self, *a, **k):
        # Zwei Vorhersagen mit unterschiedlichem Score
        return [[[0, 0, 320, 320, 0.4, 0], [0, 0, 320, 320, 0.8, 0]]]


def test_threshold(monkeypatch, tmp_path: Path) -> None:
    img = tmp_path / "img.png"
    from PIL import Image

    Image.new("RGB", (10, 10)).save(img)
    monkeypatch.setattr(
        censor_detector.dep_manager, "ensure_model", lambda *a, **k: tmp_path / "m.onnx"
    )
    monkeypatch.setattr(censor_detector.dep_manager, "is_gpu_available", lambda: False)
    monkeypatch.setattr(
        censor_detector, "_load_session", lambda *a, **k: DummySession()
    )

    boxes = censor_detector.detect_censor(img, threshold=0.5)
    assert len(boxes) == 1
    assert boxes[0]["score"] > 0.5
