"""Bootstrap-Skript zum Starten der Anwendung.

Wird dieses Skript allein heruntergeladen, kann es das Repository selbst
herunterladen und danach wie gewohnt starten.
"""

import os
import shutil
import subprocess
import sys
import time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

# Pfad zum npm-Binary; wird in check_npm ermittelt
npm_cmd = "npm"


project_root = Path(__file__).resolve().parent


def _has_symlink_privilege() -> bool:
    """Prüft, ob unter Windows Symlinks angelegt werden können."""

    if os.name != "nt":
        return True
    import tempfile

    test_dir = Path(tempfile.gettempdir()) / "dez_symlink_test"
    target = test_dir / "target"
    link = test_dir / "link"
    try:
        test_dir.mkdir(exist_ok=True)
        target.write_text("test")
        os.symlink(target, link)
    except OSError:
        return False
    else:
        link.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        test_dir.rmdir()
        return True


def ensure_admin_privileges() -> None:
    """Fordert bei fehlenden Symlink-Rechten Administratorrechte an."""

    if os.name != "nt" or os.environ.get("DEZENSUR_ADMIN"):
        return
    try:
        import ctypes

        if ctypes.windll.shell32.IsUserAnAdmin():
            os.environ["DEZENSUR_ADMIN"] = "1"
            return
    except Exception:
        pass

    if _has_symlink_privilege():
        os.environ["DEZENSUR_ADMIN"] = "1"
        return

    try:
        import ctypes

        params = " ".join(f'"{arg}"' for arg in sys.argv)
        rc = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        if int(rc) > 32:
            sys.exit(0)
    except Exception:
        pass


def run(cmd: list[str], *, beschreibung: str | None = None, **kwargs) -> None:
    """Hilfsfunktion zum Ausführen eines Befehls mit Fortschrittsanzeige."""

    beschreibung = beschreibung or " ".join(cmd)
    if sys.stdout.isatty():
        # ``rich`` erst hier importieren, damit der Start ohne Abhängigkeiten klappt
        try:
            from rich.progress import Progress, SpinnerColumn, TextColumn
        except ImportError:
            # Hinweis ausgeben, falls die Bibliothek fehlt
            print(
                "[Info] Paket 'rich' nicht gefunden - Befehle laufen ohne Fortschrittsanzeige."
            )
            # Fallback ohne Fortschrittsanzeige
            subprocess.run(cmd, check=True, **kwargs)
            return

        # Fortschrittsspinne anzeigen, solange der Prozess läuft
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(beschreibung, start=False)
            proc = subprocess.Popen(cmd, **kwargs)
            progress.start_task(task)
            while proc.poll() is None:
                progress.refresh()
                time.sleep(0.1)
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, cmd)
    else:
        subprocess.run(cmd, check=True, **kwargs)


def ensure_clean_worktree(*, auto_stash: bool = False) -> tuple[bool, bool]:
    """Prüft auf ungesicherte Änderungen und stasht sie optional.

    Gibt ein Tupel zurück: (Arbeitsverzeichnis_sauber, Wurde_Stash_erstellt)
    """

    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=project_root, text=True
        ).strip()
    except subprocess.CalledProcessError as exc:
        print(f"Git-Status konnte nicht abgefragt werden: {exc}")
        return True, False

    if status:
        if auto_stash:
            try:
                run(
                    ["git", "stash", "--include-untracked"],
                    cwd=project_root,
                    beschreibung="git stash",
                )
                return True, True
            except subprocess.CalledProcessError as exc:
                print(f"Fehler beim Stashen: {exc}")
                return False, False

        try:
            tk.Tk().withdraw()
            messagebox.showwarning(
                "Uncommittete Änderungen",
                "Bitte committe oder stash deine Änderungen, bevor ein Pull erfolgt.",
            )
        except tk.TclError:
            # Fallback, falls keine GUI verfügbar ist
            print(
                "Uncommittete Änderungen gefunden. Bitte committe oder stash sie, bevor ein Pull erfolgt."
            )
        return False, False
    return True, False


