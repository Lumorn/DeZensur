# CHANGELOG

Alle Änderungen werden in diesem Dokument festgehalten.

## [0.1.0] – 2025-07-16
### Hinzugefügt
- Initiales Projektgerüst (`gui/`, `core/`, `models/`, `tests/`)
- Bootstrap-Skript `start.py` mit Git-Self-Update & Dependency-Installer
- Vollständige README und CHANGELOG-Struktur

## [0.3.0] – 2025-07-16
### Hinzugefügt
- Electron-/React-Skeleton mit Projektverwaltung
- Python-Projektmanager und Bildlader
- Stub-Server mit Endpunkten `/detect`, `/segment`, `/inpaint`
- Aktualisiertes `start.py` zum Starten der GUI
- Neue Tests für Projektmanager und Server

## [0.4.0] – 2025-07-16
### Hinzugefügt
- Dependency-Manager lädt Modelle automatisch herunter und prüft deren Integrität

## [0.5.0] – 2025-07-16
### Hinzugefügt
- Modul 3: core/censor_detector.py (ONNX-Wrapper für anime_censor_detection)
- CLI `python -m core.censor_detector`
- NumPy-basierte NMS-Logik

## [0.6.0] – 2025-07-16
### Hinzugefügt
- Modul 4: core/segmenter.py (HQ-SAM & MobileSAM Integration)

## [0.7.0] – 2025-07-16
### Hinzugefügt
- Mask-Editor in der GUI zum manuellen Bearbeiten von Masken (Konva)

## [0.8.0] – 2025-07-16
### Hinzugefügt
- Modul 6: core/inpainter.py (LaMa + Stable-Diffusion-Inpainting)
- Neuer /inpaint-Endpunkt und GUI-Einstellung zur Modellauswahl

## [0.9.0] – 2025-07-16
### Hinzugefügt
- Modul 7: core/batch_runner.py, Rich-Progress, Thread-Pool
- Neuer /batch-Endpunkt im Stub-Server

## [1.0.0] – 2025-07-17
### Hinzugefügt
- Modul 8: JSON-Logging mit Loguru, Batch-Report-Generator
- CLI-Werkzeug `python -m core.report`

## [1.1.0] – 2025-07-17
### Geändert
- `start.py` aktualisiert nun zuerst das Repository und installiert danach die
  Python-Abhängigkeiten.
- Automatisches `npm install` in `gui/`, wenn `package.json` neuer ist oder
  `node_modules` fehlt.
### Hinzugefügt
- Modul 9: PyTest-Suite, Coverage-Threshold 80 %, GitHub Actions CI

## [1.2.0] – 2025-07-18
### Hinzugefügt
- Automatischer Prompt-Builder mit Genital-Tags
- GUI-Option „Automatische Anatomie-Tags“
- Speichert verwendetes Prompt als `prompt.txt`
### Geändert
- ersetze Paketnamen 'lama-cleaner' → 'iopaint[lama]' (PyPI-konform)

## [1.3.0] – 2025-07-19
### Hinzugefügt
- GitHub Actions Workflow mit Format- und Testlauf

## [1.3.1] – 2025-07-20
### Geändert
- README: Projektordner heißt nun `DeZensur/`
- CI-Badge verweist auf korrektes GitHub-Repository

## [1.3.2] – 2025-07-21
### Geändert
- `iopaint[lama]` ist nun auf Version 1.2.5 festgeschrieben
### Hinzugefügt
- Hinweis zur festen Version in der README

## [1.3.3] – 2025-07-22
### Geändert
- `requirements.txt` beschränkt `torch` jetzt auf Version 2.1.x
### Hinzugefügt
- Info zur Torch-Begrenzung in der README

## [1.4.0] – 2025-07-23
### Hinzugefügt
- CI-Workflow prüft jetzt flake8 und startet auch die Jest-Tests im GUI-Ordner
- Neues `npm`-Script `test` für Jest
### Geändert
- README erwähnt den automatischen CI-Lauf

