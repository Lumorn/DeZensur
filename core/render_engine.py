"""Asynchrone Tile-Render-Engine mit Abbruch- und Resume-Funktion."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Iterable, Tuple, Set

from PIL import Image


class TileRenderer:
    """Rendert ein Bild kachelweise und erlaubt Pausieren."""

    def __init__(self, image: Image.Image, tile_size: int = 128) -> None:
        self.image = image
        self.tile_size = tile_size
        self.done: Set[Tuple[int, int]] = set()
        self._abort = False

    def abort(self) -> None:
        """Bricht den aktuellen Durchlauf nach der laufenden Kachel ab."""
        self._abort = True

    def get_state(self) -> Set[Tuple[int, int]]:
        """Gibt bereits gerenderte Kacheln zurück."""
        return set(self.done)

    def save_state(self, path: Path) -> None:
        """Speichert den Fortschritt als JSON-Datei."""
        data = sorted(list(self.done))
        path.write_text(json.dumps(data), encoding="utf-8")

    def load_state(self, path: Path) -> None:
        """Lädt zuvor gespeicherten Fortschritt."""
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            self.done = {tuple(item) for item in data}

    async def render(self, state: Iterable[Tuple[int, int]] | None = None):
        """Asynchrone Erzeugung der Bildkacheln."""
        self._abort = False
        if state is not None:
            self.done = set(state)
        width, height = self.image.size
        for y in range(0, height, self.tile_size):
            for x in range(0, width, self.tile_size):
                if (x, y) in self.done:
                    continue
                if self._abort:
                    return
                box = (x, y, x + self.tile_size, y + self.tile_size)
                tile = self.image.crop(box)
                await asyncio.sleep(0)  # Kontrolle an Eventloop abgeben
                self.done.add((x, y))
                yield (x, y), tile
