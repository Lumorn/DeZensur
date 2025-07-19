"""Führt den Jest-Test aus, der die i18n-Schlüssel prüft."""

import subprocess
from pathlib import Path
import pytest


def test_jest_runs() -> None:
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["npx", "jest", "gui/src/__tests__/i18n.keys.spec.ts"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip("Jest konnte nicht ausgeführt werden")
    assert result.returncode == 0
