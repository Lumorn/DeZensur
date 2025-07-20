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

## [1.4.17] – 2025-08-06
### Hinzugefügt
- Neues Skript `generate_report.py`, das die CLI `python -m core.report` aufruft
  und einen Zielpfad für den Report entgegen nimmt.

## [1.4.18] – 2025-08-06
### Behoben
- `start.py` konnte in seltenen Fällen unendlich viele Python-Prozesse starten,
  wenn der Wechsel in die virtuelle Umgebung scheiterte. Eine Umgebungsvariable
  verhindert nun diese Neustart-Schleife.

## [1.4.19] – 2025-08-07
### Geändert
- `start.py` gibt nun auch im Terminal einen Hinweis aus, wenn `npm` fehlt. So
  ist der Grund eines Abbruchs besser erkennbar.

## [1.4.20] – 2025-08-08
### Behoben
- Kompatibilitätsproblem mit älteren ``huggingface_hub``-Versionen: Das
  ``progress_bar``-Argument wird nun optional behandelt.
### Geändert
- README um Hinweis zur geänderten Downloadfunktion ergänzt.

## [1.4.21] – 2025-08-09
### Behoben
- ``dep_manager.download_model`` versucht nun alternative Dateinamen, falls der
  ursprüngliche Modellname nicht verfügbar ist.
### Geändert
- README weist auf diese Fallback-Strategie hin.

## [1.4.22] – 2025-08-10
### Behoben
- Fehlende Modelle werden nun über einen Repository-Snapshot gesucht, wenn alle
  bekannten Dateinamen einen 404-Fehler liefern.
### Geändert
- README erläutert den neuen Snapshot-Fallback.

## [1.4.23] – 2025-08-11
### Behoben
- Snapshot-Fallback durchsucht nun alle bekannten Dateinamen und findet so auch
  ``.pth``-Modelle wie ``sam_vit_hq``.
### Geändert
- README weist auf die erweiterte Suche hin und das SAM-HQ-Repository wird in
  Kleinschreibung referenziert.

## [1.4.24] – 2025-08-12
### Behoben
- ``dep_manager.download_model`` übergibt jetzt das in ``HUGGINGFACE_HUB_TOKEN``
  hinterlegte Zugangstoken an Hugging Face.
### Geändert
- README beschreibt die Token-Variable.

## [1.4.25] – 2025-08-13
### Behoben
- HQ-SAM wird jetzt aus ``syscv-community/sam-hq-vit-base`` geladen und nutzt
  die Datei ``sam_hq_vit_b.pth``. ``sam_vit_hq.pth`` bleibt als Fallback
  erhalten.
### Geändert
- README vermerkt den neuen Modellpfad.

## [1.4.26] – 2025-08-14
### Behoben
- Das HQ-SAM-Modell nutzt nun die Datei ``model.safetensors``. ``sam_hq_vit_b.pth``
  und ``sam_vit_hq.pth`` bleiben als Fallback erhalten.
### Geändert
- README weist auf den neuen Dateinamen hin.

## [1.4.27] – 2025-08-15
### Geändert
- ``dep_manager.download_model`` ermittelt nun automatisch den neuesten
  Unterordner von ``anime_censor_detection``. Dadurch funktionieren zukünftige
  Versionen ohne Codeanpassung.
### Hinzugefügt
- Stub ``list_repo_files`` und aktualisierte Tests.

## [1.4.28] – 2025-08-16
### Hinzugefügt
- ``start.py`` prüft jetzt die installierte Node-Version und bricht bei Version
  unter 18 mit einer Fehlermeldung ab.
### Geändert
- README erwähnt die Mindestanforderung für Node.js.

## [1.4.29] – 2025-08-17
### Behoben
- Platzhalter in Log-Ausgaben werden nun korrekt mit ``{}`` formatiert.
### Geändert
- README weist auf die ``{}``-Syntax bei Loguru hin.

## [1.4.30] – 2025-08-18
### Hinzugefügt
- ``start.py`` erkennt ``npm`` jetzt auch über die Umgebungsvariable ``NPM_PATH``.
### Geändert
- README beschreibt die neue Variable zum Setzen des ``npm``-Pfads.

