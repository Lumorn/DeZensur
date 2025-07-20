"""Roundtrip-Test für das neue Projektschema."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from core.project import Project


def test_migration_roundtrip(tmp_path: Path) -> None:
    data_v1 = {
        "schema": 1,
        "title": "proj",
        "created": "2025-01-01T00:00:00",
        "images": [{"id": "a", "file": "originals/a.png", "status": "pending"}],
        "settings": {},
    }
    proj_file = tmp_path / "proj.dezproj"
    proj_root = tmp_path / "proj"
    proj_root.mkdir()
    proj_file.write_text(json.dumps(data_v1))

    proj = Project.load(proj_file)
    assert proj.data["schema"] == 2
    assert proj.data["meta"]["title"] == "proj"

    proj.save()
    proj2 = Project.load(proj_file)
    assert proj2.data == proj.data
