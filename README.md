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

- [x] Integration **anime_censor_detection** (ONNX)  
- [x] HQ‑**SAM** Segmenter (`sam_vit_hq`)  
- [ ] Option **MobileSAM** für schwache Hardware  
- [ ] Anatomie‑Tag‑Ergänzer für bessere Prompts  
- [ ] Dynamischer **Model‑Manager** (Download + Version‑Check)  
- [ ] **Batch‑Runner** mit Fortschritts‑Overlay  
- [ ] JSON‑/‑HTML‑**Report‑Generator**

### Frontend / GUI

- [x] Dark‑Theme‑Layout (AppBar | Gallery | SidePanel)  
- [x] Projekt‑Handling (Neu / Öffnen / Speichern)  
- [ ] **Masken‑Editor** (Zeichnen / Radieren / Undo‑Redo)  
- [ ] Zoom & Pan‑Werkzeuge  
- [ ] Fortschritts‑Modal für lange Tasks  
- [ ] Einstellungs‑Dialog (Modelle, Hardware, Pfade)  
- [ ] Mehrsprachigkeit (i18n)

### DevOps

- [x] **start.py** Bootstrapping (Git pull → venv → npm install)  
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
