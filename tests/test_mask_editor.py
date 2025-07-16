"""Testet den React-basierten Mask-Editor."""

import subprocess
from pathlib import Path


def test_jest_runs() -> None:
    """Führt den Jest-Test für den Mask-Editor aus."""
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run([
        "npx",
        "jest",
        "gui/__tests__/maskEditor.test.js",
    ], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
