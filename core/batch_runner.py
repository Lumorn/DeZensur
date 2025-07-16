from __future__ import annotations

"""Batch-Verarbeitung kompletter Projekte."""

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from contextlib import nullcontext
import sys
from core.project_manager import Project
from core.censor_detector import detect_censor
from core.segmenter import generate_mask, save_mask_png
from core.inpainter import inpaint
from core.dep_manager import is_gpu_available
from core.logger_setup import init_logging
from core.report import summarize_batch
import os
import time
import datetime
import argparse

def boxes_to_prompts(boxes: list[dict]) -> list[dict]:
    """Wandelt Box-Ergebnisse in Prompt-Dictionaries um."""
    return [{"type": "box", "data": b["box"]} for b in boxes]


def _process_image(
    project: Project,
    img: dict,
    model_detector: str,
    model_sam: str,
    model_inpaint: str,
    logger,
) -> None:
    """Führt die Pipeline für ein einzelnes Bild aus."""
    img_id = img["id"]
    img_path = project.get_image_path(img_id)
    start = time.perf_counter()

    try:
        boxes = detect_censor(img_path, model_name=model_detector)
        prompts = boxes_to_prompts(boxes)
        mask = generate_mask(img_path, prompts, model_sam)
        mask_path = project.get_mask_path(img_id)
        save_mask_png(mask, mask_path)
        result = inpaint(img_path, mask_path, model_key=model_inpaint)

        elapsed = int((time.perf_counter() - start) * 1000)
        project.update_status(img_id, "done", mask=str(mask_path), result=str(result))
        logger.bind(img=img_id).info(
            "done",
            duration_ms=elapsed,
            model=model_inpaint,
        )
    except Exception:
        logger.bind(img=img_id).exception("failed")


def run_batch(
    project_file: Path,
    max_workers: int | None = None,
    model_detector: str = "anime_censor_detection",
    model_sam: str = "sam_vit_hq",
    model_inpaint: str = "lama",
    disable_progress: bool = False,
) -> None:
    """Verarbeitet alle noch offenen Bilder eines Projektes."""

    project = Project.load(project_file)
    logger = init_logging(project.root)
    batch_id = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    logger = logger.bind(batch=batch_id)
    todo = [img for img in project.data["images"] if img.get("status") == "pending"]

    # Anzahl Threads automatisch wählen
    if max_workers is None:
        # Bei CPU-LaMa können mehrere Worker laufen
        if model_inpaint == "lama" and not is_gpu_available():
            max_workers = min(4, os.cpu_count() or 1)
        else:
            # GPU-Inpainting läuft besser seriell
            max_workers = 1

    show_progress = (not disable_progress) and sys.stdout.isatty()
    progress_ctx = (
        Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
        )
        if show_progress
        else nullcontext()
    )
    with progress_ctx as progress:
        task = progress.add_task("[cyan]Batch-Job", total=len(todo)) if show_progress else None
        with ThreadPoolExecutor(max_workers=max_workers) as exe:
            futures = {
                exe.submit(
                    _process_image,
                    project,
                    img,
                    model_detector,
                    model_sam,
                    model_inpaint,
                    logger,
                ): img
                for img in todo
            }
            for fut in as_completed(futures):
                img = futures[fut]
                fut.result()
                if show_progress:
                    progress.update(task, advance=1, description=f"[green]{img['id']}")
        rep_path = summarize_batch(project.root, batch_id)
        logger.info(f"Report saved: {rep_path}")

def cli() -> None:
    """Einfaches CLI-Interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--detector", default="anime_censor_detection")
    parser.add_argument("--sam", default="sam_vit_hq")
    parser.add_argument("--inpaint", default="lama")
    args = parser.parse_args()

    run_batch(Path(args.project), args.workers, args.detector, args.sam, args.inpaint)


if __name__ == "__main__":
    cli()
