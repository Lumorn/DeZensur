"""Testet das Skript generate_report.py."""

import json
import subprocess
import sys
import os
from pathlib import Path

from core.logger_setup import init_logging


def test_generate_report_creates_file(tmp_path: Path) -> None:
    proj_file = tmp_path / "proj.dezproj"
    proj_file.write_text("{}")

    logger = init_logging(tmp_path)
    logger.info("start")

    log_file = next((tmp_path / "logs").glob("run_*.jsonl"))
    batch_id = log_file.stem.replace("run_", "")
    logger.bind(img="a", model="lama").info("done", duration_ms=500)

    out_file = tmp_path / "report.json"
    html_file = tmp_path / "report.html"
    env = os.environ.copy()
    test_path = Path(__file__).resolve().parent
    env["PYTHONPATH"] = os.pathsep.join([str(test_path), env.get("PYTHONPATH", "")])
    subprocess.check_call(
        [
            sys.executable,
            str(Path(__file__).resolve().parents[1] / "generate_report.py"),
            str(proj_file),
            batch_id,
            "--report",
            str(out_file),
            "--html",
            str(html_file),
        ],
        env=env,
    )

    assert out_file.exists()
    data = json.loads(out_file.read_text())
    assert data["batch_id"] == batch_id
    assert html_file.exists()
