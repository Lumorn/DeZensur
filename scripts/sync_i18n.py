#!/usr/bin/env python3
"""Synchronisiert die i18n-JSON-Dateien im GUI-Ordner."""
from __future__ import annotations

import json
from pathlib import Path


def sync() -> None:
    base = Path(__file__).resolve().parents[1] / "gui" / "src" / "i18n"
    de_file = base / "de.json"
    en_file = base / "en.json"

    with de_file.open("r", encoding="utf-8") as f:
        de = json.load(f)
    with en_file.open("r", encoding="utf-8") as f:
        en = json.load(f)

    keys = set(de) | set(en)
    changed = False

    for key in keys:
        if key not in de:
            de[key] = en.get(key, key)
            changed = True
        if key not in en:
            en[key] = de.get(key, key)
            changed = True

    if changed:
        de_file.write_text(
            json.dumps(de, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        en_file.write_text(
            json.dumps(en, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print("\u00dcbersetzungsdateien synchronisiert.")
    else:
        print("Keine Differenzen gefunden.")


if __name__ == "__main__":
    sync()