## [1.4.1] – 2025-07-24
### Behoben
- `start.py` fügt nun das Projektverzeichnis dem `PYTHONPATH` hinzu, sodass der
  Import von `core` zuverlässig funktioniert.

## [1.4.2] – 2025-07-25
### Hinzugefügt
- `start.py` klont das Repository automatisch, wenn nur diese Datei vorliegt.

## [1.4.3] – 2025-07-26
### Behoben
- `start.py` importiert interne Module erst nach erfolgreicher Installation der
  Abhängigkeiten. Damit verhindert der Erststart fehlende Pakete wie
  `onnxruntime`.

## [1.4.4] – 2025-07-27
### Geändert
- `start.py` haelt das Terminal nun auch bei Fehlern offen und gibt den
  Stacktrace aus. So koennen Anwender die Fehlermeldung in Ruhe lesen.

## [1.4.5] – 2025-07-28
### Geändert
- `pytest.ini` verzichtet auf Coverage-Optionen, sodass die Tests auch ohne
  zusätzliche Plugins laufen.
### Hinzugefügt
- Anleitung zum lokalen Testlauf in der README.

## [1.4.6] – 2025-07-29
### Geändert
- `start.py` prüft nun, ob das Repository aktuell ist und führt bei Bedarf
  automatisch `git pull` aus.
### Geändert
- README entsprechend angepasst.

## [1.4.7] – 2025-07-30
### Geändert
- `requirements.txt` setzt nun `torch` auf Version 2.2.x, da 2.1.x keine
  Python‑3.12-Builds bietet.
- README entsprechend angepasst.

## [1.4.8] – 2025-07-31
### Geändert
- `iopaint[lama]` ist nun auf Version 1.6.0 angehoben, um Python 3.12 zu
  unterstützen.
- README entsprechend angepasst.

## [1.4.9] – 2025-07-31
### Geändert
- `diffusers` ist nun auf Version 0.27.2 festgeschrieben, da iopaint 1.6.0
  diese Version benötigt.
- README entsprechend ergänzt.

## [1.4.10] – 2025-08-01
### Hinzugefügt
- `start.py` prüft nun, ob `npm` installiert ist und gibt einen klaren
  Fehlerhinweis aus.
- README erwähnt die notwendige Node.js-Installation.

## [1.4.11] – 2025-08-02
### Geändert
- `start.py` startet nach dem Anlegen der virtuellen Umgebung automatisch
  erneut mit dem Python der venv. Dadurch stehen neu installierte Pakete sofort
  zur Verfügung.
- README erläutert dieses Verhalten.

## [1.4.12] – 2025-08-03
### Behoben
- Unter Windows verursachte der Neustart via ``os.execv`` einen Fehler
  ``OSError: [Errno 12] Not enough space``. Das Skript nutzt dort nun
  ``subprocess`` und beendet sich anschließend.
- Hinweis in der README ergänzt.

## [1.4.13] – 2025-08-04
### Geändert
- `start.py` überprüft jetzt, ob uncommittete Änderungen vorhanden sind und
  warnt den Benutzer. Bei Änderungen wird kein automatisches `git pull`
  ausgeführt.

## [1.4.14] – 2025-08-05
### Hinzugefügt
- `start.py` zeigt nun für jeden externen Befehl einen Fortschrittsspinne im
  Terminal an. So ist klar ersichtlich, was gerade passiert.

## [1.4.15] – 2025-08-05
### Geändert
- `start.py` importiert `rich` nun erst in der Hilfsfunktion `run`. Dadurch
  startet das Skript auch dann fehlerfrei, wenn die Abhängigkeiten noch nicht
  installiert sind.

## [1.4.16] – 2025-08-05
### Geändert
- Fehlt das Paket `rich`, gibt `start.py` nun einen Hinweis aus und führt den
  Befehl ohne Fortschrittsanzeige aus.
