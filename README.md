# DeZensur
![CI](https://github.com/Lumorn/DeZensur/actions/workflows/ci.yml/badge.svg)

**DeZensur** ist ein rein lokales Windows-(optionaler Cross-Platform-Support)-Tool-Kit,  
das Zensur in Anime- und Comicbildern **vollautomatisch** erkennt und entfernt.  
Es kombiniert modernste Open-Source-Modelle:

* **anime_censor_detection** (ONNX) – erkennt Zensurbalken / Mosaik / Blur  
* **SAM-HQ** – präzise Maskensegmentierung auf Knopfdruck  
* **Inpainting-Modelle** (AnimeMangaInpainting, revAnimated, LaMa, Stable Diffusion) – rekonstruiert verdeckte Bereiche

> Alles läuft **offline** auf deiner GPU/CPU, keine Cloud-Abhängigkeit.

---

## Projektziele

| Ziel | Status |
|------|--------|
| 🔄 Volle **Automatisierung** ohne manuelle Klicks | ⬜ |
| 🖼️ Intuitive **GUI** für Einzel- & Batch-Modus (Electron + React) | ⬜ |
| 🧩 **Modular** – jeder Verarbeitungsschritt als eigenständiges Modul | ⬜ |
| ⚡ **Schnellstart**: `start.py` erledigt Git-Pull + `pip install` | ✅ |
| 📦 **Selbst-Updater** & automatischer Modell-Download | ⬜ |
| 📝 Saubere **Code-Doku**, **Tests** & **CI** | ✅ |
| 🧪 **Erweiterbar** (Video-Support, neue Modelle, LoRAs) | ⬜ |

---

## Funktionsübersicht

1. **Bild-/Ordner-Import**  
2. **Automatische Zensur-Erkennung** (Bounding-Boxen via `anime_censor_detection`)  
3. **Masken-Verfeinerung** mit SAM-HQ  
4. **Inpainting** der Maskenbereiche (modell-wählbar)  
5. **Batch-Modus** für ganze Verzeichnisse  
6. **Protokoll & Export** (Original, Maske, Ergebnis, Log)

---

## Ordnerstruktur

```

DeZensur/
├─ start.py                # Bootstrap-Script (Self-Update + GUI-Start)
├─ requirements.txt
├─ gui/                    # Electron/React-Frontend
├─ core/                   # Python-Back-End-Module
│   ├─ image_loader.py
│   ├─ censor_detector.py
│   ├─ segmenter.py
│   ├─ inpainter.py
│   ├─ batch_runner.py
│   └─ dep_manager.py
├─ models/                 # Automatisch gefüllte Modell-Ordner
├─ tests/                  # PyTest-Suite
├─ CHANGELOG.md
└─ LICENSE

````

---

## Schnellstart

Voraussetzung ist eine installierte **Node.js**-Umgebung (inkl. `npm`)
ab Version **18**, da die GUI auf Electron basiert.
Ab Version 1.4.41 muss das Preload-Skript `gui/electron/preload.js` im CommonJS-Stil
(`require` statt `import`) vorliegen, da Electron ES-Module dort nicht lädt.
Seit Version 1.4.42 besitzt `gui/index.html` eine eigene Content-Security-Policy,
welche die Electron-Warnung zu unsicheren Skripten unterbindet.

```bash
# 1. Repo klonen (alternativ nur start.py herunterladen)
git clone https://github.com/<EuerRepo>/DeZensur.git
cd DeZensur

# 2. Erststart (erstellt venv, installiert Requirements, zieht Updates)
python start.py
````
Mit `python start.py --dev` startet die Oberfläche im Entwicklungsmodus.

Möchtest du die GUI direkt über Node starten, wechsle in den Ordner `gui` und
führe `npm run dev` aus. Damit laufen Vite und Electron parallel. Der Befehl
`npm start` hingegen lädt nur Electron und setzt voraus, dass zuvor `npm run
build` ausgeführt wurde. Ohne diesen Build bleibt das Fenster leer.

Ab Version 1.3.3 nutzt die neue TypeScript-Oberflaeche mit TanStack Router. Nach `npm install` startest du die Entwicklung mit `npm run dev`. Der E2E-Test laeuft mit `npx playwright test`.
Seit Version 1.7.0 kommuniziert das Frontend dank **electron-trpc** typisiert mit dem Python-Backend.
Beim Start prüft das Skript, ob neue Commits auf `origin/main` vorhanden sind
und zieht sie automatisch. Anschließend installiert es alle
Abhängigkeiten. Beim ersten Durchlauf lädt das
Tool alle benötigten Modelle in `models/`. Fehlen die Node-Abhängigkeiten,
wird automatisch `npm install` in `gui/` ausgeführt. Danach öffnet sich die GUI.

Ab Version 1.4.1 setzt `start.py` sein Verzeichnis automatisch auf den
`PYTHONPATH`. Dadurch funktioniert der Import des Pakets `core` auch dann,
wenn das Skript von einem anderen Arbeitsverzeichnis aus aufgerufen wird.

Seit Version 1.4.2 kann `start.py` zudem das komplette Repository
selbstständig klonen, wenn nur diese Datei vorhanden ist.

Ab Version 1.4.3 werden die internen Module erst nach der Installation der
Python-Abhängigkeiten importiert. So treten keine Fehler mehr auf, wenn
Pakete wie `onnxruntime` noch fehlen.
Ab Version 1.4.4 bleibt das Terminal auch bei Fehlern offen, damit man die
Ausgabe in Ruhe lesen kann.
Ab Version 1.4.6 startet `start.py` nach dem Anlegen der virtuellen Umgebung
automatisch erneut mit dem Python der venv. Dadurch sind frisch installierte
Pakete sofort nutzbar und Importfehler werden vermieden.
Ab Version 1.4.12 wird unter Windows kein ``os.execv`` mehr verwendet,
da dies dort zu ``OSError: [Errno 12] Not enough space`` führte. Stattdessen
startet ein neuer Prozess und das Skript beendet sich anschließend.
Seit Version 1.4.13 prüft `start.py` zudem, ob ungesicherte Änderungen im
Repository vorliegen. Ist dies der Fall, wird ein Hinweis angezeigt und der
automatische `git pull` übersprungen.
Ab Version 1.4.46 kann das Skript mit `--auto-stash` diese Änderungen
automatisch stashen, den Pull durchführen und anschließend den Stash wieder anwenden.
Ab Version 1.4.14 zeigt `start.py` bei jedem externen Befehl eine kleine Fortschrittsspinne im Terminal, damit man den aktuellen Schritt erkennt.
Ab Version 1.4.15 kann das Skript auch ohne das Paket `rich` starten. Die Fortschrittsanzeige erscheint erst, wenn die Abhängigkeit installiert ist.
Ab Version 1.4.16 weist `start.py` darauf hin, wenn `rich` fehlt und arbeitet dann ohne Fortschrittsanzeige weiter.
Ab Version 1.4.18 verhindert eine Umgebungsvariable endlose Neustart-Schleifen, wenn das Skript die virtuelle Umgebung aktiviert.
Ab Version 1.4.19 erscheint der Hinweis auf fehlendes `npm` nun auch im Terminal.

## Automatischer Modell-Download

Fehlende KI-Modelle werden beim Start automatisch aus dem Hugging-Face-Hub
heruntergeladen und im Ordner `models/` gespeichert. Eine SHA‑256-Prüfung
stellt sicher, dass die Dateien korrekt übertragen wurden.
Seit Version 1.4.20 ignoriert der Download das optionale ``progress_bar``-
Argument, sodass auch ältere ``huggingface_hub``-Versionen funktionieren.
Ab Version 1.4.21 prüft der Dependency-Manager zudem alternative Dateinamen,
falls ein Modell auf Hugging Face umbenannt wurde.
Ab Version 1.4.22 wird bei fehlenden Dateien das gesamte Repository als
Snapshot heruntergeladen und die erste gefundene ``.onnx``-Datei verwendet.
Seit Version 1.4.23 durchsucht dieser Snapshot alle bekannten Dateinamen,
so dass auch ``.pth``-Modelle wie ``sam_vit_hq`` gefunden werden.
Ab Version 1.4.24 kann optional ein Zugangstoken 
über die Umgebungsvariable ``HUGGINGFACE_HUB_TOKEN`` gesetzt werden,
um private oder nur für angemeldete Nutzer freigegebene Modelle herunterladen zu können.
Seit Version 1.4.25 wird das HQ-SAM-Modell aus dem Repository `syscv-community/sam-hq-vit-base` geladen. Der frühere Dateiname `sam_vit_hq.pth` bleibt als Fallback erhalten.
Ab Version 1.4.26 heißt die bereitgestellte Gewichtsdatei `model.safetensors`. Die alten Dateinamen werden weiterhin als Ersatz akzeptiert.
Seit Version 1.4.27 erkennt der Downloader automatisch den neuesten Unterordner
von `anime_censor_detection` (z.B. `censor_detect_v0.9_s/model.onnx`). Damit
funktioniert der Download auch bei zukünftigen Updates ohne Anpassungen.
Ab Version 1.4.28 prüft `start.py` die installierte Node-Version und verlangt
mindestens Version 18.
Ab Version 1.4.30 kann der Pfad zu `npm` über die Umgebungsvariable
``NPM_PATH`` gesetzt werden, falls das Programm nicht im ``PATH`` liegt.
Ab Version 1.4.31 setzte die GUI `electron-reload` erneut in Version 2.0.0 ein,
da sich damals Version 2.0.2 nicht installieren ließ.
Ab Version 1.4.34 sollte die GUI eigentlich `electron-reload` in Version 2.0.1
einsetzen. Da diese Version jedoch nicht in der Registry vorhanden war,
nutzte Version 1.4.35 weiterhin `electron-reload` 2.0.0.
Seit Version 1.4.37 wurde `electron-reload` in Version 2.0.2 verwendet, da 2.0.0 nicht mehr verfügbar war.
Seit Version 1.4.38 kam kurzzeitig wieder die stabile Version 1.6.0 zum Einsatz, weil 2.0.2 aus der Registry entfernt wurde.
Seit Version 1.4.39 verwenden wir nun Version 1.5.0, da die zuvor angegebene 1.6.0 nicht im npm-Registry existiert.
Ab Version 1.4.33 weist `start.py` auf fehlgeschlagene `npm install`-Befehle hin,
falls beispielsweise `electron-reload` in der geforderten Version nicht
gefunden wird.
Ab Version 1.4.36 kann der Schritt `npm install` mit der Umgebungsvariable
`SKIP_NPM_INSTALL` oder dem Parameter `--skip-npm` übersprungen werden. Das ist
hilfreich, wenn die Pakete bereits installiert sind oder keine
Internetverbindung besteht.
Mit `--auto-stash` stasht `start.py` ungesicherte Änderungen automatisch vor dem Pull und stellt sie anschließend wieder her.
Ab Version 1.4.40 setzt die GUI `react-konva` in Version 19.0.7 ein,
da die zuvor eingetragene Version 19.0.24 nie veröffentlicht wurde.
Ab Version 1.4.43 führt `start.py` nach einem erfolgreichen `npm install`
automatisch `npm audit` aus und weist bei Fehlern auf mögliche
Sicherheitslücken hin.
Ab Version 1.4.44 verwendet die Vite-Konfiguration den relativen Basis-Pfad
`./`, damit die gebaute Electron-Oberfläche ihre Assets findet.
Ab Version 1.4.45 prüft `start.py` das Git-Repository bereits vor dem Anlegen der
virtuellen Umgebung und aktualisiert es gegebenenfalls.
Ab Version 1.4.47 wird die React-Oberfläche automatisch gebaut, wenn noch kein
`gui/dist`-Ordner existiert. Dadurch erscheint die GUI auch bei einer frischen
Installation korrekt.
Ab Version 1.4.48 setzt `start.py` unter Windows automatisch
`CSC_IDENTITY_AUTO_DISCOVERY=false`, damit `electron-builder`
ohne Symlink-Rechte funktioniert.
Ab Version 1.4.49 fordert `start.py` bei fehlenden Symlink-Rechten
automatisch Administratorrechte an und startet sich neu.
Ab Version 1.5.0 verpasst die GUI ein neues Desktop-Layout mit Titelleiste,
Befehlsleiste, Seitenleisten und Arbeitsbereich.

## Automatische Zensur-Erkennung (Modul 3)

Die Datei `core/censor_detector.py` kapselt das ONNX-Modell
`deepghs/anime_censor_detection` (Labels: nipple_f, penis, pussy) und liefert
JSON-Bounding-Boxen inkl. Scores. Per CLI kann man den Detector so nutzen:
`python -m core.censor_detector <bild.png> --json boxes.json`.

## Schritt 4 – SAM-Segmenter

Neben HQ-SAM steht auch MobileSAM zur Auswahl. HQ-SAM liefert sehr exakte
Masken, MobileSAM arbeitet dagegen deutlich schneller und eignet sich für
schwächere Hardware.

Beispielaufruf:

```bash
python -m core.segmenter samples/page01.png --boxes 120,80,400,350 --model sam_vit_hq --out page01_mask.png
```

## Schritt 5 – Manueller Masken-Editor

In der GUI kann eine automatisch erzeugte Maske nun per Canvas bearbeitet werden.
Der Editor nutzt **Konva.js** und erlaubt Zeichnen, Radieren sowie Undo/Redo.
Die finalisierte Maske wird als PNG in den Projektordner gespeichert.

## Schritt 6 – Inpainting

Zum Auffüllen der Masken stehen zwei Verfahren bereit:

| Modellschlüssel | Technik | Vorteile |
|------------------|---------|----------|
| `lama` | CNN-Inpainting (LaMa) | sehr schnell, kein Prompt nötig |
| `sd2_inpaint` | Stable Diffusion 2 Inpainting | flexibel, promptbar |
| `revanimated` | revAnimated Inpainting | Anime-optimiert |

Alle Modelle brauchen eine GPU, bei CPU-Fallback entsteht nur ein leeres Bild.

Das LaMa-Modell wird nun über das PyPI-Paket `iopaint[lama]` bereitgestellt.
Seit Version **1.4.8** setzen wir dabei auf **iopaint 1.6.0**, da ältere Versionen
kein Python 3.12 unterstützen. Ab Version **1.4.9** ist deshalb
`diffusers` auf **0.27.2** festgeschrieben, weil diese Version von iopaint
benötigt wird.
Ab Version 1.4.7 setzen wir **PyTorch** auf die Version *2.2.x*. Die vorherige
Beschränkung auf *2.1.x* verursachte Installationsprobleme unter Python 3.12.

![Einstellungen Dialog](gui_screenshot.png "GUI-Einstellungen f\xFCr Inpainting")

Beispiel für die CLI:

```bash
python -m core.inpainter images/page01.png masks/page01.png --model revanimated \
       --prompt "bare chest, anime style" --out processed/page01.png
```

### Anatomie-Tags

Aktiviert man in den Einstellungen die Option **Automatische Anatomie-Tags**, wird der Prompt automatisch um passende Genitalbegriffe (z.B. `penis`, `pussy`) erweitert. Dadurch gelingt eine detailgetreue Rekonstruktion der verdeckten Bereiche.
Zusätzlich wird das verwendete Prompt neben dem Ergebnisbild in einer Datei `prompt.txt` gespeichert.

## Schritt 7 – Batch-Runner

Mehrere Bilder lassen sich jetzt komplett ohne Interaktion verarbeiten. Der
Befehl zeigt eine Rich-Fortschrittsleiste an.

```bash
python -m core.batch_runner Projekte/Manga03.dezproj --workers 4
```

Der Stub-Server bietet dazu den Endpunkt `/batch`, der denselben Vorgang im
Hintergrund startet und eine Task-ID zurückliefert.

## Schritt 8 – Logging & Reports

Der Batch-Runner schreibt nun strukturierte Log-Dateien in den Projektordner.
Neben einer lesbaren `run_*.log`-Datei entsteht ein JSON-Log `run_*.jsonl`.
Loguru kümmert sich dabei um Rotation und Aufbewahrung. Nach Abschluss wird ein
Report mit Kennzahlen generiert. Log-Nachrichten verwenden die
loguru-übliche Formatierung mit `{}`-Platzhaltern, etwa
`logger.info("Lade ONNX-Modell {}", pfad)`.

Einen Report kann man auch nachträglich erstellen:

```bash
python -m core.report Projekte/Manga03.dezproj <batch_id>
```

Alternativ erlaubt das Skript `generate_report.py` einen frei wählbaren Zielpfad:

```bash
python generate_report.py Projekte/Manga03.dezproj <batch_id> --report Auswertung/report.json
```

Beispiel für einen JSON-Eintrag:

```json
{"time":"2025-07-16T18:22:30.003Z","level":"INFO","message":"done",
 "extra":{"batch":"20250716_1822","img":"page01","duration_ms":742,"model":"lama"}}
```

---

## Projektordnerstruktur & GUI

Beim Anlegen eines Projektes wird eine Ordnerstruktur erzeugt:

```
<Projektname>/
├─ originals/   # importierte Bilder
├─ masks/       # Masken
├─ processed/   # Ergebnisse
└─ logs/        # Protokolle
```

Die GUI erlaubt das Importieren einzelner Bilder oder ganzer Ordner. Alle
Bilder werden in `originals/` kopiert und in der Galerie als Thumbnails
angezeigt. Einstellungen und Bildstatus werden in einer `.dezproj`-Datei im
Projektordner gespeichert.
Versucht man, ohne geöffnetes Projekt Bilder hinzuzufügen, erscheint nun eine
Hinweismeldung.

## Mockups

Im Ordner `mockups/` liegen zwei HTML-Dateien, die das geplante
Desktop-Layout von DeZensur demonstrieren.
`front.html` zeigt die normale Benutzeroberfläche, `backstage.html` die
Einstellungs-Ansicht. Du kannst die Dateien einfach im Browser öffnen, um
einen ersten Eindruck vom Dark-Theme und der Anordnung der Bereiche zu
erhalten.

---

## Mitwirken

1. Forken ➜ Branch ➜ Pull Request
2. Code-Style: **black + isort**
3. Commit-Muster: `feat:`, `fix:`, `docs:` usw. (Conventional Commits)
4. Jeder PR benötigt einen Testfall in `tests/`
5. Die GitHub-Action prüft Formatierung (black, isort, flake8) und startet alle Tests

## Tests

Um die Tests lokal auszuführen, muss der Ordner `tests` im `PYTHONPATH` stehen,
damit die Stubs der Abhängigkeiten gefunden werden:

```bash
PYTHONPATH=tests pytest -q
```

---

## TODO-Liste (Auszug)

* [ ] React-Galerie-Komponente fertigstellen
* [ ] Asynchrones Laden großer Ordner
* [ ] Fortschritts-Overlay für Batch-Jobs
* [ ] GPU-vs-CPU-Fallback automatisieren
* [ ] Video-Pipeline (ffmpeg + frame-by-frame)
* [ ] Portable EXE-Build (PyInstaller)

---

## Lizenz

MIT – siehe [LICENSE](LICENSE).
