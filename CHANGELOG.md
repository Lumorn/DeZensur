# CHANGELOG

Alle Ãnderungen werden in diesem Dokument festgehalten.

## [0.1.0] â 2025-07-16
### HinzugefÃ¼gt
- Initiales ProjektgerÃ¼st (`gui/`, `core/`, `models/`, `tests/`)
- Bootstrap-Skript `start.py` mit Git-Self-Update & Dependency-Installer
- VollstÃ¤ndige README und CHANGELOG-Struktur

## [0.3.0] â 2025-07-16
### HinzugefÃ¼gt
- Electron-/React-Skeleton mit Projektverwaltung
- Python-Projektmanager und Bildlader
- Stub-Server mit Endpunkten `/detect`, `/segment`, `/inpaint`
- Aktualisiertes `start.py` zum Starten der GUI
- Neue Tests fÃ¼r Projektmanager und Server

## [0.4.0] â 2025-07-16
### HinzugefÃ¼gt
- Dependency-Manager lÃ¤dt Modelle automatisch herunter und prÃ¼ft deren IntegritÃ¤t

## [0.5.0] â 2025-07-16
### HinzugefÃ¼gt
- Modul 3: core/censor_detector.py (ONNX-Wrapper fÃ¼r anime_censor_detection)
- CLI `python -m core.censor_detector`
- NumPy-basierte NMS-Logik

## [0.6.0] â 2025-07-16
### HinzugefÃ¼gt
- Modul 4: core/segmenter.py (HQ-SAM & MobileSAM Integration)

## [0.7.0] â 2025-07-16
### HinzugefÃ¼gt
- Mask-Editor in der GUI zum manuellen Bearbeiten von Masken (Konva)

## [0.8.0] â 2025-07-16
### HinzugefÃ¼gt
- Modul 6: core/inpainter.py (LaMa + Stable-Diffusion-Inpainting)
- Neuer /inpaint-Endpunkt und GUI-Einstellung zur Modellauswahl

## [0.9.0] â 2025-07-16
### HinzugefÃ¼gt
- Modul 7: core/batch_runner.py, Rich-Progress, Thread-Pool
- Neuer /batch-Endpunkt im Stub-Server

## [1.0.0] â 2025-07-17
### HinzugefÃ¼gt
- Modul 8: JSON-Logging mit Loguru, Batch-Report-Generator
- CLI-Werkzeug `python -m core.report`

## [1.1.0] â 2025-07-17
### GeÃ¤ndert
- `start.py` aktualisiert nun zuerst das Repository und installiert danach die
  Python-AbhÃ¤ngigkeiten.
- Automatisches `npm install` in `gui/`, wenn `package.json` neuer ist oder
  `node_modules` fehlt.
### HinzugefÃ¼gt
- Modul 9: PyTest-Suite, Coverage-Threshold 80 %, GitHub Actions CI

## [1.2.0] â 2025-07-18
### HinzugefÃ¼gt
- Automatischer Prompt-Builder mit Genital-Tags
- GUI-Option âAutomatische Anatomie-Tagsâ
- Speichert verwendetes Prompt als `prompt.txt`
### GeÃ¤ndert
- ersetze Paketnamen 'lama-cleaner' â 'iopaint[lama]' (PyPI-konform)

## [1.3.0] â 2025-07-19
### HinzugefÃ¼gt
- GitHub Actions Workflow mit Format- und Testlauf

## [1.3.1] â 2025-07-20
### GeÃ¤ndert
- README: Projektordner heiÃt nun `DeZensur/`
- CI-Badge verweist auf korrektes GitHub-Repository

## [1.3.2] â 2025-07-21
### GeÃ¤ndert
- `iopaint[lama]` ist nun auf Version 1.2.5 festgeschrieben
### HinzugefÃ¼gt
- Hinweis zur festen Version in der README

## [1.3.3] â 2025-07-22
### GeÃ¤ndert
- `requirements.txt` beschrÃ¤nkt `torch` jetzt auf Version 2.1.x
### HinzugefÃ¼gt
- Info zur Torch-Begrenzung in der README

## [1.4.0] â 2025-07-23
### HinzugefÃ¼gt
- CI-Workflow prÃ¼ft jetzt flake8 und startet auch die Jest-Tests im GUI-Ordner
- Neues `npm`-Script `test` fÃ¼r Jest
### GeÃ¤ndert
- README erwÃ¤hnt den automatischen CI-Lauf

## [1.4.1] â 2025-07-24
### Behoben
- `start.py` fÃ¼gt nun das Projektverzeichnis dem `PYTHONPATH` hinzu, sodass der
  Import von `core` zuverlÃ¤ssig funktioniert.

## [1.4.2] â 2025-07-25
### HinzugefÃ¼gt
- `start.py` klont das Repository automatisch, wenn nur diese Datei vorliegt.

