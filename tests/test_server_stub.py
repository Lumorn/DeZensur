"""Tests für den Server-Stub."""

import subprocess
import sys
import time
import os
from pathlib import Path
import sys as _sys
from tests import requests_stub, flask
import importlib
import tests.huggingface_hub as hf_stub
sys.modules['huggingface_hub'] = hf_stub
sys.modules['tqdm'] = __import__('tests.tqdm', fromlist=[''])
sys.modules['numpy'] = importlib.import_module('tests.numpy')

_sys.modules['requests'] = requests_stub
_sys.modules['flask'] = flask
import requests


def test_server_detect_endpoint(tmp_path):
    env = os.environ.copy()
    test_path = Path(__file__).resolve().parent
    env["PYTHONPATH"] = os.pathsep.join([str(test_path), env.get("PYTHONPATH", "")])
    proc = subprocess.Popen([sys.executable, "-m", "core.server_stub"], env=env)  # noqa: E501
    try:
        time.sleep(1)
        img = tmp_path / "a.png"
        img.write_bytes(b"x")
        r = requests.post("http://127.0.0.1:8787/detect", json={"path": str(img)})
        assert r.status_code == 200
        assert isinstance(r.json()["boxes"], list)
    finally:
        proc.terminate()
        proc.wait()
