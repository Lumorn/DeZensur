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
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env
    )


def test_help() -> None:
    result = _run(["--help"])
    assert result.returncode == 0
    assert "detect" in result.stdout


def test_detect(tmp_path: Path) -> None:
    img = tmp_path / "a.png"
    img.write_bytes(b"123")
    models = Path("models/anime_censor_detection/censor_detect_v0.9_s")
    models.mkdir(parents=True, exist_ok=True)
    (models / "model.onnx").write_text("x")

    out_file = tmp_path / "result.json"
    res = _run(["detect", str(tmp_path), "--out", str(out_file)])
    assert res.returncode == 0
    assert out_file.exists()
    data = json.loads(out_file.read_text())
    assert "a.png" in data