def update_repo(*, auto_stash: bool = False) -> None:
    """Aktualisiert das Git-Repository und nutzt optional auto-stash."""

    sauber, stashed = ensure_clean_worktree(auto_stash=auto_stash)
    if not sauber:
        return
    try:
        run(["git", "fetch", "origin"], cwd=project_root, beschreibung="git fetch")
        local_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=project_root, text=True
        ).strip()
        remote_sha = subprocess.check_output(
            ["git", "rev-parse", "origin/main"], cwd=project_root, text=True
        ).strip()
        if local_sha != remote_sha:
            run(
                ["git", "pull", "origin", "main"],
                cwd=project_root,
                beschreibung="git pull",
            )
    except subprocess.CalledProcessError as exc:
        # Fehler ausgeben, aber fortfahren, damit das Terminal offen bleibt.
        print(
            f"Git-Aktualisierung fehlgeschlagen: {exc}\nBitte Branch-Tracking einrichten."
        )
    finally:
        if stashed:
            try:
                run(
                    ["git", "stash", "pop"],
                    cwd=project_root,
                    beschreibung="git stash pop",
                )
            except subprocess.CalledProcessError:
                print(
                    "Stash konnte nicht angewendet werden. Bitte manuell 'git stash pop' ausführen."
                )


def check_npm() -> None:
    """Prüft, ob npm und eine ausreichende Node-Version verfügbar sind."""

    global npm_cmd

    # Nach npm suchen und gegebenenfalls Standardpfade pruefen
    npm_cmd = shutil.which("npm")
    if npm_cmd is None:
        env_path = os.environ.get("NPM_PATH")
        if env_path and Path(env_path).exists():
            npm_cmd = env_path
        elif os.name == "nt":
            standard = Path(os.environ.get("ProgramFiles", "")) / "nodejs" / "npm.cmd"
            if standard.exists():
                npm_cmd = str(standard)

    # Wenn weiterhin nichts gefunden wurde, abbrechen
    if npm_cmd is None or shutil.which("node") is None:
        msg = "Node.js bzw. npm wurde nicht gefunden. Bitte erst installieren."
        print(msg)
        tk.Tk().withdraw()
        messagebox.showerror("Fehler", msg)
        sys.exit(1)

    # Node-Version abfragen und auf Mindestversion 18 prüfen
    try:
        proc = subprocess.run(
            ["node", "--version"], capture_output=True, text=True, check=True
        )
        version = proc.stdout.strip().lstrip("v")
        major = int(version.split(".")[0])
        if major < 18:
            msg = f"Node.js Version {version} ist zu alt (>=18 benötigt)."
            print(msg)
            tk.Tk().withdraw()
            messagebox.showerror("Fehler", msg)
            sys.exit(1)
    except Exception:  # pragma: no cover - unerwartete Fehler ignorieren
        pass


def run_npm_audit() -> None:
    """Führt `npm audit` aus und weist bei Fehlern darauf hin."""

    try:
        run([npm_cmd, "audit"], cwd="gui", beschreibung="npm audit")
    except subprocess.CalledProcessError:
        print(
            "npm audit schlug fehl. Bitte ggf. manuell mit Internetverbindung ausführen."
        )


def should_skip_npm_install(argv: list[str] | None = None) -> bool:
    """Entscheidet, ob das NPM-Install ausgelassen werden darf."""

    argv = argv or sys.argv
    skip_requested = os.environ.get("SKIP_NPM_INSTALL") or "--skip-npm" in argv
    if skip_requested and not os.environ.get("CI"):
        print("Warnung: SKIP_NPM_INSTALL ist nur in CI erlaubt und wird ignoriert.")
        return False
    return bool(skip_requested)


def ensure_gui_build(force: bool = False) -> None:
    """Baut das Frontend, falls noch keine Dist-Dateien vorhanden sind.

    Parameter ``force`` erzwingt einen Neu-Build auch bei vorhandenen Dateien.
    """

    dist_index = project_root / "gui" / "dist" / "index.html"
    # Neu bauen, wenn die Datei fehlt oder verdächtig klein ist
    if force or not dist_index.exists() or dist_index.stat().st_size < 1000:
        # Unter Windows kann das Electron-Build scheitern, wenn keine
        # Berechtigung zum Anlegen von Symlinks vorhanden ist. Durch Setzen
        # dieser Umgebungsvariable wird das Codesigning deaktiviert und der
        # entsprechende Download entfaellt.
        env = os.environ.copy()
        if os.name == "nt":
            env.setdefault("CSC_IDENTITY_AUTO_DISCOVERY", "false")
        run(
            [npm_cmd, "run", "build"],
            cwd="gui",
            beschreibung="npm run build",
            env=env,
        )
        # Nach dem Build sicherstellen, dass die Datei wirklich existiert
        if not dist_index.exists():
            msg = "GUI-Build fehlgeschlagen. Bitte 'npm run build' manuell im Ordner gui ausf\u00fchren."
            print(msg)
            tk.Tk().withdraw()
            messagebox.showerror("Fehler", msg)
            sys.exit(1)


