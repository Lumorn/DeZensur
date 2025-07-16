"""Tests für den SAM-Segmenter."""

import importlib
import sys
from pathlib import Path

sys.modules['segment_anything'] = importlib.import_module('tests.segment_anything')
sys.modules['PIL'] = importlib.import_module('tests.PIL')
sys.modules['numpy'] = importlib.import_module('tests.numpy')

from core import segmenter


def test_generate_mask_shape(monkeypatch, tmp_path: Path) -> None:
    img = tmp_path / "img.png"
    from PIL import Image

    Image.new("RGB", (8, 8)).save(img)
    monkeypatch.setattr(Image, 'open', lambda p: Image.new("RGB", (8, 8)))
    monkeypatch.setattr(segmenter, 'ensure_model', lambda *a, **k: tmp_path / 'm.pth')
    monkeypatch.setattr(segmenter, 'is_gpu_available', lambda: False)

    mask = segmenter.generate_mask(img, [{"type": "box", "data": [0, 0, 7, 7]}])
    assert len(mask) == 8
    assert len(mask[0]) == 8


def test_generate_mask_full_area(monkeypatch, tmp_path: Path) -> None:
    img = tmp_path / "img.png"
    from PIL import Image

    Image.new("RGB", (64, 64)).save(img)
    monkeypatch.setattr(Image, 'open', lambda p: Image.new("RGB", (64, 64)))
    monkeypatch.setattr(segmenter, 'ensure_model', lambda *a, **k: tmp_path / 'm.pth')
    monkeypatch.setattr(segmenter, 'is_gpu_available', lambda: False)

    mask = segmenter.generate_mask(img, [{"type": "box", "data": [0, 0, 63, 63]}])
    area = sum(sum(1 for v in row if v) for row in mask)
    assert area == 64 * 64
