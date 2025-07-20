"""Wrapper für SAM-Modelle zur Maskengenerierung."""

from __future__ import annotations

import argparse
import functools
import json
from pathlib import Path

import numpy as np
from PIL import Image
from segment_anything import SamPredictor, sam_model_registry

from .dep_manager import ensure_model, is_gpu_available
from .logger_setup import get_logger

LOGGER = get_logger(__name__)


@functools.lru_cache(maxsize=2)
def load_sam(model_key: str) -> SamPredictor:
    """Lädt ein SAM-Modell und cached den Predictor."""

    # Bei fehlender GPU automatisch auf MobileSAM ausweichen
    if model_key == "sam_vit_hq" and not is_gpu_available():
        LOGGER.info("GPU nicht vorhanden, nutze MobileSAM")
        model_key = "sam_mobile"

    model_path = ensure_model(model_key)
    model_type = "vit_t" if model_key == "sam_mobile" else "vit_h"
    LOGGER.info("Lade SAM-Modell {}", model_path)
    sam = sam_model_registry[model_type](checkpoint=str(model_path))
    predictor = SamPredictor(sam)
    device = "cuda" if is_gpu_available() else "cpu"
    predictor.model.to(device)
    return predictor


def _merge_mask(target: list[list[bool]], src: list[list[bool]]) -> None:
    """Hilfsfunktion zum Verschmelzen zweier Masken."""

    for y, row in enumerate(src):
        for x, val in enumerate(row):
            if val:
                target[y][x] = True


def generate_mask(
    image_path: Path,
    prompts: list[dict],
    model_key: str = "sam_vit_hq",
    multimask: bool = False,
) -> np.ndarray:
    """Erzeugt eine Bool-Maske aus Box- oder Punkt-Prompts."""

    img = Image.open(image_path).convert("RGB")
    predictor = load_sam(model_key)
    predictor.set_image(np.asarray(img))
    width, height = img.size
    # Manche Stubs benötigen diese Info separat
    try:
        predictor.image_shape = (height, width)
    except Exception:
        pass
    final_mask = [[False] * width for _ in range(height)]

    for prm in prompts:
        if prm.get("type") == "box":
            box = np.asarray(prm["data"], dtype=np.float32)
            masks, _, _ = predictor.predict(box=box, multimask_output=multimask)
        elif prm.get("type") == "point":
            x, y, label = prm["data"]
            coords = np.asarray([[x, y]], dtype=np.float32)
            labels = np.asarray([label], dtype=np.int32)
            masks, _, _ = predictor.predict(
                point_coords=coords,
                point_labels=labels,
                multimask_output=multimask,
            )
        else:
            raise ValueError(f"Unbekannter Prompt-Typ: {prm.get('type')}")

        # Erste Maske aus der Vorhersage entnehmen und in Bool-Werte wandeln
        mask = masks[0]
        mask_bool = [[bool(px) for px in row] for row in np.asarray(mask)]
        _merge_mask(final_mask, mask_bool)

    if not any(any(r) for r in final_mask):
        raise RuntimeError("Keine Maske erzeugt")

    return np.asarray(final_mask, dtype=bool)


def save_mask_png(mask: np.ndarray, out_path: Path) -> None:
    """Speichert eine Binärmaske als PNG mit Transparenz."""

    height, width = mask.shape[:2]
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    alpha = Image.fromarray((np.asarray(mask, dtype=np.uint8) * 255), mode="L")
    img.putalpha(alpha)
    img.save(out_path)


def cli() -> None:
    """CLI-Einstiegspunkt."""

    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("--boxes", nargs="*", default=[])
    parser.add_argument("--points", nargs="*", default=[])
    parser.add_argument("--model", default="sam_vit_hq")
    parser.add_argument("--out", default="mask.png")
    parser.add_argument("--multimask", action="store_true")
    args = parser.parse_args()

    prm: list[dict] = []
    for b in args.boxes:
        x1, y1, x2, y2 = map(int, b.split(","))
        prm.append({"type": "box", "data": [x1, y1, x2, y2]})
    for p in args.points:
        x, y, label = map(int, p.split(","))
        prm.append({"type": "point", "data": [x, y, label]})

    mask = generate_mask(Path(args.image), prm, args.model, args.multimask)
    save_mask_png(mask, Path(args.out))
    stats = {"H": mask.shape[0], "W": mask.shape[1], "area_px": int(mask.sum())}
    print(json.dumps(stats))


if __name__ == "__main__":
    cli()
