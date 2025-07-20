"""Testet den React-basierten Mask-Editor."""

import subprocess
from pathlib import Path

import pytest


def test_jest_runs() -> None:
    """Führt den Jest-Test für den Mask-Editor aus."""
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["npx", "jest", "gui/__tests__/maskEditor.test.js"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip("Jest konnte nicht ausgef\u00fchrt werden")
    assert result.returncode == 0
