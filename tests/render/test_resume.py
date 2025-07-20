import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.modules['PIL'] = importlib.import_module('tests.PIL')

import asyncio

from PIL import Image

from core.render_engine import TileRenderer


def test_resume(tmp_path: Path) -> None:
    img = Image.new("RGB", (8, 8))
    engine = TileRenderer(img, tile_size=4)

    tiles = []

    async def run_first():
        async for pos, _ in engine.render():
            tiles.append(pos)
            if len(tiles) == 2:
                engine.abort()
    asyncio.run(run_first())

    assert len(engine.get_state()) == 2

    async def run_resume():
        async for pos, _ in engine.render(state=engine.get_state()):
            tiles.append(pos)
    asyncio.run(run_resume())

    assert len(tiles) == 4