## [1.4.31] – 2025-08-19
### Behoben
- ``electron-reload`` wird wieder in Version ``2.0.0`` installiert, da ``2.0.2``
  nicht verfügbar ist.
### Geändert
- README verweist auf die angepasste Abhängigkeit.

## [1.4.32] – 2025-08-20
### Behoben
- Fehlerhafte Version ``2.0.2`` von ``electron-reload`` entfernt und auf ``2.0.0``
  zurückgesetzt.
### Geändert
- README entsprechend angepasst.

## [1.4.33] – 2025-08-21
### Geändert
- `start.py` gibt nun einen Hinweis aus, wenn `npm install` wegen fehlender
  Pakete wie `electron-reload` scheitert.
### Geändert
- README um diese Info erweitert.

## [1.4.34] – 2025-08-22
### Geändert
- `electron-reload` wird jetzt in Version ``2.0.1`` installiert, da 2.0.0 und
  2.0.2 zu Problemen führten.
### Geändert
- README entsprechend angepasst.

## [1.4.35] – 2025-08-23
### Behoben
- Die Version ``2.0.1`` von ``electron-reload`` existiert nicht im NPM-Registry.
  Das Paket wird daher wieder in Version ``2.0.0`` verwendet.
### Geändert
- README und ``package.json`` entsprechend angepasst.

## [1.4.36] – 2025-08-24
### Hinzugefügt
- ``start.py`` bietet mit ``SKIP_NPM_INSTALL`` bzw. ``--skip-npm`` die Möglichkeit,
  den `npm install`-Schritt zu überspringen.
### Geändert
- README beschreibt die neue Option.

## [1.4.37] – 2025-08-25
### Geändert
- ``electron-reload`` wird nun in Version ``2.0.2`` verwendet,
  weil ``2.0.0`` nicht mehr in der Registry verfügbar ist.
- README und ``package.json`` wurden entsprechend angepasst.


## [1.4.38] – 2025-08-26
### Behoben
- `electron-reload` 2.0.2 ist aus der Registry verschwunden. Die GUI nutzt wieder die stabile Version 1.6.0.
### Geändert
- README und `package.json` entsprechend angepasst.

## [1.4.39] – 2025-08-27
### Behoben
- Version 1.6.0 von `electron-reload` ist im npm-Registry nicht vorhanden. Wir verwenden nun Version 1.5.0.
### Geändert
- README und `package.json` wurden entsprechend angepasst.

## [1.4.40] – 2025-08-28
### Behoben
- Die Abhängigkeit `react-konva` zeigte auf eine nicht existierende Version 19.0.24.
  Jetzt verwenden wir Version 19.0.7 und passen `konva` auf 9.3.3 an.
### Geändert
- README und `package.json` führen die korrigierte Version auf.

## [1.4.41] – 2025-08-29
### Behoben
- `preload.js` verwendet jetzt CommonJS, damit Electron das Skript korrekt lädt.
### Geändert
- README erwähnt das CommonJS-Format des Preload-Skripts.

## [1.4.42] – 2025-08-30
### Geändert
- `index.html` definiert nun eine Content-Security-Policy, wodurch die Electron-Warnung zu unsicheren Skripten verschwindet.
### Geändert
- README weist auf die neue Content-Security-Policy hin.

## [1.4.43] – 2025-08-31
### Hinzugefügt
- `start.py` ruft nach einem erfolgreichen `npm install` automatisch `npm audit` auf und meldet eventuelle Probleme.
### Geändert
- README beschreibt die neue Sicherheitsprüfung.

## [1.4.44] – 2025-09-01
### Behoben
- `vite.config.js` setzt nun den Basis-Pfad auf `./`, damit die gebaute GUI ihre Assets korrekt findet.
### Geändert
- README weist auf die neue `base`-Einstellung hin.

## [1.4.45] – 2025-09-02
### Geändert
- `start.py` prüft das Git-Repository nun direkt beim Start und führt ggf. ein Update durch, bevor weitere Schritte erfolgen.
- README beschreibt diese Änderung.

## [1.4.46] – 2025-09-03
### Hinzugefügt
- Option `--auto-stash` in `start.py`, die ungesicherte Änderungen automatisch vor dem `git pull` stasht und anschließend wieder einspielt.
### Geändert
- README erläutert die neue Option.

