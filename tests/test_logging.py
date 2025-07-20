"""Tests für das Logging-Modul."""

import json
import sys
from pathlib import Path

import tests.loguru as loguru_stub

sys.modules["loguru"] = loguru_stub

from core.logger_setup import init_logging
from core.report import summarize_batch


def test_logging_and_report(tmp_path: Path) -> None:
    logger = init_logging(tmp_path)
    logger.info("start")

    log_file = next((tmp_path / "logs").glob("run_*.jsonl"))
    batch_id = log_file.stem.replace("run_", "")

    logger.bind(img="img1", model="lama").info("done", duration_ms=500)
    logger.bind(img="img2").error("failed")

    report = summarize_batch(tmp_path, batch_id)

    files = list((tmp_path / "logs").iterdir())
    assert len(files) == 3

    data = json.loads(report.read_text())
    for key in ["batch_id", "images", "avg_sec", "errors", "models", "created"]:
        assert key in data
