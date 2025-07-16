"""Tests für den Server-Stub."""

import subprocess
import sys
import time
import requests


def test_server_detect_endpoint(tmp_path):
    proc = subprocess.Popen([sys.executable, "-m", "core.server_stub"])  # noqa: E501
    try:
        time.sleep(1)
        r = requests.post("http://127.0.0.1:8787/detect", json={"id": "x"})
        assert r.status_code == 200
        assert r.json()["action"] == "detect"
    finally:
        proc.terminate()
        proc.wait()