## [1.4.3] â 2025-07-26
### Behoben
- `start.py` importiert interne Module erst nach erfolgreicher Installation der
  AbhÃ¤ngigkeiten. Damit verhindert der Erststart fehlende Pakete wie
  `onnxruntime`.

## [1.4.4] â 2025-07-27
### GeÃ¤ndert
- `start.py` haelt das Terminal nun auch bei Fehlern offen und gibt den
  Stacktrace aus. So koennen Anwender die Fehlermeldung in Ruhe lesen.

## [1.4.5] â 2025-07-28
### GeÃ¤ndert
- `pytest.ini` verzichtet auf Coverage-Optionen, sodass die Tests auch ohne
  zusÃ¤tzliche Plugins laufen.
### HinzugefÃ¼gt
- Anleitung zum lokalen Testlauf in der README.

## [1.4.6] â 2025-07-29
### GeÃ¤ndert
- `start.py` prÃ¼ft nun, ob das Repository aktuell ist und fÃ¼hrt bei Bedarf
  automatisch `git pull` aus.
### GeÃ¤ndert
- README entsprechend angepasst.

## [1.4.7] â 2025-07-30
### GeÃ¤ndert
- `requirements.txt` setzt nun `torch` auf Version 2.2.x, da 2.1.x keine
  Pythonâ3.12-Builds bietet.
- README entsprechend angepasst.

## [1.4.8] â 2025-07-31
### GeÃ¤ndert
- `iopaint[lama]` ist nun auf Version 1.6.0 angehoben, um Python 3.12 zu
  unterstÃ¼tzen.
- README entsprechend angepasst.

## [1.4.9] â 2025-07-31
### GeÃ¤ndert
- `diffusers` ist nun auf Version 0.27.2 festgeschrieben, da iopaint 1.6.0
  diese Version benÃ¶tigt.
- README entsprechend ergÃ¤nzt.

## [1.4.10] â 2025-08-01
### HinzugefÃ¼gt
- `start.py` prÃ¼ft nun, ob `npm` installiert ist und gibt einen klaren
  Fehlerhinweis aus.
- README erwÃ¤hnt die notwendige Node.js-Installation.

## [1.4.11] â 2025-08-02
### GeÃ¤ndert
- `start.py` startet nach dem Anlegen der virtuellen Umgebung automatisch
  erneut mit dem Python der venv. Dadurch stehen neu installierte Pakete sofort
  zur VerfÃ¼gung.
- README erlÃ¤utert dieses Verhalten.

## [1.4.12] â 2025-08-03
### Behoben
- Unter Windows verursachte der Neustart via ``os.execv`` einen Fehler
  ``OSError: [Errno 12] Not enough space``. Das Skript nutzt dort nun
  ``subprocess`` und beendet sich anschlieÃend.
- Hinweis in der README ergÃ¤nzt.

## [1.4.13] â 2025-08-04
### GeÃ¤ndert
- `start.py` Ã¼berprÃ¼ft jetzt, ob uncommittete Ãnderungen vorhanden sind und
  warnt den Benutzer. Bei Ãnderungen wird kein automatisches `git pull`
  ausgefÃ¼hrt.

## [1.4.14] â 2025-08-05
### HinzugefÃ¼gt
- `start.py` zeigt nun fÃ¼r jeden externen Befehl einen Fortschrittsspinne im
  Terminal an. So ist klar ersichtlich, was gerade passiert.

## [1.4.15] â 2025-08-05
### GeÃ¤ndert
- `start.py` importiert `rich` nun erst in der Hilfsfunktion `run`. Dadurch
  startet das Skript auch dann fehlerfrei, wenn die AbhÃ¤ngigkeiten noch nicht
  installiert sind.

## [1.4.16] â 2025-08-05
### GeÃ¤ndert
- Fehlt das Paket `rich`, gibt `start.py` nun einen Hinweis aus und fÃ¼hrt den
  Befehl ohne Fortschrittsanzeige aus.

## [1.4.17] â 2025-08-06
### HinzugefÃ¼gt
- Neues Skript `generate_report.py`, das die CLI `python -m core.report` aufruft
  und einen Zielpfad fÃ¼r den Report entgegen nimmt.

## [1.4.18] â 2025-08-06
### Behoben
- `start.py` konnte in seltenen FÃ¤llen unendlich viele Python-Prozesse starten,
  wenn der Wechsel in die virtuelle Umgebung scheiterte. Eine Umgebungsvariable
  verhindert nun diese Neustart-Schleife.

## [1.4.19] â 2025-08-07
### GeÃ¤ndert
- `start.py` gibt nun auch im Terminal einen Hinweis aus, wenn `npm` fehlt. So
  ist der Grund eines Abbruchs besser erkennbar.

