# DeZensur

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
| 📝 Saubere **Code-Doku**, **Tests** & **CI** | ⬜ |
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

zensur_remover/
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

```bash
# 1. Repo klonen
git clone https://github.com/<EuerRepo>/DeZensur.git
cd DeZensur

# 2. Erststart (erstellt venv, installiert Requirements, zieht Updates)
python start.py
````

Das Skript führt zuerst `git pull` aus, aktualisiert also euer Repository und
installiert anschließend alle Abhängigkeiten. Beim ersten Durchlauf lädt das
Tool alle benötigten Modelle in `models/`. Danach öffnet sich die GUI.

---

## Mitwirken

1. Forken ➜ Branch ➜ Pull Request
2. Code-Style: **black + isort**
3. Commit-Muster: `feat:`, `fix:`, `docs:` usw. (Conventional Commits)
4. Jeder PR benötigt einen Testfall in `tests/`

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
