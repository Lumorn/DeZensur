# DeZensur

![CI](https://github.com/Lumorn/DeZensur/actions/workflows/ci.yml/badge.svg)

**DeZensur** ist ein rein lokales Toolkit zur automatischen Entfernung von Zensur in Anime‑ und Comicbildern.  
Alle Modelle laufen **offline** auf deiner GPU / CPU – keine Cloud‑Abhängigkeiten.

---

## Projektziele

| Ziel | Status |
|------|--------|
| 🔄 Volle **End‑to‑End‑Automatisierung** | ⬜ |
| 🖼️ Intuitive **Electron + React GUI** | ⬜ |
| 🧩 **Modulare Pipeline** (Detection → Segmentation → Inpainting) | ⬜ |
| ⚡ **start.py** erledigt Git + `pip install` + GUI‑Build | ✅ |
| 📦 **Self‑Updater** & automatischer Modell‑Download | ⬜ |
| 📝 **Tests + CI** (black, isort, flake8, pytest) | ✅ |
| 🧪 **Erweiterbar** (Video‑Support, LoRA‑Modelle) | ⬜ |

---

## **Aktuelle TODO‑Liste**  
*Markdown‑Checkboxen können direkt in GitHub oder VS Code abgehakt werden.*

### Backend / Core

- [ ] Integration **anime_censor_detection** (ONNX)  
- [ ] HQ‑**SAM** Segmenter (`sam_vit_hq`)  
- [ ] Option **MobileSAM** für schwache Hardware  
- [ ] Anatomie‑Tag‑Ergänzer für bessere Prompts  
- [ ] Dynamischer **Model‑Manager** (Download + Version‑Check)  
- [ ] **Batch‑Runner** mit Fortschritts‑Overlay  
- [ ] JSON‑/‑HTML‑**Report‑Generator**

### Frontend / GUI

- [ ] Dark‑Theme‑Layout (AppBar | Gallery | SidePanel)  
- [ ] Projekt‑Handling (Neu / Öffnen / Speichern)  
- [ ] **Masken‑Editor** (Zeichnen / Radieren / Undo‑Redo)  
- [ ] Zoom & Pan‑Werkzeuge  
- [ ] Fortschritts‑Modal für lange Tasks  
- [ ] Einstellungs‑Dialog (Modelle, Hardware, Pfade)  
- [ ] Mehrsprachigkeit (i18n)

### DevOps

- [ ] **start.py** Bootstrapping (Git pull → venv → npm install)  
- [ ] Portable **EXE‑Build** (PyInstaller)  
- [ ] Signierter Windows‑Installer  
- [ ] > 90 % Test‑Coverage  
- [ ] Automatisches Changelog‑Release (GitHub‑Action)

---

## **Offline‑Wissensbasis**

Eine kompakte Referenz für LLM‑Agents ohne Internet‑Zugriff.

### KI‑Modelle

| Schlüssel | Zweck | Repo / Datei | Größe | Status |
|-----------|-------|-------------|-------|--------|
| `anime_censor_detection` | Zensur‑BBox | `deepghs/anime_censor_detection` → `*/model.onnx` | 45 MB | ✅ |
| `sam_vit_hq` | Hochpräzise Masken | `syscv-community/sam-hq-vit-base` → `model.safetensors` | 380 MB | ✅ |
| `mobile_sam` | CPU‑/Low‑VRAM‑Masken | `yuval-alaluf/mobile_sam` → `*.pth` | 91 MB | ⬜ |
| `lama` | CNN‑Inpainting | PyPI: `iopaint[lama]` | 210 MB | ✅ |
| `sd2_inpaint` | Stable Diffusion 2‑Inpaint | `stabilityai/stable-diffusion-2-inpainting` | 1.5 GB | ⬜ |
| `revanimated` | Anime‑Inpaint (SD1.5) | `lnook/revAnimated-inpainting` | 2.1 GB | ✅ |

> Modelle werden beim ersten Start nach `models/` heruntergeladen (SHA‑256‑Check).

### Gepinnte NPM‑Pakete

| Paket | Version | Grund |
|-------|---------|-------|
| `electron-reload` | `2.0.2` (Fallback 2.0.0) | kompatibel mit Electron 28 |
| `electron-trpc` | `^0.7.1` | neuere Versionen nicht im Registry |
| `react-konva` | `19.0.7` | 19.0.24 nie veröffentlicht |
| `vite` | `5.x` | benötigt by Electron‑Vite‑Template |

---

## Schnellstart

```bash
git clone https://github.com/<EuerRepo>/DeZensur.git
cd DeZensur
python start.py          # erstellt venv, lädt Modelle, baut GUI
# Dev‑Modus:
python start.py --dev    # Hot‑Reload für Front‑ und Backend
```

---

## Ordnerstruktur

```
DeZensur/
├─ start.py              # Bootstrap‑Script
├─ requirements.txt
├─ gui/                  # Electron/React‑Frontend
├─ core/                 # Python‑Module
│  ├─ censor_detector.py │  sam & Inpainting etc.
│  └─ …
├─ models/               # Automatisch geladene Gewichte
└─ tests/
```

---

## Contributing

1. **Fork → Branch → PR** (Conventional Commits)  
2. Lint: `black`, `isort`, `flake8`  
3. Jeder PR braucht Tests (`pytest`)  
4. CI‑Pipeline muss grün sein  

---

## Lizenz

MIT – siehe [LICENSE](LICENSE)



## TODO‑Board 🗂️ (Stand 2025-07-19)

> **Hinweis:** Bitte in Pull‑Requests den Punkt abhaken (_- [x]_).  
> Jede Zeile besitzt daneben einen **🔬 Test‑Job** Indikator, der in  `tests/` nach­gezogen werden muss.

### 1️⃣ Core‑Backend
- [ ] **Projekt‑Loader/Saver** (`core/project.py`)
  - [ ] .dezproj Schema v1 (JSON + Assets)
  - [ ] Migration v1 → v2 Script
  - [ ] 🔬 `tests/core/test_project_roundtrip.py`
- [ ] **Censor‑Detector v2**
  - [ ] Konfigurierbare Schwelle + ROI‑Filtering
  - [ ] Batch‑CLI `detect-batch`
  - [ ] 🔬 `tests/detector/test_thresholds.py`
- [ ] **Segmenter Module**
  - [ ] SAM‑HQ GPU‑Pipeline
  - [ ] MobileSAM Fallback (CPU)
  - [ ] 🔬 `tests/segmenter/test_mobile_fallback.py`
- [ ] **Inpainter**
  - [ ] Diffusers Pipeline mit ControlNet‑Aux
  - [ ] Lama‑Cleaner Classical Fallback
  - [ ] 🔬 `tests/inpaint/test_seams.py`
- [ ] **Render‑Engine**
  - [ ] Async Tile‑Renderer
  - [ ] Abort/Resume Support
  - [ ] 🔬 `tests/render/test_resume.py`

### 2️⃣ Desktop‑GUI (Electron + React Konva)
- [ ] **Galerie‑View**
  - [ ] Drag‑&‑Drop Import
  - [ ] Lazy Thumb Generation (Worker)
  - [ ] 🔬 Playwright E2E `e2e/gallery.spec.ts`
- [ ] **Masken‑Editor**
  - [ ] Zeichen‑Tool, Radierer, Shortcut (⌘Z)
  - [ ] Zoom & Pan (Ctrl + Wheel)
  - [ ] 🔬 `e2e/editor.spec.ts`
- [ ] **Side‑Panel**
  - [ ] Kontextabhängige Property‑Leisten
  - [ ] Modell‑Selector Dropdown
  - [ ] 🔬 `e2e/sidepanel.spec.ts`
- [ ] **Einstellungs‑Dialog**
  - [ ] GPU Auswahl / CPU‑Fallback
  - [ ] Modelle nach­laden (+ Checksum)
  - [ ] 🔬 Unit `src/__tests__/settings.spec.tsx`
- [ ] **i18n**
  - [ ] Deutsch / Englisch JSON Bundles
  - [ ] Runtime‑Language Switch
  - [ ] 🔬 `tests/i18n/test_loader.py`

### 3️⃣ CLI‑&‑Batch‑Tools
- [ ] `dez detect <folder>` → JSON Report
- [ ] `dez inpaint --mask *.png`
- [ ] 🔬 `tests/cli/test_help.py`

### 4️⃣ DevOps & Release
- [ ] GitHub Actions
  - [ ] Matrix (windows‑latest / ubuntu‑latest)
  - [ ] Cashing von HF‑Modellen
- [ ] PyPI Build (`dezensor` Wheel)
- [ ] Windows x64 Portable `.exe` (PyInstaller + --add‑data assets)
- [ ] Code‑Signing Setup (signtool)
- [ ] 🔬 CI checks: mypy, Ruff, pytest‑cov ≥ 85 %

### 5️⃣ Dokumentation & Samples
- [ ] **Handbuch** (`docs/handbuch.md`)
- [ ] Demo Assets (blurred + unblurred)
- [ ] Video Walk‑Through (YouTube unlisted)

---

### 🧠 Offline Modell‑Katalog

| Key | Task | Format | Size | URL |
|-----|------|--------|------|-----|
| `anime_censor_detection` | Bounding‑Box NSFW | ONNX | 45 MB | deepghs/anime_censor_detection |
| `sam_vit_hq` | Segmentation HQ | SAFETENSORS | 380 MB | syscv-community/sam-hq-vit-base |
| `mobile_sam` | Segmentation CPU | PTH | 91 MB | yuval-alaluf/mobile_sam |
| `lama_cleaner` | Inpainting CNN | Wheel | 2 MB | iopaint[lama] |
| `stable_diffusion_inpaint` | Inpainting Diffusion | SAFETENSORS | 4 GB | runwayml/stable-diffusion-inpainting |

> **Tipp:** Modelle lassen sich über `python -m dezensor.fetch_model <key>` vorab offline cachen.

---
