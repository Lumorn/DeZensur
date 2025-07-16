"""Tests für den Dependency-Manager."""

from pathlib import Path
from unittest import mock

import hashlib
import sys

from tests import requests_stub
import types

sys.modules['requests'] = requests_stub
torch_stub = types.SimpleNamespace(cuda=types.SimpleNamespace(is_available=lambda: False))
sys.modules['torch'] = torch_stub
hub_stub = types.SimpleNamespace(
    hf_hub_download=lambda *a, **k: None,
    hf_hub_url=lambda *a, **k: "",
    snapshot_download=lambda *a, **k: None,
)
sys.modules['huggingface_hub'] = hub_stub
tqdm_stub = types.SimpleNamespace(tqdm=lambda *a, **k: types.SimpleNamespace(update=lambda n=None: None, close=lambda: None))
sys.modules['tqdm'] = tqdm_stub

from core import dep_manager


def test_gpu_check() -> None:
    assert isinstance(dep_manager.is_gpu_available(), bool)


def test_verify_checksum(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_text("hello")
    sha = hashlib.sha256(b"hello").hexdigest()
    assert dep_manager.verify_checksum(f, sha)
    assert not dep_manager.verify_checksum(f, "0" * 64)


def test_ensure_missing_model(tmp_path: Path) -> None:
    name = "dummy"
    dep_manager.MODEL_REGISTRY[name] = {
        "repo": "some/repo",
        "filename": "model.bin",
        "sha256": None,
        "device": "cpu",
    }

    def fake_download(**kwargs):
        cache = tmp_path / "cache"
        cache.mkdir(parents=True, exist_ok=True)
        path = cache / "model.bin"
        path.write_text("data")
        return str(path)

    with mock.patch.object(dep_manager, "hf_hub_download", side_effect=fake_download):
        with mock.patch.object(dep_manager, "MODELS_DIR", tmp_path):
            p = dep_manager.ensure_model(name)
            assert p.exists()


def test_ensure_model_returns_path(monkeypatch, tmp_path: Path) -> None:
    """Stellt sicher, dass ein Modellpfad geliefert wird."""

    def fake_download(*a, **k):
        dest = tmp_path / "cache" / "model.safetensors"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("data")
        return str(dest)

    monkeypatch.setattr(dep_manager, "hf_hub_download", fake_download)
    monkeypatch.setattr(dep_manager, "MODELS_DIR", tmp_path)

    p = dep_manager.ensure_model("sam_vit_hq")
    assert p.exists()


def test_snapshot_fallback(monkeypatch, tmp_path: Path) -> None:
    """Überprüft die Snapshot-Suche für unbekannte Dateinamen."""

    # HEAD-Anfrage liefert immer 404
    class FakeHead:
        status_code = 404
        ok = False
        headers: dict = {}

        def raise_for_status(self) -> None:
            raise Exception("404")

    monkeypatch.setattr(dep_manager.requests, "head", lambda *a, **k: FakeHead())

    # Direkter Download schlägt fehl
    monkeypatch.setattr(
        dep_manager,
        "hf_hub_download",
        lambda *a, **k: (_ for _ in ()).throw(Exception("404")),
    )

    # Snapshot enthält die erwartete Datei
    def fake_snapshot(repo_id: str, cache_dir: Path, **kwargs) -> str:
        snap = tmp_path / "snap"
        snap.mkdir()
        f = snap / "sam_vit_hq.pth"
        f.write_text("x")
        return str(snap)

    monkeypatch.setattr(dep_manager, "snapshot_download", fake_snapshot)
    monkeypatch.setattr(dep_manager, "MODELS_DIR", tmp_path)

    p = dep_manager.download_model("sam_vit_hq", progress=False)
    assert p.exists()


def test_download_with_token(monkeypatch, tmp_path: Path) -> None:
    """Stellt sicher, dass ein gesetztes Token an Hugging Face übergeben wird."""

    class FakeHead:
        ok = True
        status_code = 200
        headers = {"content-length": "1"}

    monkeypatch.setattr(dep_manager.requests, "head", lambda *a, **k: FakeHead())

    captured = {}

    def fake_hub_download(**kwargs) -> str:
        captured["token"] = kwargs.get("token")
        dest = tmp_path / "m.pth"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("x")
        return str(dest)

    monkeypatch.setattr(dep_manager, "hf_hub_download", fake_hub_download)
    monkeypatch.setattr(dep_manager, "MODELS_DIR", tmp_path)
    monkeypatch.setenv("HUGGINGFACE_HUB_TOKEN", "secret")

    p = dep_manager.download_model("sam_vit_hq", progress=False)
    assert p.exists()
    assert captured["token"] == "secret"

