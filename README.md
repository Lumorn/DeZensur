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

Voraussetzung ist eine installierte **Node.js**-Umgebung (inkl. `npm`),
da die GUI auf Electron basiert.

```bash
# 1. Repo klonen (alternativ nur start.py herunterladen)
git clone https://github.com/<EuerRepo>/DeZensur.git
cd DeZensur

# 2. Erststart (erstellt venv, installiert Requirements, zieht Updates)
python start.py
````
Mit `python start.py --dev` startet die Oberfläche im Entwicklungsmodus.

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
Ab Version 1.4.14 zeigt `start.py` bei jedem externen Befehl eine kleine Fortschrittsspinne im Terminal, damit man den aktuellen Schritt erkennt.
Ab Version 1.4.15 kann das Skript auch ohne das Paket `rich` starten. Die Fortschrittsanzeige erscheint erst, wenn die Abhängigkeit installiert ist.
Ab Version 1.4.16 weist `start.py` darauf hin, wenn `rich` fehlt und arbeitet dann ohne Fortschrittsanzeige weiter.

## Automatischer Modell-Download

Fehlende KI-Modelle werden beim Start automatisch aus dem Hugging-Face-Hub
heruntergeladen und im Ordner `models/` gespeichert. Eine SHA‑256-Prüfung
stellt sicher, dass die Dateien korrekt übertragen wurden.

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
Report mit Kennzahlen generiert.

Einen Report kann man auch nachträglich erstellen:

```bash
python -m core.report Projekte/Manga03.dezproj <batch_id>
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
