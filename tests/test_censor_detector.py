"""Tests für den Censor-Detector."""
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.modules['PIL'] = importlib.import_module('tests.PIL')
from PIL import Image

sys.modules['numpy'] = importlib.import_module('tests.numpy')

import tests.requests_stub as requests_stub

sys.modules['requests'] = requests_stub
import tests.huggingface_hub as hf_stub

sys.modules['huggingface_hub'] = hf_stub
sys.modules['tqdm'] = __import__('tests.tqdm', fromlist=[''])
import tests.loguru as loguru_stub

sys.modules['loguru'] = loguru_stub

sys.modules['onnxruntime'] = __import__('onnxruntime') if 'onnxruntime' in sys.modules else sys.modules.get('onnxruntime')
# ensure stubs for offline
import tests.onnxruntime as onnxruntime_stub

sys.modules['onnxruntime'] = onnxruntime_stub
sys.modules['torch'] = __import__('tests.torch', fromlist=[''])

from core import censor_detector


def test_detect_censor(monkeypatch, tmp_path: Path) -> None:
    img = tmp_path / "img.png"
    Image.new("RGB", (10, 10)).save(img)

    monkeypatch.setattr(censor_detector.dep_manager, 'ensure_model', lambda *a, **k: tmp_path / 'model.onnx')
    monkeypatch.setattr(censor_detector.dep_manager, 'is_gpu_available', lambda: False)

    boxes = censor_detector.detect_censor(img)
    assert isinstance(boxes, list)
    assert {'label', 'score', 'box'} <= boxes[0].keys()


def test_roi_filtering(monkeypatch, tmp_path: Path) -> None:
    img = tmp_path / "img.png"
    Image.new("RGB", (10, 10)).save(img)

    class DummySession:
        def get_inputs(self):
            from types import SimpleNamespace
            return [SimpleNamespace(name="input")]

        def run(self, *a, **k):
            return [[[0, 0, 320, 320, 0.9, 0]]]

    monkeypatch.setattr(censor_detector.dep_manager, 'ensure_model', lambda *a, **k: tmp_path / 'model.onnx')
    monkeypatch.setattr(censor_detector.dep_manager, 'is_gpu_available', lambda: False)
    monkeypatch.setattr(censor_detector, '_load_session', lambda *a, **k: DummySession())

    boxes = censor_detector.detect_censor(img, roi=(0.5, 0.5, 1.0, 1.0))
    assert boxes == []


def test_cli(tmp_path: Path) -> None:
    img = tmp_path / "img.png"
    Image.new("RGB", (10, 10)).save(img)
    models_dir = Path("models/anime_censor_detection")
    models_dir.mkdir(parents=True, exist_ok=True)
    subdir = models_dir / "censor_detect_v0.9_s"
    subdir.mkdir(parents=True, exist_ok=True)
    (subdir / "model.onnx").write_text("x")
    env = os.environ.copy()
    test_path = Path(__file__).resolve().parent
    env["PYTHONPATH"] = os.pathsep.join([str(test_path), env.get("PYTHONPATH", "")])
    proc = subprocess.run([sys.executable, "-m", "core.censor_detector", str(img)], capture_output=True, text=True, env=env)
    assert proc.returncode == 0
    data = json.loads(proc.stdout.strip())
    assert isinstance(data, list)
    assert {'label', 'score', 'box'} <= data[0].keys()


def test_cli_with_roi(tmp_path: Path) -> None:
    img = tmp_path / "img.png"
    Image.new("RGB", (10, 10)).save(img)
    models_dir = Path("models/anime_censor_detection")
    models_dir.mkdir(parents=True, exist_ok=True)
    subdir = models_dir / "censor_detect_v0.9_s"
    subdir.mkdir(parents=True, exist_ok=True)
    (subdir / "model.onnx").write_text("x")
    env = os.environ.copy()
    test_path = Path(__file__).resolve().parent
    env["PYTHONPATH"] = os.pathsep.join([str(test_path), env.get("PYTHONPATH", "")])
    proc = subprocess.run([
        sys.executable,
        "-m",
        "core.censor_detector",
        str(img),
        "--roi",
        "0,0,1,1",
    ], capture_output=True, text=True, env=env)
    assert proc.returncode == 0
    data = json.loads(proc.stdout.strip())
    assert isinstance(data, list)
    assert {'label', 'score', 'box'} <= data[0].keys()


