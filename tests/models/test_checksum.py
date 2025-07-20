import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tests import requests_stub

sys.modules["requests"] = requests_stub
sys.modules["torch"] = types.SimpleNamespace(
    cuda=types.SimpleNamespace(is_available=lambda: False)
)
sys.modules["huggingface_hub"] = types.SimpleNamespace(
    hf_hub_download=lambda *a, **k: None,
    hf_hub_url=lambda *a, **k: "",
    list_repo_files=lambda *a, **k: [],
    snapshot_download=lambda *a, **k: None,
)
sys.modules["tqdm"] = types.SimpleNamespace(
    tqdm=lambda *a, **k: types.SimpleNamespace(
        update=lambda n=None: None, close=lambda: None
    )
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import core.dep_manager as dep_manager


def test_apply_yaml_overrides(tmp_path: Path) -> None:
    dep_manager.MODEL_REGISTRY["dummy"] = {
        "repo": "r",
        "filename": "f",
        "sha256": None,
        "device": "cpu",
    }
    yaml_file = tmp_path / "models.yml"
    yaml_file.write_text("dummy:\n  filename: new.bin\n  sha256: 1234")
    dep_manager.apply_yaml_overrides(yaml_file)
    entry = dep_manager.MODEL_REGISTRY["dummy"]
    assert entry["filename"] == "new.bin"
    assert str(entry["sha256"]) == "1234"
