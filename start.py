"""Bootstrap-Skript zum Starten der Anwendung."""

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

# Sicherstellen, dass das Projektverzeichnis im Modulpfad liegt
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core import censor_detector  # ONNX-Session vorwärmen
from core.dep_manager import ensure_model


def run(cmd: list[str]) -> None:
    """Hilfsfunktion zum Ausführen eines Befehls."""
    subprocess.run(cmd, check=True)


def main() -> None:
    """Legt die virtuelle Umgebung an und startet die GUI."""

    venv_path = Path(".venv")
    if not venv_path.exists():
        # Virtuelle Umgebung erstellen, falls nicht vorhanden
        run([sys.executable, "-m", "venv", str(venv_path)])

    # Pfad zum Python-Interpreter der venv ermitteln
    python_bin = venv_path / ("Scripts" if os.name == "nt" else "bin") / "python"

    # Repository auf den neuesten Stand bringen, damit requirements aktuell sind
    run(["git", "pull"])

    # Python-Abhängigkeiten installieren
    run([str(python_bin), "-m", "pip", "install", "-r", "requirements.txt"])

    try:
        ensure_model("anime_censor_detection")
        ensure_model("sam_vit_hq")
    except Exception as exc:
        tk.Tk().withdraw()
        messagebox.showerror("Fehler", f"Modelldownload schlug fehl: {exc}")
        sys.exit(1)

    pkg_lock = Path("gui/package-lock.json")
    package_json = Path("gui/package.json")
    node_modules = Path("gui/node_modules")

    # NPM-Pakete installieren, falls noetig
    if (
        not node_modules.exists()
        or (
            pkg_lock.exists()
            and pkg_lock.stat().st_mtime > node_modules.stat().st_mtime
        )
        or (
            not pkg_lock.exists()
            and package_json.stat().st_mtime > node_modules.stat().st_mtime
        )
    ):
        run(["npm", "install"], cwd="gui")

    if "--dev" in sys.argv:
        run(["npm", "run", "dev"], cwd="gui")
    else:
        run(["npm", "start"], cwd="gui")


if __name__ == "__main__":
    main()
