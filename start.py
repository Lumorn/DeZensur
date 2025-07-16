"""Bootstrap-Skript zum Starten der Anwendung.

Wird dieses Skript allein heruntergeladen, kann es das Repository selbst
herunterladen und danach wie gewohnt starten.
"""

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
import shutil

project_root = Path(__file__).resolve().parent


def run(cmd: list[str], **kwargs) -> None:
    """Hilfsfunktion zum Ausführen eines Befehls."""
    subprocess.run(cmd, check=True, **kwargs)


def update_repo() -> None:
    """Prüft, ob das Git-Repository aktuell ist und aktualisiert es falls nötig."""
    try:
        run(["git", "fetch", "origin"], cwd=project_root)
        local_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=project_root, text=True
        ).strip()
        remote_sha = subprocess.check_output(
            ["git", "rev-parse", "origin/main"], cwd=project_root, text=True
        ).strip()
        if local_sha != remote_sha:
            run(["git", "pull", "origin", "main"], cwd=project_root)
    except subprocess.CalledProcessError as exc:
        # Fehler ausgeben, aber fortfahren, damit das Terminal offen bleibt.
        print(f"Git-Aktualisierung fehlgeschlagen: {exc}\nBitte Branch-Tracking einrichten.")


def check_npm() -> None:
    """Prueft, ob npm verfuegbar ist."""
    if shutil.which("npm") is None:
        tk.Tk().withdraw()
        messagebox.showerror(
            "Fehler",
            "Node.js bzw. npm wurde nicht gefunden. Bitte erst installieren."
        )
        sys.exit(1)

def ensure_repo() -> None:
    """Klonen des Git-Repositories, falls die Dateien fehlen."""

    if (project_root / "core").exists():
        return

    repo_url = "https://github.com/Lumorn/DeZensur.git"

    try:
        if not (project_root / ".git").exists():
            # Leeres Git-Repo anlegen und Remote setzen
            run(["git", "init"], cwd=project_root)
            run(["git", "remote", "add", "origin", repo_url], cwd=project_root)
        run(["git", "fetch", "origin"], cwd=project_root)
        run(["git", "reset", "--hard", "origin/main"], cwd=project_root)
    except Exception as exc:
        tk.Tk().withdraw()
        messagebox.showerror("Fehler", f"Repository konnte nicht geklont werden: {exc}")
        sys.exit(1)

    # Nach erfolgreichem Klonen Skript neu starten
    os.execv(sys.executable, [sys.executable, __file__] + sys.argv[1:])


# Erst sicherstellen, dass das Repo vorhanden ist
ensure_repo()

# Projektverzeichnis dem Modulpfad hinzufügen
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def main() -> None:
    """Legt die virtuelle Umgebung an und startet die GUI."""

    venv_path = Path(".venv")
    if not venv_path.exists():
        # Virtuelle Umgebung erstellen, falls nicht vorhanden
        run([sys.executable, "-m", "venv", str(venv_path)])

    # Pfad zum Python-Interpreter der venv ermitteln
    python_bin = venv_path / ("Scripts" if os.name == "nt" else "bin") / "python"

    # Repository pruefen und aktualisieren
    update_repo()
    check_npm()

    # Python-Abhängigkeiten installieren
    run([str(python_bin), "-m", "pip", "install", "-r", "requirements.txt"])

    # Erst nach der Installation können wir die Module importieren
    from core.dep_manager import ensure_model
    from core import censor_detector

    try:
        ensure_model("anime_censor_detection")
        ensure_model("sam_vit_hq")
        # ONNX-Session einmalig starten, um Wartezeit zu sparen
        censor_detector._load_session("anime_censor_detection")
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
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        # Fehlermeldung ausgeben und auf Eingabe warten, damit das Terminal
        # geoeffnet bleibt und der Nutzer den Fehler sehen kann.
        import traceback

        print(f"Fehler: {exc}")
        traceback.print_exc()
        input("Zum Beenden Enter druecken...")
        sys.exit(1)