## [1.4.20] â 2025-08-08
### Behoben
- KompatibilitÃ¤tsproblem mit Ã¤lteren ``huggingface_hub``-Versionen: Das
  ``progress_bar``-Argument wird nun optional behandelt.
### GeÃ¤ndert
- README um Hinweis zur geÃ¤nderten Downloadfunktion ergÃ¤nzt.

## [1.4.21] â 2025-08-09
### Behoben
- ``dep_manager.download_model`` versucht nun alternative Dateinamen, falls der
  ursprÃ¼ngliche Modellname nicht verfÃ¼gbar ist.
### GeÃ¤ndert
- README weist auf diese Fallback-Strategie hin.

## [1.4.22] â 2025-08-10
### Behoben
- Fehlende Modelle werden nun Ã¼ber einen Repository-Snapshot gesucht, wenn alle
  bekannten Dateinamen einen 404-Fehler liefern.
### GeÃ¤ndert
- README erlÃ¤utert den neuen Snapshot-Fallback.

## [1.4.23] â 2025-08-11
### Behoben
- Snapshot-Fallback durchsucht nun alle bekannten Dateinamen und findet so auch
  ``.pth``-Modelle wie ``sam_vit_hq``.
### GeÃ¤ndert
- README weist auf die erweiterte Suche hin und das SAM-HQ-Repository wird in
  Kleinschreibung referenziert.

## [1.4.24] â 2025-08-12
### Behoben
- ``dep_manager.download_model`` Ã¼bergibt jetzt das in ``HUGGINGFACE_HUB_TOKEN``
  hinterlegte Zugangstoken an Hugging Face.
### GeÃ¤ndert
- README beschreibt die Token-Variable.

## [1.4.25] â 2025-08-13
### Behoben
- HQ-SAM wird jetzt aus ``syscv-community/sam-hq-vit-base`` geladen und nutzt
  die Datei ``sam_hq_vit_b.pth``. ``sam_vit_hq.pth`` bleibt als Fallback
  erhalten.
### GeÃ¤ndert
- README vermerkt den neuen Modellpfad.

## [1.4.26] â 2025-08-14
### Behoben
- Das HQ-SAM-Modell nutzt nun die Datei ``model.safetensors``. ``sam_hq_vit_b.pth``
  und ``sam_vit_hq.pth`` bleiben als Fallback erhalten.
### GeÃ¤ndert
- README weist auf den neuen Dateinamen hin.

## [1.4.27] â 2025-08-15
### GeÃ¤ndert
- ``dep_manager.download_model`` ermittelt nun automatisch den neuesten
  Unterordner von ``anime_censor_detection``. Dadurch funktionieren zukÃ¼nftige
  Versionen ohne Codeanpassung.
### HinzugefÃ¼gt
- Stub ``list_repo_files`` und aktualisierte Tests.

## [1.4.28] â 2025-08-16
### HinzugefÃ¼gt
- ``start.py`` prÃ¼ft jetzt die installierte Node-Version und bricht bei Version
  unter 18 mit einer Fehlermeldung ab.
### GeÃ¤ndert
- README erwÃ¤hnt die Mindestanforderung fÃ¼r Node.js.

## [1.4.29] â 2025-08-17
### Behoben
- Platzhalter in Log-Ausgaben werden nun korrekt mit ``{}`` formatiert.
### GeÃ¤ndert
- README weist auf die ``{}``-Syntax bei Loguru hin.

## [1.4.30] â 2025-08-18
### HinzugefÃ¼gt
- ``start.py`` erkennt ``npm`` jetzt auch Ã¼ber die Umgebungsvariable ``NPM_PATH``.
### GeÃ¤ndert
- README beschreibt die neue Variable zum Setzen des ``npm``-Pfads.

## [1.4.31] â 2025-08-19
### Behoben
- ``electron-reload`` wird wieder in Version ``2.0.0`` installiert, da ``2.0.2``
  nicht verfÃ¼gbar ist.
### GeÃ¤ndert
- README verweist auf die angepasste AbhÃ¤ngigkeit.

## [1.4.32] â 2025-08-20
### Behoben
- Fehlerhafte Version ``2.0.2`` von ``electron-reload`` entfernt und auf ``2.0.0``
  zurÃ¼ckgesetzt.
### GeÃ¤ndert
- README entsprechend angepasst.

## [1.4.33] â 2025-08-21
### GeÃ¤ndert
- `start.py` gibt nun einen Hinweis aus, wenn `npm install` wegen fehlender
  Pakete wie `electron-reload` scheitert.
### GeÃ¤ndert
- README um diese Info erweitert.

## [1.4.34] â 2025-08-22
### GeÃ¤ndert
- `electron-reload` wird jetzt in Version ``2.0.1`` installiert, da 2.0.0 und
  2.0.2 zu Problemen fÃ¼hrten.
### GeÃ¤ndert
- README entsprechend angepasst.

