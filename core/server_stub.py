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
    data = request.get_json()
    return jsonify({"action": "segment", "id": data.get("id")})


@app.post("/inpaint")
def inpaint():
    data = request.get_json()
    return jsonify({"action": "inpaint", "id": data.get("id")})


def run() -> None:
    app.run(port=8787)


if __name__ == "__main__":
    run()