## [1.4.47] – 2025-09-04
### Behoben
- `start.py` baut die GUI nun automatisch, wenn `gui/dist` fehlt. Dadurch wird die Oberfläche korrekt angezeigt.

## [1.4.48] – 2025-09-05
### Behoben
- Unter Windows schlug der Electron-Build fehl, wenn keine Symlink-Rechte vorhanden waren. `start.py` setzt nun `CSC_IDENTITY_AUTO_DISCOVERY=false`, damit kein Codesigning stattfindet.
### Geändert
- README beschreibt diese neue Umgebungsvariable.

## [1.4.49] – 2025-09-06
### Hinzugefügt
- `start.py` startet unter Windows automatisch mit Administratorrechten neu,
  wenn Symlink-Rechte fehlen.
### Geändert
- README dokumentiert dieses Verhalten.

## [1.4.50] – 2025-09-07
### Behoben
- Beim Aufruf von `npm start` erschien nur ein leeres Fenster, falls kein
  Vite-Server lief. `gui/electron/main.js` prüft nun, ob der Server erreichbar
  ist und zeigt andernfalls die gebaute Oberfläche oder einen Hinweis an.
### Geändert
- README erklärt den Unterschied zwischen `npm run dev` und `npm start`.

## [1.4.51] – 2025-09-08
### Behoben
- "Bilder hinzufügen" löst jetzt einen Hinweis aus, wenn noch kein Projekt
  geöffnet ist. Dadurch verhindert die GUI einen Absturz.
### Geändert
- README um Hinweis auf die neue Fehlermeldung ergänzt.

## [1.5.0] – 2025-09-09
### Hinzugefügt
- Neues Desktop-Layout in der React-GUI mit Titelleiste,
  Befehlsleiste und Seitenleisten.
- Tailwind-Konfiguration enthält nun Farbtokens für das Dark-Theme.

## [1.5.1] – 2025-09-10
### Hinzugefügt
- Ordner `mockups/` mit zwei HTML-Dateien als Vorschau auf die
  Desktop-Oberfläche (Front und Backstage).
- README beschreibt, wie die Mockups genutzt werden können.


## [1.6.0] – 2025-09-11
### Hinzugefügt
- Neues TypeScript-Frontend mit TanStack Router und Zustand-Stores.
- Playwright-Smoke-Test und electron-trpc IPC-Gerüst.

## [1.7.0] – 2025-09-12
### Hinzugefügt
- IPC-Kommunikation nutzt jetzt **electron-trpc** mit Typsicherheit.
- Preload und Renderer binden die IPC-Routen automatisch ein.

## [1.7.1] – 2025-09-13
### Geändert
- Da Version 0.12.0 noch nicht veröffentlicht ist, nutzt die GUI `electron-trpc` jetzt fest Version 0.11.x.

## [1.7.2] – 2025-09-14
### Geändert
- Das Startskript erwähnt bei einem fehlgeschlagenen `npm install` nun `electron-trpc` statt `electron-reload`.

## [1.7.3] – 2025-09-15
### Behoben
- Das GUI-Build schlug wegen einer nicht vorhandenen Version von `electron-trpc` fehl. Die Abhängigkeit ist nun auf ^0.7.1 begrenzt.
### Geändert
- README und `package.json` weisen auf die korrigierte Version hin.
## [1.7.4] - 2025-09-16
### Geändert
- Electron deaktiviert jetzt das Autofill-Feature, um DevTools-Fehler zu vermeiden.

## [1.7.5] - 2025-09-17
### Hinzugefügt
- `start.py` prüft nach `npm run build`, ob `gui/dist/index.html` vorhanden ist.
  Fehlt die Datei, erscheint eine Fehlermeldung.

## [1.7.6] - 2025-09-18
### Behoben
- `vite.config.ts` enthält nun ebenfalls den Basis-Pfad `./`, womit Electron die
  gebauten Assets fehlerfrei lädt.

## [1.7.7] - 2025-07-17
### Hinzugefügt
- "Add Images" Dialog inklusive Galerie-Grid und Auswahlfunktion