## [1.4.35] â 2025-08-23
### Behoben
- Die Version ``2.0.1`` von ``electron-reload`` existiert nicht im NPM-Registry.
  Das Paket wird daher wieder in Version ``2.0.0`` verwendet.
### GeÃ¤ndert
- README und ``package.json`` entsprechend angepasst.

## [1.4.36] â 2025-08-24
### HinzugefÃ¼gt
- ``start.py`` bietet mit ``SKIP_NPM_INSTALL`` bzw. ``--skip-npm`` die MÃ¶glichkeit,
  den `npm install`-Schritt zu Ã¼berspringen.
### GeÃ¤ndert
- README beschreibt die neue Option.

## [1.4.37] â 2025-08-25
### GeÃ¤ndert
- ``electron-reload`` wird nun in Version ``2.0.2`` verwendet,
  weil ``2.0.0`` nicht mehr in der Registry verfÃ¼gbar ist.
- README und ``package.json`` wurden entsprechend angepasst.


## [1.4.38] â 2025-08-26
### Behoben
- `electron-reload` 2.0.2 ist aus der Registry verschwunden. Die GUI nutzt wieder die stabile Version 1.6.0.
### GeÃ¤ndert
- README und `package.json` entsprechend angepasst.

## [1.4.39] â 2025-08-27
### Behoben
- Version 1.6.0 von `electron-reload` ist im npm-Registry nicht vorhanden. Wir verwenden nun Version 1.5.0.
### GeÃ¤ndert
- README und `package.json` wurden entsprechend angepasst.

## [1.4.40] â 2025-08-28
### Behoben
- Die AbhÃ¤ngigkeit `react-konva` zeigte auf eine nicht existierende Version 19.0.24.
  Jetzt verwenden wir Version 19.0.7 und passen `konva` auf 9.3.3 an.
### GeÃ¤ndert
- README und `package.json` fÃ¼hren die korrigierte Version auf.

## [1.4.41] â 2025-08-29
### Behoben
- `preload.js` verwendet jetzt CommonJS, damit Electron das Skript korrekt lÃ¤dt.
### GeÃ¤ndert
- README erwÃ¤hnt das CommonJS-Format des Preload-Skripts.

## [1.4.42] â 2025-08-30
### GeÃ¤ndert
- `index.html` definiert nun eine Content-Security-Policy, wodurch die Electron-Warnung zu unsicheren Skripten verschwindet.
### GeÃ¤ndert
- README weist auf die neue Content-Security-Policy hin.

## [1.4.43] â 2025-08-31
### HinzugefÃ¼gt
- `start.py` ruft nach einem erfolgreichen `npm install` automatisch `npm audit` auf und meldet eventuelle Probleme.
### GeÃ¤ndert
- README beschreibt die neue SicherheitsprÃ¼fung.

## [1.4.44] â 2025-09-01
### Behoben
- `vite.config.js` setzt nun den Basis-Pfad auf `./`, damit die gebaute GUI ihre Assets korrekt findet.
### GeÃ¤ndert
- README weist auf die neue `base`-Einstellung hin.

## [1.4.45] â 2025-09-02
### GeÃ¤ndert
- `start.py` prÃ¼ft das Git-Repository nun direkt beim Start und fÃ¼hrt ggf. ein Update durch, bevor weitere Schritte erfolgen.
- README beschreibt diese Ãnderung.

## [1.4.46] â 2025-09-03
### HinzugefÃ¼gt
- Option `--auto-stash` in `start.py`, die ungesicherte Ãnderungen automatisch vor dem `git pull` stasht und anschlieÃend wieder einspielt.
### GeÃ¤ndert
- README erlÃ¤utert die neue Option.

## [1.4.47] â 2025-09-04
### Behoben
- `start.py` baut die GUI nun automatisch, wenn `gui/dist` fehlt. Dadurch wird die OberflÃ¤che korrekt angezeigt.

## [1.4.48] â 2025-09-05
### Behoben
- Unter Windows schlug der Electron-Build fehl, wenn keine Symlink-Rechte vorhanden waren. `start.py` setzt nun `CSC_IDENTITY_AUTO_DISCOVERY=false`, damit kein Codesigning stattfindet.
### GeÃ¤ndert
- README beschreibt diese neue Umgebungsvariable.

## [1.4.49] â 2025-09-06
### HinzugefÃ¼gt
- `start.py` startet unter Windows automatisch mit Administratorrechten neu,
  wenn Symlink-Rechte fehlen.
### GeÃ¤ndert
- README dokumentiert dieses Verhalten.

## [1.4.50] â 2025-09-07
### Behoben
- Beim Aufruf von `npm start` erschien nur ein leeres Fenster, falls kein
  Vite-Server lief. `gui/electron/main.js` prÃ¼ft nun, ob der Server erreichbar
  ist und zeigt andernfalls die gebaute OberflÃ¤che oder einen Hinweis an.
