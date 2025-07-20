import importlib
import sys
from pathlib import Path

sys.modules["segment_anything"] = importlib.import_module("tests.segment_anything")
sys.modules["PIL"] = importlib.import_module("tests.PIL")
sys.modules["numpy"] = importlib.import_module("tests.numpy")
sys.modules["requests"] = importlib.import_module("tests.requests")
sys.modules["torch"] = importlib.import_module("tests.torch")
sys.modules["huggingface_hub"] = importlib.import_module("tests.huggingface_hub")
sys.modules["tqdm"] = importlib.import_module("tests.tqdm")
sys.modules["loguru"] = importlib.import_module("tests.loguru")

from core import segmenter


def test_sam_hq_gpu_pipeline(monkeypatch, tmp_path: Path) -> None:
    # Cache leeren, um sicheres Laden zu gewährleisten
    segmenter.load_sam.cache_clear()

    img = tmp_path / "img.png"
    from PIL import Image

    Image.new("RGB", (8, 8)).save(img)

    used = {}

    def fake_ensure_model(key: str):
        used["key"] = key
        return tmp_path / f"{key}.pth"

    monkeypatch.setattr(segmenter, "ensure_model", fake_ensure_model)
    monkeypatch.setattr(segmenter, "is_gpu_available", lambda: True)

    segmenter.generate_mask(img, [{"type": "box", "data": [0, 0, 7, 7]}])
    assert used["key"] == "sam_vit_hq"