def ensure_repo() -> None:
    """Klonen des Git-Repositories, falls die Dateien fehlen."""

    if (project_root / "core").exists():
        return

    repo_url = "https://github.com/Lumorn/DeZensur.git"

    try:
        if not (project_root / ".git").exists():
            # Leeres Git-Repo anlegen und Remote setzen
            run(["git", "init"], cwd=project_root, beschreibung="git init")
            run(
                ["git", "remote", "add", "origin", repo_url],
                cwd=project_root,
                beschreibung="git remote add",
            )
        run(["git", "fetch", "origin"], cwd=project_root, beschreibung="git fetch")
        run(
            ["git", "reset", "--hard", "origin/main"],
            cwd=project_root,
            beschreibung="git reset",
        )
    except Exception as exc:
        tk.Tk().withdraw()
        messagebox.showerror("Fehler", f"Repository konnte nicht geklont werden: {exc}")
        sys.exit(1)

    # Nach erfolgreichem Klonen Skript neu starten
    os.execv(sys.executable, [sys.executable, __file__] + sys.argv[1:])


# Zuerst pruefen wir unter Windows, ob Symlink-Rechte vorhanden sind
ensure_admin_privileges()

# Erst sicherstellen, dass das Repo vorhanden ist
ensure_repo()
# Option für automatisches Stashen auswerten
auto_stash_flag = "--auto-stash" in sys.argv
if auto_stash_flag:
    sys.argv.remove("--auto-stash")
# Option zum Erzwingen eines GUI-Rebuilds auswerten
force_build_flag = "--force-build" in sys.argv
if force_build_flag:
    sys.argv.remove("--force-build")
# Vor allen weiteren Schritten prüfen wir, ob das Git-Repository aktuell ist
update_repo(auto_stash=auto_stash_flag)

# Projektverzeichnis dem Modulpfad hinzufügen
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def main() -> None:
    """Legt die virtuelle Umgebung an und startet die GUI."""

    venv_path = Path(".venv")
    if not venv_path.exists():
        # Virtuelle Umgebung erstellen, falls nicht vorhanden
        run(
            [sys.executable, "-m", "venv", str(venv_path)],
            beschreibung="Erzeuge virtuelle Umgebung",
        )

    # Pfad zum Python-Interpreter der venv ermitteln
    python_bin = venv_path / ("Scripts" if os.name == "nt" else "bin") / "python"

    # Wenn dieses Skript nicht mit dem venv-Python ausgeführt wird,
    # starten wir uns selbst erneut. Um eine Neustart-Schleife zu vermeiden,
    # setzen wir eine Umgebungsvariable.
    if Path(sys.executable).resolve() != python_bin.resolve() and not os.environ.get(
        "DEZENSUR_VENV"
    ):
        os.environ["DEZENSUR_VENV"] = "1"
        if os.name == "nt":
            subprocess.check_call(
                [str(python_bin), __file__] + sys.argv[1:], env=os.environ
            )
            sys.exit(0)
        else:
            os.execv(str(python_bin), [str(python_bin), __file__] + sys.argv[1:])

    # npm und Node-Version pruefen
    check_npm()

    # Python-Abhängigkeiten installieren
    run(
        [str(python_bin), "-m", "pip", "install", "-r", "requirements.txt"],
        beschreibung="pip install",
    )

    # Erst nach der Installation können wir die Module importieren
    from core import censor_detector
    from core.dep_manager import ensure_model

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

    # Prüfen, ob npm-Install übersprungen werden soll
    skip_npm = should_skip_npm_install()

    # NPM-Pakete installieren, falls erforderlich und nicht übersprungen
    if not skip_npm and (
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
        try:
            # npm-Abhängigkeiten installieren
            run([npm_cmd, "install"], cwd="gui", beschreibung="npm install")
            # Nach erfolgreicher Installation Sicherheitsprüfung ausführen
            run_npm_audit()
        except subprocess.CalledProcessError:
            # Hinweis für den Nutzer, falls ein Paket wie electron-trpc nicht verfügbar ist
            print(
                "npm install schlug fehl. Bitte Prüfe die Internetverbindung "
                "oder passe die Version von electron-trpc im package.json an."
            )
            raise
    elif skip_npm:
        print("npm install wird aufgrund von SKIP_NPM_INSTALL übersprungen.")

    if "--dev" in sys.argv:
        run([npm_cmd, "run", "dev"], cwd="gui", beschreibung="npm run dev")
    else:
        # Falls die gebaute Oberflaeche fehlt oder der Nutzer einen Neu-Build
        # erzwingen moechte, wird dieser nun ausgefuehrt
        ensure_gui_build(force=force_build_flag)
        run([npm_cmd, "start"], cwd="gui", beschreibung="npm start")


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
