#!/usr/bin/env python3
"""Build-Skript für die portable Windows-EXE.

Das Skript ruft PyInstaller mit einer festen Spec-Datei auf. Es sollte
unter Windows ausgeführt werden.
"""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    spec_file = repo_root / "pyinstaller.spec"
    if not spec_file.exists():
        print("Spec-Datei pyinstaller.spec fehlt", file=sys.stderr)
        sys.exit(1)
    subprocess.run(["pyinstaller", "--clean", spec_file.as_posix()], check=True)


if __name__ == "__main__":
    main()