### GeÃ¤ndert
- README erklÃ¤rt den Unterschied zwischen `npm run dev` und `npm start`.

## [1.4.51] â 2025-09-08
### Behoben
- "Bilder hinzufÃ¼gen" lÃ¶st jetzt einen Hinweis aus, wenn noch kein Projekt
  geÃ¶ffnet ist. Dadurch verhindert die GUI einen Absturz.
### GeÃ¤ndert
- README um Hinweis auf die neue Fehlermeldung ergÃ¤nzt.

## [1.5.0] â 2025-09-09
### HinzugefÃ¼gt
- Neues Desktop-Layout in der React-GUI mit Titelleiste,
  Befehlsleiste und Seitenleisten.
- Tailwind-Konfiguration enthÃ¤lt nun Farbtokens fÃ¼r das Dark-Theme.

## [1.5.1] â 2025-09-10
### HinzugefÃ¼gt
- Ordner `mockups/` mit zwei HTML-Dateien als Vorschau auf die
  Desktop-OberflÃ¤che (Front und Backstage).
- README beschreibt, wie die Mockups genutzt werden kÃ¶nnen.


## [1.6.0] â 2025-09-11
### HinzugefÃ¼gt
- Neues TypeScript-Frontend mit TanStack Router und Zustand-Stores.
- Playwright-Smoke-Test und electron-trpc IPC-GerÃ¼st.

## [1.7.0] â 2025-09-12
### HinzugefÃ¼gt
- IPC-Kommunikation nutzt jetzt **electron-trpc** mit Typsicherheit.
- Preload und Renderer binden die IPC-Routen automatisch ein.

## [1.7.1] â 2025-09-13
### GeÃ¤ndert
- Da Version 0.12.0 noch nicht verÃ¶ffentlicht ist, nutzt die GUI `electron-trpc` jetzt fest Version 0.11.x.

## [1.7.2] â 2025-09-14
### GeÃ¤ndert
- Das Startskript erwÃ¤hnt bei einem fehlgeschlagenen `npm install` nun `electron-trpc` statt `electron-reload`.

## [1.7.3] â 2025-09-15
### Behoben
- Das GUI-Build schlug wegen einer nicht vorhandenen Version von `electron-trpc` fehl. Die AbhÃ¤ngigkeit ist nun auf ^0.7.1 begrenzt.
### GeÃ¤ndert
- README und `package.json` weisen auf die korrigierte Version hin.
## [1.7.4] - 2025-09-16
### GeÃ¤ndert
- Electron deaktiviert jetzt das Autofill-Feature, um DevTools-Fehler zu vermeiden.

## [1.7.5] - 2025-09-17
### HinzugefÃ¼gt
- `start.py` prÃ¼ft nach `npm run build`, ob `gui/dist/index.html` vorhanden ist.
  Fehlt die Datei, erscheint eine Fehlermeldung.

## [1.7.6] - 2025-09-18
### Behoben
- `vite.config.ts` enthÃ¤lt nun ebenfalls den Basis-Pfad `./`, womit Electron die
  gebauten Assets fehlerfrei lÃ¤dt.

## [1.7.7] - 2025-07-17
### HinzugefÃ¼gt
- "Add Images" Dialog inklusive Galerie-Grid und Auswahlfunktion

## [1.7.8] - 2025-09-19
### HinzugefÃ¼gt
- Fenstersteuerung Ã¼ber die KnÃ¶pfe der Titelleiste
- Projektbefehle (Neu, Ãffnen, Bilder, Batch, Export) in der CommandBar
- AppBar mit Settings-Overlay, GPU-Umschalter und Ordnerauswahl
- Start-Button fÃ¼hrt die Zensurerkennung fÃ¼r das gewÃ¤hlte Bild aus
### GeÃ¤ndert
- README erwÃ¤hnt die neuen Button-Funktionen

## [1.7.9] - 2025-09-20
### GeÃ¤ndert
- Ordnerauswahl legt jetzt den Arbeitsordner im Zustand ab.
- Start-Button nutzt den tRPC-Endpunkt `censorDetect`.
- README beschreibt die beiden neuen Funktionen.

## [1.8.0] - 2025-09-21
### HinzugefÃ¼gt
- HTML-Export im Batch-Report (`core.report.render_html` und `generate_report.py --html`)
- README fÃ¼hrt das neue Kommando unter "Batch-Reports erstellen" auf

## [1.8.1] - 2025-09-22
### HinzugefÃ¼gt
- Einfaches CLI `dez.py` mit Befehl `detect`
- Testskript unter `tests/cli/test_help.py`
### GeÃ¤ndert
- README beschreibt den neuen CLI-Aufruf und hakt das TODO ab

