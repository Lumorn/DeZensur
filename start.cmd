@echo off
REM Startet DeZensur ueber start.py
pushd %~dp0
python start.py %*
popd
