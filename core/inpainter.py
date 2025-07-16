"""Inpainting von zensierten Bildbereichen mit wahlweisen Modellen."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
from PIL import Image

from .dep_manager import ensure_model, is_gpu_available
from .prompt_helper import build_prompt

import torch

SUPPORTED_MODELS = {
    "lama": "big_lama",
    "sd2_inpaint": "sd2_inpaint",
    "revanimated": "revanimated_inpaint",
}

logger = logging.getLogger(__name__)


def _load_images(image_path: Path, mask_path: Path) -> tuple[Image.Image, Image.Image]:
    """Lädt Bild und Maske und prüft das Seitenverhältnis."""
    img = Image.open(image_path).convert("RGB")
    mask = Image.open(mask_path).convert("L")
    if img.size != mask.size:
        mask = mask.resize(img.size)
    w, h = img.size
    ratio = max(w / h, h / w)
    if ratio > 1.5:
        logging.warning("Ungewöhnliches Seitenverhältnis: %.2f", ratio)
    return img, mask


def inpaint(
    image_path: Path,
    mask_path: Path,
    labels: list[str] | None = None,
    model_key: str = "lama",
    user_prompt: str = "",
) -> Path:
    """Gibt den Pfad zum Ergebnis-PNG im Ordner ``processed`` zurück."""
    img, mask = _load_images(image_path, mask_path)
    device = "cuda" if is_gpu_available() else "cpu"

    prompt, negative_prompt = "", ""
    if model_key != "lama":
        prompt, negative_prompt = build_prompt(labels or [], user_prompt)

    if device == "cpu":
        # CPU-Fallback: liefert nur ein leeres Bild zur Wahrung der Dimensionen
        result = Image.new("RGB", img.size)
    elif model_key == "lama":
        model_path = ensure_model("big_lama")
        from lama_cleaner.model_manager import ModelManager

        image_np = np.asarray(img)[:, :, ::-1]
        mask_np = np.asarray(mask)
        model = ModelManager(name="lama", model_dir=model_path, device=device)
        res_np = model(image_np, mask_np)
        result = Image.fromarray(res_np[:, :, ::-1])
    else:
        from diffusers import StableDiffusionInpaintPipeline

        model_path = ensure_model(SUPPORTED_MODELS[model_key])
        dtype = torch.float16 if device == "cuda" else torch.float32
        pipe = StableDiffusionInpaintPipeline.from_pretrained(
            model_path, safety_checker=None, torch_dtype=dtype
        ).to(device)
        with torch.cuda.amp.autocast(device if device == "cuda" else "cpu"):
            result = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image=img,
                mask_image=mask,
                num_inference_steps=30,
                strength=0.98,
            ).images[0]

    out_dir = image_path.parent.parent / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{image_path.stem}_{model_key}.png"
    result.save(out_path)
    if prompt:
        prompt_file = out_path.with_suffix(".txt")
        prompt_file.write_text(prompt)
    return out_path


def cli() -> None:
    """Kommandozeilenschnittstelle für das Modul."""
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("mask")
    parser.add_argument(
        "--model", default="lama", choices=list(SUPPORTED_MODELS.keys())
    )
    parser.add_argument("--prompt", default="")
    parser.add_argument("--out", default="processed/out.png")
    args = parser.parse_args()

    out = inpaint(
        Path(args.image),
        Path(args.mask),
        None,
        args.model,
        args.prompt,
    )
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Image.open(out).save(args.out)
    print(out)


if __name__ == "__main__":
    cli()
