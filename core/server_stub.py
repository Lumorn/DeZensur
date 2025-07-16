"""Ein kleiner HTTP-Server mit Dummy-Endpunkten."""

from __future__ import annotations

import json
from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)


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
def inpaint():
    data = request.get_json()
    return jsonify({"action": "inpaint", "id": data.get("id")})


def run() -> None:
    app.run(port=8787)


if __name__ == "__main__":
    run()
