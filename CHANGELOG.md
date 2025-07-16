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
