import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.modules['diffusers'] = importlib.import_module('tests.diffusers')
sys.modules['iopaint.model_manager'] = importlib.import_module('tests.iopaint')
sys.modules['PIL'] = importlib.import_module('tests.PIL')
sys.modules['numpy'] = importlib.import_module('tests.numpy')
sys.modules['torch'] = importlib.import_module('tests.torch')
sys.modules['controlnet_aux'] = importlib.import_module('tests.controlnet_aux')
sys.modules['huggingface_hub'] = importlib.import_module('tests.huggingface_hub')
sys.modules['requests'] = importlib.import_module('tests.requests_stub')
sys.modules['tqdm'] = importlib.import_module('tests.tqdm')

from PIL import Image

from core.inpainter import _blend_seams


def test_blend_seams_returns_image(tmp_path: Path) -> None:
    orig = Image.new('RGB', (8, 8))
    res = Image.new('RGB', (8, 8))
    mask = Image.new('L', (8, 8))
    out = _blend_seams(res, orig, mask)
    assert hasattr(out, 'size') and out.size == (8, 8)