## [1.8.2] - 2025-09-23
### HinzugefÃ¼gt
- Neuer CLI-Befehl `inpaint` zum Bearbeiten einzelner Bilder
- Test `tests/cli/test_inpaint_cli.py`
### GeÃ¤ndert
- README ergÃ¤nzt CLI-Beispiel und hakt das TODO ab

## [1.8.3] - 2025-09-24
### HinzugefÃ¼gt
- Neues Modul `core.project` mit Schema-VersionÂ 2 und automatischer Migration
- Test `tests/core/test_project_roundtrip.py`
### GeÃ¤ndert
- README erklÃ¤rt die Migration und hakt das TODO-Board ab

## [1.8.4] - 2025-09-25
### HinzugefÃ¼gt
- `detect_censor` unterstÃ¼tzt nun ein optionales ROI-Argument
  und die CLI kennt `--roi`
- Beispiel in der README angepasst
- Neue Tests fÃ¼r die ROI-Filterung
### GeÃ¤ndert
- TODO-Liste im README aktualisiert

## [1.8.5] - 2025-09-26
### HinzugefÃ¼gt
- Alias `detect-batch` fÃ¼r die CLI
- Test `tests/cli/test_detect_batch_cli.py`
- Test `tests/detector/test_thresholds.py`
### GeÃ¤ndert
- README um den neuen Befehl ergÃ¤nzt und TODOs aktualisiert

## [1.8.6] - 2025-09-27
### HinzugefÃ¼gt
- VersionsprÃ¼fung im Dependency-Manager (`core.dep_manager`)
- Neuer Test `tests/test_dep_manager.py::test_version_update`
### GeÃ¤ndert
- README hakt den Punkt "Dynamischer Model-Manager" ab

## [1.8.7] - 2025-09-28
### HinzugefÃ¼gt
- Automatischer Fallback auf **MobileSAM** bei fehlender GPU
- Neuer Test `tests/test_segmenter_mobile_fallback.py`
### GeÃ¤ndert
- TODO-Board markiert den MobileSAM-Fallback als erledigt

## [1.8.8] - 2025-09-29
### HinzugefÃ¼gt
- Neuer Test `tests/test_segmenter_gpu_pipeline.py`
### GeÃ¤ndert
- README hakt die SAM-HQ GPU-Pipeline und den Lama-Fallback ab

## [1.8.9] - 2025-09-30
### HinzugefÃ¼gt
- Einfache i18n-UnterstÃ¼tzung mit `de` und `en` JSON-Bundles
- Zustands-Store zur Laufzeitumschaltung der Sprache
- Neuer Test `tests/i18n/test_loader.py`
### GeÃ¤ndert
- README erklÃ¤rt den Sprachwechsel und markiert das TODO als erledigt

## [1.8.10] - 2025-10-01
### HinzugefÃ¼gt
- CLI-Skript `python -m dezensor.fetch_model` zum manuellen Herunterladen von Modellen
- Test `tests/test_fetch_model_cli.py`
### GeÃ¤ndert
- README beschreibt das Skript und hakt den Punkt "Modelle nachladen" ab

## [1.8.11] - 2025-10-02
### HinzugefÃ¼gt
- Unit-Test `gui/src/__tests__/settings.spec.tsx` und Wrapper `tests/test_settings_modal.py`
### GeÃ¤ndert
- README hakt den TODO-Eintrag fr den Settings-Test ab

## [1.8.12] - 2025-10-03
### HinzugefÃ¼gt
- Erste Version des Benutzerhandbuchs unter `docs/handbuch.md`
### GeÃ¤ndert
- README verweist auf das Handbuch und markiert den Punkt im TODO-Board als erledigt

## [1.8.13] - 2025-10-04
### HinzugefÃ¼gt
- Fortschritts-Modal zeigt den Status laufender Aufgaben in der GUI.
### GeÃ¤ndert
- README hakt den Punkt "Fortschritts-Modal" ab.


## [1.8.14] - 2025-10-05
### HinzugefÃ¼gt
- ControlNet-UnterstÃ¼tzung im Inpainter (`sd_controlnet`)
- Unit-Test `tests/inpaint/test_seams.py`
### GeÃ¤ndert
- README ergÃ¤nzt das ControlNet-Modell und markiert TODOs als erledigt

## [1.8.15] - 2025-10-06
### HinzugefÃ¼gt
- Auswahl zwischen GPU und CPU Ã¼ber das neue `DEZENSUR_DEVICE` Environment-Flag
- GUI-Option fÃ¼r Hardware im Einstellungsdialog
- Test `test_device_override` prÃ¼ft die Variable
### GeÃ¤ndert
- README erklÃ¤rt die Option und hakt den TODO-Punkt ab

## [1.8.16] - 2025-10-07
### HinzugefÃ¼gt
- Zoom- und Pan-UnterstÃ¼tzung im Masken-Editor (Strg + Mausrad, Space zum Verschieben)
- Jest-Test `zoom with wheel` deckt das neue Feature ab
### GeÃ¤ndert
- README markiert Zoom & Pan als erledigt

