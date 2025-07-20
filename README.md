# DeZensur

![CI](https://github.com/Lumorn/DeZensur/actions/workflows/ci.yml/badge.svg)

**DeZensur** ist ein rein lokales Toolkit zur automatischen Entfernung von Zensur in Anime‑ und Comicbildern.  
Alle Modelle laufen **offline** auf deiner GPU / CPU – keine Cloud‑Abhängigkeiten.

Eine ausführliche Schritt‑für‑Schritt‑Anleitung findest du im [Handbuch](docs/handbuch.md).

---

## Projektziele

| Ziel | Status |
|------|--------|
| 🔄 Volle **End‑to‑End‑Automatisierung** | ⬜ |
| 🖼️ Intuitive **Electron + React GUI** | ⬜ |
| 🧩 **Modulare Pipeline** (Detection → Segmentation → Inpainting) | ⬜ |
| ⚡ **start.py** erledigt Git + `pip install` + GUI‑Build | ✅ |
| 📦 **Self‑Updater** & automatischer Modell‑Download | ⬜ |
| 📝 **Tests + CI** (black, isort, flake8, ruff, mypy, pytest-cov) | ✅ |
| 🧪 **Erweiterbar** (Video‑Support, LoRA‑Modelle) | ⬜ |

---

## **Aktuelle TODO‑Liste**  
*Markdown‑Checkboxen können direkt in GitHub oder VS Code abgehakt werden.*

-### Backend / Core

- [x] Integration **anime_censor_detection** (ONNX)
- [x] HQ‑**SAM** Segmenter (`sam_vit_hq`)
- [x] Option **MobileSAM** für schwache Hardware
- [x] Anatomie‑Tag‑Ergänzer für bessere Prompts
- [x] Dynamischer **Model‑Manager** (Download + Version‑Check)
- [x] **Batch‑Runner** mit Fortschritts‑Overlay
- [x] JSON‑/‑HTML‑**Report‑Generator**

### Frontend / GUI

- [x] Dark‑Theme‑Layout (AppBar | Gallery | SidePanel)
- [x] Projekt‑Handling (Neu / Öffnen / Speichern)
- [x] **Masken‑Editor** (Zeichnen / Radieren / Undo‑Redo)
- [x] Zoom & Pan‑Werkzeuge
- [x] Fortschritts‑Modal für lange Tasks
- [x] Einstellungs‑Dialog (Modelle, Hardware, Pfade)
- [x] Mehrsprachigkeit (i18n)

### DevOps

- [x] **start.py** Bootstrapping (Git pull → venv → npm install)
- [x] Portable **EXE‑Build** (PyInstaller)
- [ ] Signierter Windows‑Installer  
- [x] > 90 % Test‑Coverage
- [x] Automatisches Changelog‑Release (GitHub‑Action)

---

## **Offline‑Wissensbasis**

Eine kompakte Referenz für LLM‑Agents ohne Internet‑Zugriff.

### KI‑Modelle

| Schlüssel | Zweck | Repo / Datei | Größe | Status |
|-----------|-------|-------------|-------|--------|
| `anime_censor_detection` | Zensur‑BBox | `deepghs/anime_censor_detection` → `*/model.onnx` | 45 MB | ✅ |
| `sam_vit_hq` | Hochpräzise Masken | `syscv-community/sam-hq-vit-base` → `model.safetensors` | 380 MB | ✅ |
| `mobile_sam` | CPU‑/Low‑VRAM‑Masken | `yuval-alaluf/mobile_sam` → `*.pth` | 91 MB | ✅ |
| `lama` | CNN‑Inpainting | PyPI: `iopaint[lama]` | 210 MB | ✅ |
| `sd2_inpaint` | Stable Diffusion 2‑Inpaint | `stabilityai/stable-diffusion-2-inpainting` | 1.5 GB | ⬜ |
| `revanimated` | Anime‑Inpaint (SD1.5) | `lnook/revAnimated-inpainting` | 2.1 GB | ✅ |

> Modelle werden beim ersten Start nach `models/` heruntergeladen
> und falls vorhanden per SHA‑256 überprüft.

### Gepinnte NPM‑Pakete

| Paket | Version | Grund |
|-------|---------|-------|
| `electron-reload` | `1.5.0` (Fallback 2.0.0) | kompatibel mit Electron 28 |
| `electron` | `28.2.0` | stable Release |
| `electron-trpc` | `0.7.1` | neuere Versionen nicht im Registry |
| `react-konva` | `19.0.7` | 19.0.24 nie veröffentlicht |
| `vite` | `5.x` | benötigt by Electron‑Vite‑Template |

Die IPC-Anbindung erfolgt über `exposeElectronTRPC` im Preload und einen
`createTRPCProxyClient` mit `ipcLink()` im Renderer.

---

## Schnellstart

```bash
git clone https://github.com/<EuerRepo>/DeZensur.git
cd DeZensur
python start.py          # erstellt venv, lädt Modelle, baut GUI
# Dev‑Modus:
python start.py --dev    # Hot‑Reload für Front‑ und Backend
# Build erzwingen:
python start.py --force-build
```

Unter Windows kannst du das Programm auch bequem per Doppelklick starten.
Nutze dazu entweder direkt `start.py` oder das neue Skript `start.cmd`.

Sollte nach dem Start nur ein weißes Fenster erscheinen, fehlt oder
beschädigt oft der Frontend‑Build. `start.py` erkennt solche Fälle nun und
erstellt die Dateien automatisch neu. Alternativ kannst du jederzeit
`python scripts/repair_gui.py` ausführen oder im Ordner `gui/` ein
`npm run build` anstoßen. Mit `python start.py --force-build` lässt sich der
Build ebenfalls erzwingen. Starte die GUI nicht direkt mit `npm start`, wenn
kein Build vorhanden ist – sonst bleibt das Fenster leer.

### Sprache umschalten

Oben rechts in der GUI kannst du zwischen **DE** und **EN** wählen. Die zugehörigen
JSON-Dateien findest du unter `gui/src/i18n/`. Mit
`python scripts/sync_i18n.py` stellst du sicher, dass beide Dateien dieselben
Schlüssel enthalten.

### Theme wechseln

Über die Schaltfläche neben dem GPU-Schalter lässt sich zwischen hellem und dunklem Layout
umschalten. Die Farbwerte sind in `gui/src/tailwind.css` definiert.

### Masken-Editor

Im integrierten Masken-Editor kannst du Bereiche zeichnen oder radieren. Über die
Werkzeugleiste lässt sich die Pinselgröße anpassen und per Undo/Redo rückgängig
machen. Halte **Strg** gedrückt und nutze das Mausrad zum Zoomen. Mit gedrückter
**Leertaste** lässt sich die Ansicht verschieben.

### Bilder importieren

Bilder kannst du direkt per Drag-&-Drop in die Galerie ziehen. Alternativ öffnest du
**File → Add Images…** oder drückst **Ctrl+O**.
Beim ersten Anzeigen erzeugt ein Web Worker automatisch verkleinerte Vorschaubilder.
Beispielbilder findest du im Ordner `demo_assets/`.

### Side-Panel

Nach dem Anklicken eines Bildes erscheinen rechts dessen Eigenschaften
(ID und Dateiname). Dort wählst du auch das Inpainting-Modell aus.

### Batch-Reports erstellen

Nach einem Batch-Lauf kann ein zusammenfassender Bericht erzeugt werden.

```bash
python generate_report.py projekt.dezproj 20240719 --report batch.json --html batch.html
```
Der JSON- und optional der HTML-Report liegen anschließend im angegebenen Pfad.

### Tile-Renderer

Die Render-Engine zerlegt Bilder in Kacheln und kann jederzeit pausiert werden.
Beim erneuten Start setzt sie den letzten Stand fort.

### Zensur-Scan per CLI

Mit dem Skript `dez.py` lässt sich ein kompletter Ordner analysieren:

```bash
python dez.py detect bilder/ --out scan.json --roi 0.3,0.3,0.7,0.7
```
Der Parameter `--roi` begrenzt die Suche optional auf einen Bereich
(x1,y1,x2,y2, Werte 0‑1). Der JSON-Bericht listet alle gefundenen Boxen pro Datei auf.

Alternativ kann der Befehl auch als `detect-batch` ausgeführt werden:

```bash
python dez.py detect-batch bilder/ --out scan.json
```

### Inpainting per CLI

Ein einzelnes Bild kann direkt über die Kommandozeile bearbeitet werden:

```bash
python dez.py inpaint bild.png --mask maske.png --out ergebnis.png
```
Das Ergebnisbild landet im angegebenen Pfad. Alternativ kann mit dem neuen Modell
`sd_controlnet` gearbeitet werden:

```bash
python dez.py inpaint bild.png --mask maske.png --model sd_controlnet --out ergebnis.png
```

### Modelle vorab herunterladen

Zum Offline-Betrieb können die benötigten Gewichte schon vorher geladen werden:

```bash
python -m dezensor.fetch_model sam_vit_hq
```
Der Pfad zum heruntergeladenen Modell wird nach Abschluss ausgegeben.

### GPU- oder CPU-Modus wählen

Standardmäßig nutzt DeZensur die GPU, falls verfügbar. Mit der
Umgebungsvariable `DEZENSUR_DEVICE` lässt sich dies überschreiben:

```bash
DEZENSUR_DEVICE=cpu python dez.py detect bilder/
```
Mögliche Werte sind `gpu` oder `cpu`.

### Projektdateien aktualisieren

Beim Laden einer alten Projektdatei wird diese automatisch auf Schema v2 gehoben:

```python
from core.project import Project

proj = Project.load("meinprojekt.dezproj")
proj.save()  # schreibt im neuen Format
```

### Wheel erzeugen

Mit dem Standardwerkzeug **build** kann ein installierbares Wheel erstellt werden:

```bash
pip install build
python -m build
```
Das Paketarchiv landet danach im Ordner `dist/`.

### Windows-EXE erzeugen

Mit **PyInstaller** lässt sich eine portable Windows-EXE erzeugen. Das
Skript `scripts/build_windows_exe.py` übernimmt den Aufruf:

```bash
pip install pyinstaller
python scripts/build_windows_exe.py
```
Die fertige Datei befindet sich anschließend in `dist/dezensor.exe`.

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
2. Lint: `black`, `isort`, `flake8`, `ruff`, `mypy`
3. Zeigt die CI "Imports are incorrectly sorted" an, führe `isort .` aus;
   einzelne Dateien korrigierst du mit `isort core/dep_manager.py core/inpainter.py`
4. Jeder PR braucht Tests (`pytest`)
5. CI‑Pipeline muss grün sein

---

## Lizenz

MIT – siehe [LICENSE](LICENSE)



## TODO‑Board 🗂️ (Stand 2025-07-19)

> **Hinweis:** Bitte in Pull‑Requests den Punkt abhaken (_- [x]_).  
> Jede Zeile besitzt daneben einen **🔬 Test‑Job** Indikator, der in  `tests/` nach­gezogen werden muss.

### 1️⃣ Core‑Backend
- [x] **Projekt‑Loader/Saver** (`core/project.py`)
  - [x] .dezproj Schema v1 (JSON + Assets)
  - [x] Migration v1 → v2 Script
  - [x] 🔬 `tests/core/test_project_roundtrip.py`
- [x] **Censor‑Detector v2**
  - [x] Konfigurierbare Schwelle + ROI‑Filtering
  - [x] Batch‑CLI `detect-batch`
  - [x] 🔬 `tests/detector/test_thresholds.py`
- [x] **Segmenter Module**
  - [x] SAM‑HQ GPU‑Pipeline
  - [x] MobileSAM Fallback (CPU)
  - [x] 🔬 `tests/segmenter/test_mobile_fallback.py`
  - [x] 🔬 `tests/segmenter/test_gpu_pipeline.py`
- [x] **Inpainter**
  - [x] Diffusers Pipeline mit ControlNet‑Aux
  - [x] Lama‑Cleaner Classical Fallback
  - [x] 🔬 `tests/inpaint/test_seams.py`
- [x] **Render‑Engine**
  - [x] Async Tile‑Renderer
  - [x] Abort/Resume Support
  - [x] 🔬 `tests/render/test_resume.py`

### 2️⃣ Desktop‑GUI (Electron + React Konva)
- [ ] **Galerie‑View**
  - [x] Drag‑&‑Drop Import
  - [x] Lazy Thumb Generation (Worker)
  - [x] 🔬 Playwright E2E `e2e/gallery.spec.ts`
  - [x] **Masken‑Editor**
  - [x] Zeichen‑Tool, Radierer, Shortcut (⌘Z)
  - [x] Zoom & Pan (Ctrl + Wheel)
  - [x] 🔬 `e2e/editor.spec.ts`
- [x] **Side‑Panel**
  - [x] Kontextabhängige Property‑Leisten
  - [x] Modell‑Selector Dropdown
  - [x] 🔬 `e2e/sidepanel.spec.ts`
- [x] **Einstellungs‑Dialog**
  - [x] GPU Auswahl / CPU‑Fallback
  - [x] Modelle nach­laden (+ Checksum)
  - [x] 🔬 Unit `src/__tests__/settings.spec.tsx`
 - [x] **i18n**
  - [x] Deutsch / Englisch JSON Bundles
  - [x] Runtime‑Language Switch
  - [x] 🔬 `tests/i18n/test_loader.py`

### 3️⃣ CLI‑&‑Batch‑Tools
- [x] `dez detect <folder>` → JSON Report
- [x] `dez inpaint --mask *.png`
- [x] 🔬 `tests/cli/test_help.py`

### 4️⃣ DevOps & Release
- [x] GitHub Actions
  - [x] Matrix (windows‑latest / ubuntu‑latest)
  - [x] Cashing von HF‑Modellen
 - [x] PyPI Build (`dezensor` Wheel)
   - [x] Windows x64 Portable `.exe` (PyInstaller + --add‑data assets)
  - [ ] Code‑Signing Setup (signtool)
 - [x] 🔬 CI checks: mypy, Ruff, pytest‑cov ≥ 85 %

-### 5️⃣ Dokumentation & Samples
- [x] **Handbuch** (`docs/handbuch.md`)
- [x] Demo Assets (blurred + unblurred)
- [ ] Video Walk‑Through (YouTube unlisted)

### 🛠️ DeZensur Bug- & Fix-Liste (Stand 2025-07-19)
_Nur Punkte, die **noch offen** sind – als kopier- & abhakbare Markdown-Checkboxen._

#### 1️⃣ GUI / Electron + React
- [x] **Frontend-Build fehlt**
  - Datei `gui/dist/index.html` wird nicht erzeugt → weißes Fenster.  
  - **Fix:** `npm run build` (oder `python start.py`) in _gui/_ automatisieren.  
  - **Tests:** Playwright `e2e/window-load.spec.ts` sorgt dafür, dass `document.title` ≠ "" ist.

- [x] **Preload-Skript (`gui/electron/preload.js`) fehlt**
  - `main.js` erwartet `preload.js` mit `contextBridge`.  
  - **Fix:** neue Datei mit  
    ```js
    const { contextBridge, ipcRenderer } = require('electron');
    const { exposeElectronTRPC } = require('electron-trpc/preload');
    exposeElectronTRPC({ ipcRenderer });
    ```  
  - **Tests:** Jest `preload.test.ts` prüft, dass `window.trpc` existiert.

- [x] **Electron-TRPC Client nicht initialisiert**
  - Renderer hat keinen `createTRPCProxyClient`.  
  - **Fix:** in `gui/src/main.tsx`  
    ```ts
    import { createTRPCProxyClient, ipcLink } from 'electron-trpc/client';
    export const trpc = createTRPCProxyClient<AppRouter>({ links:[ipcLink()] });
    ```  
  - **Tests:** React-Testing-Library `trpc.spec.tsx` mockt Ping-Procedure.

- [x] **Falscher Vite-Alias**
  - `@` zeigt auf `./src/renderer`, Code liegt in `./src`.  
  - **Fix:** in `gui/vite.config.ts`  
    ```ts
    resolve:{ alias:{ '@': path.resolve(__dirname,'./src') } }
    ```  

- [x] **Tailwind CSS nicht konfiguriert**
  - Klassen wie `bg-bg-primary` ohne `tailwind.config.js`.  
  - **Fix:** Config mit `content:['./src/**/*.{ts,tsx}']`, Theme-Farben definieren.  
  - **Tests:** Storybook Screenshot-Diff.

- [x] **Incompatible NPM-Versions**
  - `electron-reload` ^1.5.0 → 1.5.0
  - `electron-trpc` ^0.11.0 → 0.7.1 (letzte veröffentlichte)  
  - `react-konva` ^19.0.7 → **19.0.7** (Caret entfernen)  
  - `electron` “latest” → 28.2.x pinnen
  - **Fix:** `package.json` & `package-lock.json` anpassen; `npm ci` in CI.

- [x] **electron-trpc Preload Import fehlerhaft**
  - `window.electronTRPC` fehlte, weil `exposeElectronTRPC` aus `electron-trpc/main` aufgerufen wurde.
  - **Fix:** `gui/src/main/preload.ts` nutzt nun `electron-trpc/preload` und übergibt `ipcRenderer`.

- [ ] **Galerie-View unvollständig**  
  - Thumbnails werden generiert, UI zeigt aber nichts an.  
  - **Fix:** React-Komponente `GalleryView` fertigstellen (Grid, Select, Open).  
  - **Tests:** E2E `e2e/gallery.spec.ts` (Drag-&-Drop, Klick).

-#### 2️⃣ Backend / Core
- [x] **Stable-Diffusion-Inpainting fehlt**
  - Auswahl `sd2_inpaint` führt zu 404.  
  - **Fix:** Diffusers-Pipeline (`StableDiffusionInpaintPipeline.from_pretrained`) integrieren.  
  - **Tests:** `tests/inpaint/test_sd2.py` (dummy-mask).

- [x] **tsconfig.json fehlt**
  - TypeScript-Abhängigkeit ohne Config → Vite-Errors.  
  - **Fix:** Minimal `tsconfig.json` per `tsc --init`, Pfade auf _src/_ setzen.

- [x] **Project-IPC-Handler (`gui/electron/project.js`) fehlt**
  - `ProjectIPC(ipcMain)` Aufrufe verpuffen.  
  - **Fix:** Handler implementieren: open/save dialog, returns path.  
  - **Tests:** Spectron `ipc-project.spec.ts`.

 - [x] **i18n-Bundles prüfen**
  - Fehlende Keys lösen React-Warnungen aus.
  - **Fix:** `de.json` & `en.json` per script synchronisieren.
  - **Tests:** Jest `i18n.keys.spec.ts` (Snapshot aller Keys).

 - [x] **Model-Manager Checksummen & Pfade**
    - Torch 2.2.x ok, aber future 2.3 bricht ONNX.
    - **Fix:** `requirements.txt` mit `torch<2.3`. SHA-256 in `models.yml`.
    - **Tests:** `tests/models/test_checksum.py`.

#### 3️⃣ Dev-Scripts & CI
- [x] **start.py überspringt _npm install_** wenn `SKIP_NPM_INSTALL` gesetzt
  - **Fix:** Flag nur für CI erlauben; Warnung im Terminal.
  - **Tests:** `tests/test_start.py::test_should_skip_npm_install_*`.

- [x] **Jest unterstützt ESModule-Imports**
  - Beim CI-Lauf erschienen "Cannot use import statement outside a module".
  - **Fix:** `gui/babel.config.cjs` und `gui/jest.config.cjs` konfigurieren Babel-Jest.
  - **Tests:** `npm test` läuft nun ohne Syntaxfehler.
- [x] **GalleryStore filtert doppelte Pfade**
  - `addImages()` legte bei mehrfachen Pfaden auch Duplikate an.
  - **Fix:** In `useGalleryStore.ts` werden Pfade vorab dedupliziert.
  - **Tests:** `galleryStore.test.ts` prüft die einzigartige Anzahl korrekt.
- [x] **Imports sind konsistent sortiert**
  - CI schlug wegen falsch angeordneter `import`-Blöcke fehl.
  - **Fix:** `isort .` stellt eine einheitliche Reihenfolge sicher.
- [x] **PyYAML als Testabhängigkeit**
  - Pytest konnte `yaml` nicht finden.
  - **Fix:** Paket `PyYAML` zu den Abhängigkeiten hinzugefügt.
- [x] **Importreihenfolge in zwei Modulen gefixt**
  - `core/dep_manager.py` und `core/inpainter.py` mussten erneut sortiert werden.
  - **Fix:** `isort core/dep_manager.py core/inpainter.py` ausführen.


- [ ] **Code-Signing Pipeline**
  - Windows EXE unsigniert → SmartScreen-Warnung.  
  - **Fix:** GH Action mit `signtool` / EV-Zertifikat einrichten.  
  - **Tests:** Artifact-Hash-Check nach Signierung.



---

### 🧠 Offline Modell‑Katalog

| Key | Task | Format | Size | URL |
|-----|------|--------|------|-----|
| `anime_censor_detection` | Bounding‑Box NSFW | ONNX | 45 MB | deepghs/anime_censor_detection |
| `sam_vit_hq` | Segmentation HQ | SAFETENSORS | 380 MB | syscv-community/sam-hq-vit-base |
| `mobile_sam` | Segmentation CPU | PTH | 91 MB | yuval-alaluf/mobile_sam |
| `lama_cleaner` | Inpainting CNN | Wheel | 2 MB | iopaint[lama] |
| `stable_diffusion_inpaint` | Inpainting Diffusion | SAFETENSORS | 4 GB | runwayml/stable-diffusion-inpainting |
| `controlnet_canny` | ControlNet Hint | SAFETENSORS | 1 GB | lllyasviel/control_v11p_sd15_canny |

 > **Tipp:** Modelle lassen sich über `python -m dezensor.fetch_model <key>` vorab offline cachen. Das Skript verwendet den internen Downloader mit Versions- und Prüfsummenprüfung.

Die zugehörigen SHA-256-Werte und Dateinamen sind in `models.yml` hinterlegt und
können dort angepasst werden. Fehlt ein Wert, entfällt die Prüfung.

---
