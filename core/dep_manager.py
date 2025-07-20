"""Abhängigkeiten und Modelle verwalten."""
# mypy: ignore-errors

from __future__ import annotations

import hashlib
import json
import logging
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, cast

import requests
import torch
import yaml
from huggingface_hub import (hf_hub_download, hf_hub_url, list_repo_files,
                             snapshot_download)
from tqdm import tqdm

logger = logging.getLogger(__name__)

# Basisordner für alle Modelle
MODELS_DIR = Path("models")
VERSIONS_FILE = MODELS_DIR / "versions.json"


def _load_versions() -> dict[str, str]:
    """Lädt die gespeicherten Modellversionen."""

    if VERSIONS_FILE.exists():
        try:
            return json.loads(VERSIONS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_versions(data: dict[str, str]) -> None:
    """Schreibt die Modellversionen auf die Platte."""

    VERSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    VERSIONS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def _remote_etag(repo: str, filename: str) -> str | None:
    """Fragt das aktuelle ETag eines Modells ab."""

    url = hf_hub_url(repo, filename)
    try:
        resp = requests.head(url, allow_redirects=True, timeout=10)
        if resp.ok:
            return resp.headers.get("etag")
    except Exception as exc:  # pragma: no cover - reine Warnung
        logger.warning("Konnte ETag nicht abrufen: %s", exc)
    return None


# Registry mit bekannten Modellen und Metadaten
# "alternatives" listet alternative Dateinamen auf, falls der Hauptname nicht
# mehr vorhanden ist.
MODEL_REGISTRY: dict[str, dict[str, str | list[str] | None]] = {
    "anime_censor_detection": {
        "repo": "deepghs/anime_censor_detection",
        # aktueller Pfad innerhalb des Repos
        "filename": "censor_detect_v0.9_s/model.onnx",
        # ältere Dateinamen als Fallback
        "alternatives": [
            "censor_detect_v0.7_s.onnx",
            "censor_detect_v0.7.onnx",
            "censor_detect_v0.8.onnx",
        ],
        "sha256": None,
        "device": "cpu",
    },
    "sam_vit_hq": {
        # Repository wurde verschoben und die bereitgestellten Gewichte liegen
        # inzwischen als ``model.safetensors`` vor
        "repo": "syscv-community/sam-hq-vit-base",
        "filename": "model.safetensors",
        "alternatives": ["sam_hq_vit_b.pth", "sam_vit_hq.pth"],
        "sha256": None,
        "device": "gpu",
    },
    "sam_mobile": {
        "repo": "ChaoningZhang/MobileSAM",
        "filename": "mobile_sam.pt",
        "sha256": None,
        "device": "gpu",
    },
    "animanga_inpaint": {
        "repo": "dreMaz/AnimeMangaInpainting",
        "filename": "big-lama.zip",
        "sha256": None,
        "device": "gpu",
    },
    "iopaint_lama": {
        "repo": "advimman/lama",
        "filename": "big-lama.zip",
        "sha256": None,
        "device": "gpu",
    },
    "sd2_inpaint": {
        "repo": "stabilityai/stable-diffusion-2-inpainting",
        "filename": "model.safetensors",
        "sha256": None,
        "device": "gpu",
    },
    "revanimated_inpaint": {
        "repo": "Uminosachi/revAnimated_v121Inp-inpainting",
        "filename": "revAnimated_v121Inp-inpainting.safetensors",
        "sha256": None,
        "device": "gpu",
    },
    "sd_controlnet": {
        "repo": "stabilityai/stable-diffusion-2-inpainting",
        "filename": "model.safetensors",
        "sha256": None,
        "device": "gpu",
    },
    "controlnet_canny": {
        "repo": "lllyasviel/control_v11p_sd15_canny",
        "filename": "diffusion_pytorch_model.safetensors",
        "sha256": None,
        "device": "gpu",
    },
}

# Pfad zur optionalen YAML-Datei mit erweiterten Angaben
MODELS_YAML = Path(__file__).resolve().parent.parent / "models.yml"


def apply_yaml_overrides(yaml_path: Path = MODELS_YAML) -> None:
    """Aktualisiert die Registry anhand einer YAML-Datei."""

    if not yaml_path.exists():
        return
    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # pragma: no cover - Fehler beim Parsen
        logger.warning("models.yml konnte nicht geladen werden: %s", exc)
        return
    for key, info in data.items():
        if key in MODEL_REGISTRY and isinstance(info, dict):
            MODEL_REGISTRY[key].update(info)


# YAML-Overrides direkt beim Import anwenden
apply_yaml_overrides()


def is_gpu_available() -> bool:
    """Prüft, ob eine GPU gewünscht und verfügbar ist."""

    override = os.environ.get("DEZENSUR_DEVICE")
    if override:
        return override.lower() == "gpu"
    return torch.cuda.is_available()


def verify_checksum(path: Path, sha256: str) -> bool:
    """Vergleicht die SHA-256-Prüfsumme einer Datei."""

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest() == sha256.lower()


def _parallel_download(url: str, dest: Path, size: int, progress: bool) -> None:
    """Lädt eine große Datei mittels vier Threads herunter."""

    chunk_size = size // 4
    ranges = []
    for i in range(4):
        start = i * chunk_size
        end = start + chunk_size - 1 if i < 3 else size - 1
        ranges.append((start, end))

    tmp_files = [dest.with_suffix(dest.suffix + f".part{i}") for i in range(4)]

    bar = tqdm(
        total=size, disable=not progress, unit="B", unit_scale=True, desc=dest.name
    )

    def worker(rng: tuple[int, int], out_file: Path) -> None:
        headers = {"Range": f"bytes={rng[0]}-{rng[1]}"}
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with out_file.open("wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

    with ThreadPoolExecutor(max_workers=4) as exe:
        futures = [exe.submit(worker, r, t) for r, t in zip(ranges, tmp_files)]
        for f in futures:
            f.result()

    bar.close()

    with dest.open("wb") as final:
        for part in tmp_files:
            with part.open("rb") as src:
                shutil.copyfileobj(src, final)
            os.remove(part)


def download_model(name: str, progress: bool = True) -> Path:
    """Lädt das angegebene Modell über den Hugging-Face-Hub."""

    info = MODEL_REGISTRY[name]
    repo = info["repo"]
    filename = cast(str, info["filename"])
    token = os.environ.get("HUGGINGFACE_HUB_TOKEN") or os.environ.get("HF_TOKEN")
    alternatives = cast(list[str], info.get("alternatives", []) or [])
    models_dir = MODELS_DIR / name
    models_dir.mkdir(parents=True, exist_ok=True)
    dest = models_dir / filename
    dest.parent.mkdir(parents=True, exist_ok=True)

    candidates = [filename, *alternatives]
    if name == "anime_censor_detection":
        try:
            files = list_repo_files(repo_id=repo, token=token)
            subdirs = sorted(
                {p.split("/")[0] for p in files if p.startswith("censor_detect_v")},
                reverse=True,
            )
            if subdirs:
                candidates.insert(0, f"{subdirs[0]}/model.onnx")
        except Exception as exc:  # pragma: no cover - nur Warnung
            logger.warning("Konnte Unterordner nicht ermitteln: %s", exc)
    last_exc: Exception | None = None
    for fname in candidates:
        url = hf_hub_url(repo, fname)
        size = 0
        status = None
        try:
            head = requests.head(url, allow_redirects=True, timeout=10)
            status = head.status_code
            if head.ok and head.headers.get("content-length"):
                size = int(head.headers["content-length"])
            if not head.ok:
                raise requests.HTTPError(f"HTTP {head.status_code}")
        except Exception as exc:  # pragma: no cover - reine Warnung
            last_exc = exc
            logger.warning("Konnte Dateigröße nicht bestimmen: %s", exc)
            if status == 404:
                continue
        try:
            if size > 500 * 1024 * 1024:
                _parallel_download(url, dest, size, progress)
            else:
                try:
                    path = hf_hub_download(
                        repo_id=repo,
                        filename=fname,
                        cache_dir=models_dir,
                        resume_download=True,
                        progress_bar=False,
                        token=token,
                    )
                except TypeError:
                    # Ältere huggingface_hub-Versionen kennen das Argument
                    # ``progress_bar`` nicht.
                    path = hf_hub_download(
                        repo_id=repo,
                        filename=fname,
                        cache_dir=models_dir,
                        resume_download=True,
                        token=token,
                    )
                shutil.copy(Path(path), dest)
            break
        except Exception as exc:
            last_exc = exc
            logger.warning("Download von %s fehlgeschlagen: %s", fname, exc)
            continue
    else:
        logger.warning(
            "Keiner der bekannten Dateinamen funktionierte, versuche Snapshot"
        )
        try:
            snap = snapshot_download(repo_id=repo, cache_dir=models_dir, token=token)
        except Exception as exc:  # pragma: no cover - reiner Fehlerpfad
            raise RuntimeError(f"Download für {name} fehlgeschlagen: {exc}") from exc

        found: Path | None = None
        for cand in candidates:
            matches = list(Path(snap).rglob(cand))
            if matches:
                found = matches[0]
                break
        if not found:
            raise RuntimeError(
                f"Im Snapshot von {repo} wurde keine der Dateien {candidates} gefunden"
            )
        shutil.copy(found, dest)

    sha256 = info.get("sha256")
    if sha256 and not verify_checksum(dest, sha256):
        raise ValueError(f"Checksumme stimmt nicht für {name}")
    if sha256 is None:
        logger.warning("Keine Prüfsumme für %s hinterlegt", name)
    return dest


def ensure_model(name: str, prefer_gpu: bool = True) -> Path:
    """Sorgt dafür, dass ein Modell vorhanden und valide ist."""

    info = MODEL_REGISTRY[name]
    target = MODELS_DIR / name / info["filename"]
    versions = _load_versions()
    remote = _remote_etag(info["repo"], info["filename"])
    local_ver = versions.get(name)
    if target.exists() and local_ver == remote:
        if info.get("sha256") and not verify_checksum(target, info["sha256"]):
            logger.warning("Checksumme für %s fehlerhaft, lade neu", name)
            target.unlink()
        else:
            return target

    if info.get("device") == "gpu" and prefer_gpu and not is_gpu_available():
        logger.warning(
            "GPU nicht verfügbar. Das Modell %s wird auf der CPU benutzt.",
            name,
        )

    path = download_model(name)
    if remote:
        versions[name] = remote
        _save_versions(versions)
    return path


def list_installed() -> dict[str, Path]:
    """Listet installierte Modelle auf."""

    result: dict[str, Path] = {}
    for k, v in MODEL_REGISTRY.items():
        path = MODELS_DIR / k / v["filename"]
        if path.exists():
            result[k] = path
    return result
