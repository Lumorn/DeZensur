"""Hilfsfunktionen zum Laden von Bildern."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image


def load_image(project_root: Path, rel_path: str) -> Image.Image:
    """Lädt ein Bild aus dem Ordner ``originals``."""
    path = project_root / rel_path
    return Image.open(path)


def thumbnail(image: Image.Image, size: tuple[int, int] = (256, 256)) -> bytes:
    """Erzeugt ein Thumbnail und gibt die Bytes zurück."""
    img = image.copy()
    img.thumbnail(size)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
