"""Tests für den Batch-Runner."""

import importlib
import sys
import types
from pathlib import Path


# Rich-Stubs früh einsetzen
class DummyProgress:
    def __init__(self, *a, **k):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        pass

    def add_task(self, *a, **k):
        return 0

    def update(self, *a, **k):
        pass

rich_stub = types.SimpleNamespace(Progress=lambda *a, **k: DummyProgress(), BarColumn=lambda: None, TimeRemainingColumn=lambda: None)
sys.modules['rich.progress'] = rich_stub
sys.modules['PIL'] = importlib.import_module('tests.PIL')
sys.modules['numpy'] = importlib.import_module('tests.numpy')
sys.modules['onnxruntime'] = importlib.import_module('tests.onnxruntime')
sys.modules['torch'] = importlib.import_module('tests.torch')
import tests.requests_stub as requests_stub

sys.modules['requests'] = requests_stub
import tests.huggingface_hub as hf_stub

sys.modules['huggingface_hub'] = hf_stub
import tests.loguru as loguru_stub

sys.modules['loguru'] = loguru_stub
sys.modules['tqdm'] = importlib.import_module('tests.tqdm')
sys.modules['segment_anything'] = importlib.import_module('tests.segment_anything')

from PIL import Image

import core.batch_runner as batch_runner
from core.project_manager import Project


def test_run_batch_updates_status(monkeypatch, tmp_path: Path) -> None:
    img1 = tmp_path / "a.png"
    img2 = tmp_path / "b.png"
    Image.new("RGB", (4, 4)).save(img1)
    Image.new("RGB", (4, 4)).save(img2)

    proj_dir = tmp_path / "proj"
    proj = Project(proj_dir)
    proj.add_images([str(img1), str(img2)])

    monkeypatch.setattr(batch_runner, "detect_censor", lambda *a, **k: [{"box": [0, 0, 1, 1]}])
    monkeypatch.setattr(batch_runner, "generate_mask", lambda *a, **k: [[True]])
    monkeypatch.setattr(batch_runner, "save_mask_png", lambda mask, p: p.write_text("m"))

    def fake_inpaint(image_path, mask_path, labels=None, model_key="lama", user_prompt=""):
        out = mask_path.parent.parent / "processed" / f"{Path(image_path).stem}_{model_key}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("r")
        return out

    monkeypatch.setattr(batch_runner, "inpaint", fake_inpaint)
    monkeypatch.setattr(batch_runner, "is_gpu_available", lambda: False)

    batch_runner.run_batch(proj.file, disable_progress=True)

    updated = Project.load(proj.file)
    assert all(img["status"] == "done" for img in updated.data["images"])
