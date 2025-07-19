"""Lädt Übersetzungsdateien aus dem GUI-Ordner."""

from __future__ import annotations

import json
from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=None)
def load_translations(lang: str) -> dict[str, str]:
    """Gibt das Übersetzungs-Dictionary für die gewünschte Sprache zurück."""
    base = Path(__file__).resolve().parents[1] / "gui" / "src" / "i18n"
    path = base / f"{lang}.json"
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def translate(lang: str, key: str) -> str:
    """Liefert die Übersetzung oder den Schlüssel selbst."""
    return load_translations(lang).get(key, key)
