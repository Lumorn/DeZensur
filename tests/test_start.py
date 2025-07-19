import importlib
from unittest import mock

import pytest

start = importlib.import_module("start")


def test_check_npm_missing(capsys):
    with mock.patch("shutil.which", return_value=None), mock.patch(
        "tkinter.Tk"
    ), mock.patch("tkinter.messagebox.showerror") as m_err, pytest.raises(SystemExit):
        start.check_npm()
    out = capsys.readouterr().out
    assert "Node.js bzw. npm wurde nicht gefunden" in out
    m_err.assert_called_once()


def test_check_npm_outdated(capsys):
    """Prüft, ob eine zu alte Node-Version bemängelt wird."""

    fake_proc = mock.Mock(returncode=0, stdout="v16.0.0")
    with mock.patch("shutil.which", side_effect=lambda x: f"/usr/bin/{x}"), mock.patch(
        "subprocess.run", return_value=fake_proc
    ), mock.patch("tkinter.Tk"), mock.patch(
        "tkinter.messagebox.showerror"
    ) as m_err, pytest.raises(
        SystemExit
    ):
        start.check_npm()
    out = capsys.readouterr().out
    assert "zu alt" in out
    m_err.assert_called_once()


def test_check_npm_ok():
    """Stellt sicher, dass gültige Versionen akzeptiert werden."""

    fake_proc = mock.Mock(returncode=0, stdout="v18.5.0")
    with mock.patch("shutil.which", side_effect=lambda x: f"/usr/bin/{x}"), mock.patch(
        "subprocess.run", return_value=fake_proc
    ), mock.patch("tkinter.Tk"), mock.patch("tkinter.messagebox.showerror") as m_err:
        start.check_npm()
    m_err.assert_not_called()


def test_ensure_clean_worktree_autostash():
    """Prüft, ob bei aktivem auto-stash ein git stash ausgeführt wird."""

    with mock.patch(
        "subprocess.check_output", return_value=" M changed_file"
    ), mock.patch("start.run") as m_run:
        sauber, stashed = start.ensure_clean_worktree(auto_stash=True)
    m_run.assert_called_once_with(
        ["git", "stash", "--include-untracked"],
        cwd=start.project_root,
        beschreibung="git stash",
    )
    assert sauber is True
    assert stashed is True


def test_ensure_gui_build(monkeypatch, tmp_path):
    """Stellt sicher, dass die GUI bei fehlendem Build erzeugt wird."""

    monkeypatch.setattr(start, "project_root", tmp_path)
    (tmp_path / "gui").mkdir()

    with mock.patch.object(start, "run") as m_run, pytest.raises(SystemExit):
        with mock.patch("tkinter.Tk"), mock.patch("tkinter.messagebox.showerror"):
            start.ensure_gui_build()
    m_run.assert_called_once_with(
        [start.npm_cmd, "run", "build"],
        cwd="gui",
        beschreibung="npm run build",
        env=mock.ANY,
    )

    dist = tmp_path / "gui" / "dist"
    dist.mkdir(parents=True)
    (dist / "index.html").write_text("x")

    with mock.patch.object(start, "run") as m_run:
        with mock.patch("tkinter.Tk"), mock.patch("tkinter.messagebox.showerror"):
            start.ensure_gui_build()
        m_run.assert_not_called()


def test_should_skip_npm_install_ci(monkeypatch):
    monkeypatch.setenv("SKIP_NPM_INSTALL", "1")
    monkeypatch.setenv("CI", "true")
    assert start.should_skip_npm_install(["--skip-npm"]) is True


def test_should_skip_npm_install_local(monkeypatch, capsys):
    monkeypatch.setenv("SKIP_NPM_INSTALL", "1")
    monkeypatch.delenv("CI", raising=False)
    assert start.should_skip_npm_install(["--skip-npm"]) is False
    out = capsys.readouterr().out
    assert "nur in CI erlaubt" in out