## [1.8.17] - 2025-10-08
### HinzugefÃ¼gt
- Asynchrone Tile-Render-Engine mit Abbruch- und Resume-Funktion
- Unit-Test `tests/render/test_resume.py`
### GeÃ¤ndert
- README hakt die Render-Engine im TODO-Board ab

## [1.8.18] - 2025-10-09
### HinzugefÃ¼gt
- Modell-Selector im Side-Panel (`RightInspector`)
- Jest-Test `rightInspector.spec.tsx`
### GeÃ¤ndert
- README markiert Projekt-Handling, Masken-Editor und Einstellungs-Dialog als erledigt
- TODO-Board vermerkt den Modell-Selector

## [1.8.19] - 2025-10-10
### HinzugefÃ¼gt
- GitHub-Action `ci.yml` mit Windows- und Ubuntu-Matrix
- Caching fÃ¼r HuggingFace-Modelle
### GeÃ¤ndert
- README markiert die GitHub-Actions-Punkte im TODO-Board als erledigt

## [1.8.20] - 2025-10-11
### HinzugefÃ¼gt
- GitHub-Action `release.yml` erstellt Releases aus dem CHANGELOG
- Skript `scripts/extract_changelog.py` extrahiert die Notizen
### GeÃ¤ndert
- README hakt das automatische Changelog-Release ab

## [1.8.21] - 2025-10-12
### HinzugefÃ¼gt
- Mypy- und Ruff-PrÃ¼fung im CI-Workflow
- Coverage-Check mit Mindestwert 85Â %
### GeÃ¤ndert
- README markiert die CI-Checks im TODO-Board als erledigt
- Dokumentation der neuen Lint-Tools

## [1.8.22] - 2025-10-13
### HinzugefÃ¼gt
- Umschaltbare Light/Dark-Themes in der GUI
### GeÃ¤ndert
- README hakt Dark-Theme und Test-Coverage im TODO-Board ab

## [1.8.23] - 2025-10-14
### HinzugefÃ¼gt
- Paket-Metadaten im `pyproject.toml` ermÃ¶glichen den PyPI-Build
### GeÃ¤ndert
- README erklÃ¤rt das Erzeugen eines Wheels und markiert den TODO-Punkt als erledigt

## [1.8.24] - 2025-10-15
### HinzugefÃ¼gt
- Galerie unterstÃ¼tzt Drag-&-Drop zum HinzufÃ¼gen von Bildern
### GeÃ¤ndert
- README beschreibt den Import per Drag-&-Drop und hakt den TODO-Punkt ab

## [1.8.25] - 2025-10-16
### HinzugefÃ¼gt
- End-to-end-Test `e2e/editor.spec.ts` prÃ¼ft das Ãffnen des Masken-Editors
### GeÃ¤ndert
- README hakt den Editor-Test im TODO-Board ab

## [1.8.26] - 2025-10-17
### HinzugefÃ¼gt
- Skript `scripts/build_windows_exe.py` und `pyinstaller.spec` erzeugen eine portable EXE.
### GeÃ¤ndert
- README erklÃ¤rt den EXE-Build und hakt den TODO-Punkt ab

## [1.8.27] - 2025-10-18
### HinzugefÃ¼gt
- Galerie generiert Vorschaubilder asynchron im Web Worker
- Platzhalter-Demo-Assets unter `demo_assets/`
### GeÃ¤ndert
- README markiert Lazy Thumb Generation und Demo Assets im TODO-Board als erledigt
## [1.8.28] - 2025-10-19
### HinzugefÃ¼gt
- KontextabhÃ¤ngige Eigenschaften im Side-Panel
- End-to-end-Test `e2e/sidepanel.spec.ts`
### GeÃ¤ndert
- README markiert die Side-Panel-Punkte im TODO-Board als erledigt und beschreibt die Funktion

## [1.8.29] - 2025-10-20
### GeÃ¤ndert
- IPC nutzt jetzt `exposeElectronTRPC` im Preload und `createTRPCProxyClient`
  im Renderer.
### Behoben
- Build-Fehler durch fehlenden `createIPCClient`-Export behoben.

## [1.8.30] - 2025-10-21
### Behoben
- Fehlt der `dist`-Ordner, zeigt die Anwendung nun einen Hinweis statt eines
  weiÃen Fensters.
### GeÃ¤ndert
- README erlÃ¤utert diesen Hinweis und wie der Build nachgeholt werden kann.


## [1.8.31] - 2025-10-22
### HinzugefÃ¼gt
- Skript `scripts/repair_gui.py` erstellt den Frontend-Build automatisch nach.
### GeÃ¤ndert
- README erwÃ¤hnt das neue Reparatur-Skript.

