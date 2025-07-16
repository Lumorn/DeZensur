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
