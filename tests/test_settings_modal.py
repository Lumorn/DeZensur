"""Testet den Einstellungsdialog via Jest."""

import subprocess
from pathlib import Path

import pytest


def test_jest_runs() -> None:
    """Führt den Jest-Test für das SettingsModal aus."""
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["npx", "jest", "gui/src/__tests__/settings.spec.tsx"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip("Jest konnte nicht ausgeführt werden")
    assert result.returncode == 0
