import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "dez.py"
TEST_PATH = Path(__file__).resolve().parent.parent


def _run(args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([
        str(TEST_PATH),
        env.get("PYTHONPATH", ""),
    ])
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_inpaint_cli(tmp_path: Path) -> None:
    img = tmp_path / "img.png"
    mask = tmp_path / "mask.png"
    img.write_bytes(b"0")
    mask.write_bytes(b"0")

    models = Path("models/iopaint_lama")
    models.mkdir(parents=True, exist_ok=True)
    (models / "big-lama.zip").write_text("x")

    out_file = tmp_path / "out.png"
    res = _run([
        "inpaint",
        str(img),
        "--mask",
        str(mask),
        "--out",
        str(out_file),
    ])
    assert res.returncode == 0
    assert out_file.exists()
