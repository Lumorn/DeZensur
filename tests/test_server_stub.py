"""Tests für den Server-Stub."""

import importlib
import os
import subprocess
import sys
import sys as _sys
import time
import types
from pathlib import Path

import tests.huggingface_hub as hf_stub
from tests import flask, requests_stub

sys.modules['huggingface_hub'] = hf_stub
sys.modules['tqdm'] = __import__('tests.tqdm', fromlist=[''])
sys.modules['numpy'] = importlib.import_module('tests.numpy')
rich_stub = types.SimpleNamespace(
    Progress=lambda *a, **k: types.SimpleNamespace(__enter__=lambda s: s, __exit__=lambda s, *e: None, add_task=lambda *a, **k: 0, update=lambda *a, **k: None),
    BarColumn=lambda: None,
    TimeRemainingColumn=lambda: None,
)
sys.modules['rich.progress'] = rich_stub

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


def test_server_batch_endpoint(tmp_path):
    env = os.environ.copy()
    test_path = Path(__file__).resolve().parent
    env["PYTHONPATH"] = os.pathsep.join([str(test_path), env.get("PYTHONPATH", "")])
    proc = subprocess.Popen([sys.executable, "-m", "core.server_stub"], env=env)
    try:
        time.sleep(1)
        proj = tmp_path / "p"
        proj.mkdir()
        r = requests.post(
            "http://127.0.0.1:8787/batch", json={"project": str(proj)}
        )
        assert r.status_code == 200
        assert "task" in r.json()
    finally:
        proc.terminate()
        proc.wait()