## [1.7.8] - 2025-09-19
### Hinzugefügt
- Fenstersteuerung über die Knöpfe der Titelleiste
- Projektbefehle (Neu, Öffnen, Bilder, Batch, Export) in der CommandBar
- AppBar mit Settings-Overlay, GPU-Umschalter und Ordnerauswahl
- Start-Button führt die Zensurerkennung für das gewählte Bild aus
### Geändert
- README erwähnt die neuen Button-Funktionen

## [1.7.9] - 2025-09-20
### Geändert
- Ordnerauswahl legt jetzt den Arbeitsordner im Zustand ab.
- Start-Button nutzt den tRPC-Endpunkt `censorDetect`.
- README beschreibt die beiden neuen Funktionen.

## [1.8.0] - 2025-09-21
### Hinzugefügt
- HTML-Export im Batch-Report (`core.report.render_html` und `generate_report.py --html`)
- README führt das neue Kommando unter "Batch-Reports erstellen" auf

## [1.8.1] - 2025-09-22
### Hinzugefügt
- Einfaches CLI `dez.py` mit Befehl `detect`
- Testskript unter `tests/cli/test_help.py`
### Geändert
- README beschreibt den neuen CLI-Aufruf und hakt das TODO ab

## [1.8.2] - 2025-09-23
### Hinzugefügt
- Neuer CLI-Befehl `inpaint` zum Bearbeiten einzelner Bilder
- Test `tests/cli/test_inpaint_cli.py`
### Geändert
- README ergänzt CLI-Beispiel und hakt das TODO ab

## [1.8.3] - 2025-09-24
### Hinzugefügt
- Neues Modul `core.project` mit Schema-Version 2 und automatischer Migration
- Test `tests/core/test_project_roundtrip.py`
### Geändert
- README erklärt die Migration und hakt das TODO-Board ab

## [1.8.4] - 2025-09-25
### Hinzugefügt
- `detect_censor` unterstützt nun ein optionales ROI-Argument
  und die CLI kennt `--roi`
- Beispiel in der README angepasst
- Neue Tests für die ROI-Filterung
### Geändert
- TODO-Liste im README aktualisiert

## [1.8.5] - 2025-09-26
### Hinzugefügt
- Alias `detect-batch` für die CLI
- Test `tests/cli/test_detect_batch_cli.py`
- Test `tests/detector/test_thresholds.py`
### Geändert
- README um den neuen Befehl ergänzt und TODOs aktualisiert

## [1.8.6] - 2025-09-27
### Hinzugefügt
- Versionsprüfung im Dependency-Manager (`core.dep_manager`)
- Neuer Test `tests/test_dep_manager.py::test_version_update`
### Geändert
- README hakt den Punkt "Dynamischer Model-Manager" ab

## [1.8.7] - 2025-09-28
### Hinzugefügt
- Automatischer Fallback auf **MobileSAM** bei fehlender GPU
- Neuer Test `tests/test_segmenter_mobile_fallback.py`
### Geändert
- TODO-Board markiert den MobileSAM-Fallback als erledigt

## [1.8.8] - 2025-09-29
### Hinzugefügt
- Neuer Test `tests/test_segmenter_gpu_pipeline.py`
### Geändert
- README hakt die SAM-HQ GPU-Pipeline und den Lama-Fallback ab

## [1.8.9] - 2025-09-30
### Hinzugefügt
- Einfache i18n-Unterstützung mit `de` und `en` JSON-Bundles
- Zustands-Store zur Laufzeitumschaltung der Sprache
- Neuer Test `tests/i18n/test_loader.py`
### Geändert
- README erklärt den Sprachwechsel und markiert das TODO als erledigt

## [1.8.10] - 2025-10-01
### Hinzugefügt
- CLI-Skript `python -m dezensor.fetch_model` zum manuellen Herunterladen von Modellen
- Test `tests/test_fetch_model_cli.py`
### Geändert
- README beschreibt das Skript und hakt den Punkt "Modelle nachladen" ab

## [1.8.11] - 2025-10-02
### Hinzugefügt
- Unit-Test `gui/src/__tests__/settings.spec.tsx` und Wrapper `tests/test_settings_modal.py`
### Geändert
- README hakt den TODO-Eintrag fr den Settings-Test ab

