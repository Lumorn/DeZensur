import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "dez.py"
TEST_PATH = Path(__file__).resolve().parent.parent


def _run(args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(TEST_PATH), env.get("PYTHONPATH", "")])
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env)


def test_detect_batch(tmp_path: Path) -> None:
    img = tmp_path / "b.png"
    img.write_bytes(b"123")
    models = Path("models/anime_censor_detection/censor_detect_v0.9_s")
    models.mkdir(parents=True, exist_ok=True)
    (models / "model.onnx").write_text("x")

    out_file = tmp_path / "result.json"
    res = _run(["detect-batch", str(tmp_path), "--out", str(out_file)])
    assert res.returncode == 0
    data = json.loads(out_file.read_text())
    assert "b.png" in data
