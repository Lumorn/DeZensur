"""Tests für den Projektmanager."""

from pathlib import Path
import tempfile
from core.project_manager import Project


def test_add_images_creates_copies(tmp_path: Path):
    img_file = tmp_path / "sample.jpg"
    img_file.write_bytes(b"123")

    proj_dir = tmp_path / "proj"
    proj = Project(proj_dir)
    proj.add_images([str(img_file)])

    copied = proj_dir / "originals" / "sample.jpg"
    assert copied.exists(), "Bildkopie sollte vorhanden sein"
