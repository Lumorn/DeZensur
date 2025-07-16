"""Bootstrap-Skript zum Starten der Anwendung."""

import os
import subprocess
import sys
from pathlib import Path


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

    # Abhängigkeiten installieren
    run([str(python_bin), "-m", "pip", "install", "-r", "requirements.txt"])

    # Repository aktualisieren
    run(["git", "pull"])

    pkg_lock = Path("gui/package-lock.json")
    node_modules = Path("gui/node_modules")
    if pkg_lock.exists() and (
        not node_modules.exists() or pkg_lock.stat().st_mtime > node_modules.stat().st_mtime
    ):
        run(["npm", "install"], cwd="gui")

    if "--dev" in sys.argv:
        run(["npm", "run", "dev"], cwd="gui")
    else:
        run(["npm", "start"], cwd="gui")


if __name__ == "__main__":
    main()
