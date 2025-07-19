import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "dezensor" / "fetch_model.py"
TEST_PATH = Path(__file__).resolve().parent


def test_fetch_model_cli(tmp_path: Path) -> None:
    stub = tmp_path / "stub"
    (stub / "core").mkdir(parents=True)
    (stub / "core" / "__init__.py").write_text("")

    (stub / "core" / "dep_manager.py").write_text(
        "from pathlib import Path\n"
        "def ensure_model(key, prefer_gpu=True):\n"
        f"    p = Path('{tmp_path}') / f\"{{key}}.bin\"\n"
        "    p.write_text('data')\n"
        "    return p\n"
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [
            str(stub),
            str(TEST_PATH),
            env.get("PYTHONPATH", ""),
        ]
    )
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "dummy"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
    assert f"{tmp_path}/dummy.bin" in result.stdout
