#!/usr/bin/env python3
"""Hilfsskript, um den Frontend-Build erneut zu erstellen.

Wird nach dem Start nur ein wei\u00dfes Fenster angezeigt, fehlt meist der
Build der Benutzeroberfl\u00e4che. Dieses Skript ruft die Funktion
``ensure_gui_build`` aus ``start.py`` auf und legt die fehlenden Dateien an.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Projektwurzel bestimmen und zum Pythonpfad hinzuf\u00fcgen
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, repo_root.as_posix())

from start import ensure_gui_build  # noqa: E402


def main() -> None:
    """Frontend-Build pr\u00fcfen und bei Bedarf erstellen."""
    dist_index = repo_root / "gui" / "dist" / "index.html"
    if dist_index.exists():
        print("Frontend-Build ist bereits vorhanden.")
    else:
        print("Baue fehlenden Frontend-Build...")
        ensure_gui_build(force=True)
        print("Build abgeschlossen.")

    print("Starte die Anwendung anschlie\u00dfend mit 'python start.py'.")


if __name__ == "__main__":
    main()