## [1.8.32] - 2025-10-23
### HinzugefÃ¼gt
- `start.cmd` ermÃ¶glicht den Start per Doppelklick unter Windows.
### GeÃ¤ndert
- README und Handbuch beschreiben das neue Skript.

## [1.8.33] - 2025-10-24
### GeÃ¤ndert
- `start.py` verweigert `SKIP_NPM_INSTALL` auÃerhalb von CI und warnt den Nutzer.
### HinzugefÃ¼gt
- Tests `test_should_skip_npm_install_*` und README-TODO aktualisiert.

## [1.8.34] - 2025-10-25
### GeÃ¤ndert
- `gui/vite.config.ts` nutzt nun den Alias `./src`.
- `gui/package.json` pinnt `electron` auf Version 28.2.0,
  `electron-reload` auf 2.0.2 und `react-konva` auf 19.0.7.
### HinzugefÃ¼gt
- README markiert die erledigten Punkte im TODO-Board und
  listet die neuen Paketversionen auf.

## [1.8.35] - 2025-10-26
### HinzugefÃ¼gt
- Skript `scripts/sync_i18n.py` gleicht die Sprachdateien ab.
- Jest-Test `i18n.keys.spec.ts` prÃ¼ft identische SchlÃ¼ssel und wird Ã¼ber
  `tests/i18n/test_keys.py` ausgefÃ¼hrt.
### GeÃ¤ndert
- README beschreibt das neue Skript und hakt den TODO-Punkt zu den
  i18n-Bundles ab.

## [1.8.36] - 2025-10-27
### HinzugefÃ¼gt
- Datei `models.yml` verwaltet die PrÃ¼fsummen der Modelle zentral.
- Test `tests/models/test_checksum.py` prÃ¼ft das Einlesen der YAML.
### GeÃ¤ndert
- `core/dep_manager.py` lÃ¤dt nun optionale YAML-Overrides.
- README markiert den Punkt "Model-Manager Checksummen & Pfade" als erledigt.

## [1.8.37] - 2025-10-28
### Behoben
- Download des Modells `anime_censor_detection` schlÃ¤gt nicht mehr wegen
  falscher PrÃ¼fsumme fehl. Die PrÃ¼fsumme wird nun ignoriert.

## [1.8.38] - 2025-10-29
### Behoben
- `npm install` schlug fehl, weil `electron-reload` in Version 2.0.2 nicht
  verfÃ¼gbar ist. Die AbhÃ¤ngigkeit wurde daher auf Version 1.5.0 gesetzt.
### GeÃ¤ndert
- README und `package.json` fÃ¼hren die angepasste Version auf.

## [1.8.39] - 2025-10-30
### GeÃ¤ndert
- README ergÃ¤nzt: `npm start` ohne vorangegangenen Build fÃ¼hrt zu einer leeren
  OberflÃ¤che. Empfohlene Befehle sind `python start.py` oder `npm run build`.

## [1.8.40] - 2025-10-31
### HinzugefÃ¼gt
- Option `--force-build` in `start.py` erzwingt einen neuen GUI-Build.
- `scripts/repair_gui.py` nutzt diese Option und baut stets neu.
### GeÃ¤ndert
- README beschreibt die neue Option.

## [1.8.41] - 2025-11-01
### Behoben
- Preload importierte versehentlich `electron-trpc/main`, wodurch das `electronTRPC`-Objekt im Renderer fehlte.
### Geändert
- README erläutert den korrigierten Import in der Bug-Liste.

## [1.8.42] - 2025-11-02
### Behoben
- Jest brach mit "Cannot use import statement outside a module" ab.
  Neue Dateien `gui/babel.config.cjs` und `gui/jest.config.cjs` stellen die Transformation sicher.
### Geändert
- README führt die Babel- und Jest-Konfiguration als behobenen Fehler auf.

## [1.8.43] - 2025-11-03
### Behoben
- `galleryStore.addImages` legte doppelte Bilder an.
  Pfade werden nun innerhalb eines Aufrufs dedupliziert.
- Fehlende Playwright-Abhängigkeit führte zu Modulfehlern.
  `@playwright/test` ist jetzt in den Dev-Dependencies.
### Geändert
- Jest ignoriert `tests/e2e/` damit Playwright separat läuft.
- README ergänzt Bugfix zur Galerie.

## [1.8.44] - 2025-11-04
### Behoben
- CI schlug wegen unsortierter `import`-Blöcke fehl.
  `isort .` korrigiert nun automatisch alle Dateien.
### Geändert
- README erwähnt den isort-Fix.

## [1.8.45] - 2025-11-05
### Behoben
- Pytest meldete `ModuleNotFoundError: yaml`.
  Das Paket `PyYAML` ist nun in `requirements.txt` enthalten.
### Geändert
- README führt PyYAML als neue Abhängigkeit auf.
