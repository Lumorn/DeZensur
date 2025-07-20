import importlib
from unittest import mock

repair_gui = importlib.import_module("scripts.repair_gui")


def test_repair_gui_build(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(repair_gui, "repo_root", tmp_path)
    (tmp_path / "gui").mkdir()
    with mock.patch("scripts.repair_gui.ensure_gui_build") as m_build:
        repair_gui.main()
        m_build.assert_called_once_with(force=True)
    out = capsys.readouterr().out
    assert "Frontend-Build" in out