## [1.8.12] - 2025-10-03
### Hinzugefügt
- Erste Version des Benutzerhandbuchs unter `docs/handbuch.md`
### Geändert
- README verweist auf das Handbuch und markiert den Punkt im TODO-Board als erledigt

## [1.8.13] - 2025-10-04
### Hinzugefügt
- Fortschritts-Modal zeigt den Status laufender Aufgaben in der GUI.
### Geändert
- README hakt den Punkt "Fortschritts-Modal" ab.


## [1.8.14] - 2025-10-05
### Hinzugefügt
- ControlNet-Unterstützung im Inpainter (`sd_controlnet`)
- Unit-Test `tests/inpaint/test_seams.py`
### Geändert
- README ergänzt das ControlNet-Modell und markiert TODOs als erledigt

## [1.8.15] - 2025-10-06
### Hinzugefügt
- Auswahl zwischen GPU und CPU über das neue `DEZENSUR_DEVICE` Environment-Flag
- GUI-Option für Hardware im Einstellungsdialog
- Test `test_device_override` prüft die Variable
### Geändert
- README erklärt die Option und hakt den TODO-Punkt ab

## [1.8.16] - 2025-10-07
### Hinzugefügt
- Zoom- und Pan-Unterstützung im Masken-Editor (Strg + Mausrad, Space zum Verschieben)
- Jest-Test `zoom with wheel` deckt das neue Feature ab
### Geändert
- README markiert Zoom & Pan als erledigt

## [1.8.17] - 2025-10-08
### Hinzugefügt
- Asynchrone Tile-Render-Engine mit Abbruch- und Resume-Funktion
- Unit-Test `tests/render/test_resume.py`
### Geändert
- README hakt die Render-Engine im TODO-Board ab

## [1.8.18] - 2025-10-09
### Hinzugefügt
- Modell-Selector im Side-Panel (`RightInspector`)
- Jest-Test `rightInspector.spec.tsx`
### Geändert
- README markiert Projekt-Handling, Masken-Editor und Einstellungs-Dialog als erledigt
- TODO-Board vermerkt den Modell-Selector

## [1.8.19] - 2025-10-10
### Hinzugefügt
- GitHub-Action `ci.yml` mit Windows- und Ubuntu-Matrix
- Caching für HuggingFace-Modelle
### Geändert
- README markiert die GitHub-Actions-Punkte im TODO-Board als erledigt

## [1.8.20] - 2025-10-11
### Hinzugefügt
- GitHub-Action `release.yml` erstellt Releases aus dem CHANGELOG
- Skript `scripts/extract_changelog.py` extrahiert die Notizen
### Geändert
- README hakt das automatische Changelog-Release ab

## [1.8.21] - 2025-10-12
### Hinzugefügt
- Mypy- und Ruff-Prüfung im CI-Workflow
- Coverage-Check mit Mindestwert 85 %
### Geändert
- README markiert die CI-Checks im TODO-Board als erledigt
- Dokumentation der neuen Lint-Tools

## [1.8.22] - 2025-10-13
### Hinzugefügt
- Umschaltbare Light/Dark-Themes in der GUI
### Geändert
- README hakt Dark-Theme und Test-Coverage im TODO-Board ab

## [1.8.23] - 2025-10-14
### Hinzugefügt
- Paket-Metadaten im `pyproject.toml` ermöglichen den PyPI-Build
### Geändert
- README erklärt das Erzeugen eines Wheels und markiert den TODO-Punkt als erledigt

## [1.8.24] - 2025-10-15
### Hinzugefügt
- Galerie unterstützt Drag-&-Drop zum Hinzufügen von Bildern
### Geändert
- README beschreibt den Import per Drag-&-Drop und hakt den TODO-Punkt ab

## [1.8.25] - 2025-10-16
### Hinzugefügt
- End-to-end-Test `e2e/editor.spec.ts` prüft das Öffnen des Masken-Editors
### Geändert
- README hakt den Editor-Test im TODO-Board ab

## [1.8.26] - 2025-10-17
### Hinzugefügt
- Skript `scripts/build_windows_exe.py` und `pyinstaller.spec` erzeugen eine portable EXE.
### Geändert
- README erklärt den EXE-Build und hakt den TODO-Punkt ab

