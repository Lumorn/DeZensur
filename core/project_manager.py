"""Verwaltet Projekte und die zugehörigen Dateien."""

from __future__ import annotations

import datetime
import json
import shutil
from pathlib import Path

SCHEMA_VERSION = 1


class Project:
    """Repräsentiert ein Projekt."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.file = root.with_suffix(".dezproj")
        self.data = {
            "schema": SCHEMA_VERSION,
            "title": root.name,
            "created": datetime.datetime.utcnow().isoformat(),
            "images": [],
            "settings": {},
        }

    @staticmethod
    def load(proj_file: Path) -> "Project":
        with proj_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        p = Project(proj_file.with_suffix(""))
        p.data = data
        return p

    def save(self) -> None:
        with self.file.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def _ensure_dirs(self) -> None:
        for d in ("originals", "masks", "processed", "logs"):
            (self.root / d).mkdir(parents=True, exist_ok=True)

    def add_images(self, paths: list[str]) -> None:
        self._ensure_dirs()
        for p in paths:
            dest = self.root / "originals" / Path(p).name
            shutil.copy2(p, dest)
            self.data["images"].append(
                {
                    "id": dest.stem,
                    "file": str(dest.relative_to(self.root)),
                    "status": "pending",
                }
            )
        self.save()
