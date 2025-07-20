"""Ein kleiner HTTP-Server mit Dummy-Endpunkten."""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

# Läuft ein Batch-Prozess im Hintergrund
_tasks: dict[str, threading.Thread] = {}


@app.post("/detect")
def detect():
    """Ruft die Zensurerkennung auf."""
    data = request.get_json()
    img_path = Path(data.get("path", ""))
    from core.censor_detector import detect_censor

    boxes = detect_censor(img_path)
    return jsonify({"boxes": boxes})


@app.post("/segment")
def segment():
    """Erzeugt eine Maske aus übergebenen Box-Prompts."""
    data = request.get_json()
    project = Path(data.get("project", ""))
    img_id = data.get("img_id", "")
    boxes = data.get("boxes", [])

    from core.segmenter import generate_mask, save_mask_png

    img_path = project / "originals" / f"{img_id}.png"
    mask_path = project / "masks" / f"{img_id}_mask.png"
    prompts = [{"type": "box", "data": b} for b in boxes]
    mask = generate_mask(img_path, prompts)
    save_mask_png(mask, mask_path)
    return jsonify({"mask": str(mask_path)})


@app.post("/inpaint")
def inpaint_route():
    """Führt das Inpainting für ein Projektbild aus."""
    data = request.get_json()
    project = Path(data.get("project", ""))
    img_id = data.get("img_id", "")
    model = data.get("model", "revanimated")
    prompt = data.get("prompt") or ""

    labels = []
    detect_json = project / "logs" / f"{img_id}_detect.json"
    if detect_json.exists():
        try:
            labels = [b.get("label") for b in json.load(detect_json.open())]
        except Exception:
            labels = []

    img_path = project / "originals" / f"{img_id}.png"
    mask_path = project / "masks" / f"{img_id}_mask.png"

    from core.inpainter import inpaint

    result = inpaint(img_path, mask_path, labels=labels, model_key=model, user_prompt=prompt)
    return jsonify({"result": str(result)})


@app.post("/batch")
def batch_route():
    """Startet den Batch-Runner im Hintergrund."""
    data = request.get_json()
    project = Path(data.get("project", ""))
    from core.batch_runner import run_batch

    params = {
        "max_workers": data.get("workers"),
        "model_detector": data.get("detector", "anime_censor_detection"),
        "model_sam": data.get("sam", "sam_vit_hq"),
        "model_inpaint": data.get("inpaint", "lama"),
        "batch_user_prompt": data.get("prompt", ""),
    }
    task_id = str(int(time.time() * 1000))
    thread = threading.Thread(
        target=run_batch, args=(project,), kwargs=params, daemon=True
    )
    _tasks[task_id] = thread
    thread.start()
    return jsonify({"task": task_id})


def run() -> None:
    app.run(port=8787)


if __name__ == "__main__":
    run()
