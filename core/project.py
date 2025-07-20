from __future__ import annotations

"""Verwaltet Projekte im neuen Schema v2."""

import datetime
import json
import shutil
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 2


class Project:
    """Repräsentiert ein Projekt und speichert Meta‑Infos."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.file = root.with_suffix(".dezproj")
        self.data: dict[str, Any] = {
            "schema": SCHEMA_VERSION,
            "meta": {
                "title": root.name,
                "created": datetime.datetime.utcnow().isoformat(),
            },
            "images": [],
            "settings": {},
        }

    @staticmethod
    def migrate_v1_to_v2(data: dict) -> dict:
        """Wandelt ein Projekt im alten Schema in Version 2 um."""

        return {
            "schema": SCHEMA_VERSION,
            "meta": {
                "title": data.get("title", ""),
                "created": data.get("created", datetime.datetime.utcnow().isoformat()),
            },
            "images": data.get("images", []),
            "settings": data.get("settings", {}),
        }

    @staticmethod
    def load(proj_file: Path) -> "Project":
        """Lädt ein Projekt und führt bei Bedarf eine Migration durch."""

        with proj_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("schema", 1) == 1:
            data = Project.migrate_v1_to_v2(data)
        p = Project(proj_file.with_suffix(""))
        p.data = data
        return p

    def save(self) -> None:
        """Speichert die Projektdaten auf die Festplatte."""

        self._ensure_dirs()
        with self.file.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def _ensure_dirs(self) -> None:
        """Legt notwendige Ordner an."""

        for d in ("originals", "masks", "processed", "logs"):
            (self.root / d).mkdir(parents=True, exist_ok=True)

    def add_images(self, paths: list[str]) -> None:
        """Kopiert Bilder ins Projekt und legt Einträge an."""

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

    def get_image_entry(self, img_id: str) -> dict:
        """Liefert das Dictionary eines Bildes."""

        for entry in self.data["images"]:
            if entry["id"] == img_id:
                return entry
        raise KeyError(img_id)

    def get_image_path(self, img_id: str) -> Path:
        """Pfad zum Originalbild."""

        entry = self.get_image_entry(img_id)
        return self.root / entry["file"]

    def get_mask_path(self, img_id: str) -> Path:
        """Pfad zur Maske."""

        return self.root / "masks" / f"{img_id}_mask.png"

    def update_status(self, img_id: str, status: str, **extra: str) -> None:
        """Aktualisiert den Status eines Bildes."""

        entry = self.get_image_entry(img_id)
        entry["status"] = status
        entry.update(extra)
        self.save()
