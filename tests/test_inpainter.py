"""Tests für den Inpainter."""

import importlib
import sys
from pathlib import Path

sys.modules["diffusers"] = importlib.import_module("tests.diffusers")
sys.modules["iopaint.model_manager"] = importlib.import_module("tests.iopaint")
sys.modules["PIL"] = importlib.import_module("tests.PIL")
sys.modules["numpy"] = importlib.import_module("tests.numpy")
sys.modules["torch"] = importlib.import_module("tests.torch")
sys.modules["controlnet_aux"] = importlib.import_module("tests.controlnet_aux")
sys.modules["requests"] = importlib.import_module("tests.requests_stub")

from PIL import Image

from core import inpainter


def test_inpaint_creates_output(monkeypatch, tmp_path: Path) -> None:
    img = tmp_path / "img.png"
    mask = tmp_path / "mask.png"
    Image.new("RGB", (8, 8)).save(img)
    Image.new("L", (8, 8)).save(mask)

    monkeypatch.setattr(Image, "open", lambda p: Image.new("RGB", (8, 8)))
    monkeypatch.setattr(inpainter, "ensure_model", lambda *a, **k: tmp_path / "model")
    monkeypatch.setattr(inpainter, "is_gpu_available", lambda: False)

    out = inpainter.inpaint(img, mask, labels=None, model_key="lama")
    assert out.exists()
    res = Image.open(out)
    assert res.size == (8, 8)
