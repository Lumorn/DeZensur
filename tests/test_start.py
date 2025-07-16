import importlib
from unittest import mock
import pytest

start = importlib.import_module('start')


def test_check_npm_missing(capsys):
    with mock.patch('shutil.which', return_value=None), \
         mock.patch('tkinter.Tk'), \
         mock.patch('tkinter.messagebox.showerror') as m_err, \
         pytest.raises(SystemExit):
        start.check_npm()
    out = capsys.readouterr().out
    assert "Node.js bzw. npm wurde nicht gefunden" in out
    m_err.assert_called_once()