## [1.8.27] - 2025-10-18
### Hinzugefügt
- Galerie generiert Vorschaubilder asynchron im Web Worker
- Platzhalter-Demo-Assets unter `demo_assets/`
### Geändert
- README markiert Lazy Thumb Generation und Demo Assets im TODO-Board als erledigt
## [1.8.28] - 2025-10-19
### Hinzugefügt
- Kontextabhängige Eigenschaften im Side-Panel
- End-to-end-Test `e2e/sidepanel.spec.ts`
### Geändert
- README markiert die Side-Panel-Punkte im TODO-Board als erledigt und beschreibt die Funktion

## [1.8.29] - 2025-10-20
### Geändert
- IPC nutzt jetzt `exposeElectronTRPC` im Preload und `createTRPCProxyClient`
  im Renderer.
### Behoben
- Build-Fehler durch fehlenden `createIPCClient`-Export behoben.

## [1.8.30] - 2025-10-21
### Behoben
- Fehlt der `dist`-Ordner, zeigt die Anwendung nun einen Hinweis statt eines
  weißen Fensters.
### Geändert
- README erläutert diesen Hinweis und wie der Build nachgeholt werden kann.


## [1.8.31] - 2025-10-22
### Hinzugefügt
- Skript `scripts/repair_gui.py` erstellt den Frontend-Build automatisch nach.
### Geändert
- README erwähnt das neue Reparatur-Skript.

## [1.8.32] - 2025-10-23
### Hinzugefügt
- `start.cmd` ermöglicht den Start per Doppelklick unter Windows.
### Geändert
- README und Handbuch beschreiben das neue Skript.

## [1.8.33] - 2025-10-24
### Geändert
- `start.py` verweigert `SKIP_NPM_INSTALL` außerhalb von CI und warnt den Nutzer.
### Hinzugefügt
- Tests `test_should_skip_npm_install_*` und README-TODO aktualisiert.

## [1.8.34] - 2025-10-25
### Geändert
- `gui/vite.config.ts` nutzt nun den Alias `./src`.
- `gui/package.json` pinnt `electron` auf Version 28.2.0,
  `electron-reload` auf 2.0.2 und `react-konva` auf 19.0.7.
### Hinzugefügt
- README markiert die erledigten Punkte im TODO-Board und
  listet die neuen Paketversionen auf.

## [1.8.35] - 2025-10-26
### Hinzugefügt
- Skript `scripts/sync_i18n.py` gleicht die Sprachdateien ab.
- Jest-Test `i18n.keys.spec.ts` prüft identische Schlüssel und wird über
  `tests/i18n/test_keys.py` ausgeführt.
### Geändert
- README beschreibt das neue Skript und hakt den TODO-Punkt zu den
  i18n-Bundles ab.

## [1.8.36] - 2025-10-27
### Hinzugefügt
- Datei `models.yml` verwaltet die Prüfsummen der Modelle zentral.
- Test `tests/models/test_checksum.py` prüft das Einlesen der YAML.
### Geändert
- `core/dep_manager.py` lädt nun optionale YAML-Overrides.
- README markiert den Punkt "Model-Manager Checksummen & Pfade" als erledigt.

## [1.8.37] - 2025-10-28
### Behoben
- Download des Modells `anime_censor_detection` schlägt nicht mehr wegen
  falscher Prüfsumme fehl. Die Prüfsumme wird nun ignoriert.

## [1.8.38] - 2025-10-29
### Behoben
- `npm install` schlug fehl, weil `electron-reload` in Version 2.0.2 nicht
  verfügbar ist. Die Abhängigkeit wurde daher auf Version 1.5.0 gesetzt.
### Geändert
- README und `package.json` führen die angepasste Version auf.

## [1.8.39] - 2025-10-30
### Geändert
- README ergänzt: `npm start` ohne vorangegangenen Build führt zu einer leeren
  Oberfläche. Empfohlene Befehle sind `python start.py` oder `npm run build`.

## [1.8.40] - 2025-10-31
### Hinzugefügt
- Option `--force-build` in `start.py` erzwingt einen neuen GUI-Build.
- `scripts/repair_gui.py` nutzt diese Option und baut stets neu.
### Geändert
- README beschreibt die neue Option.
