# DeZensur
![CI](https://github.com/Lumorn/DeZensur/actions/workflows/ci.yml/badge.svg)

**DeZensur** ist ein rein lokales Windows-(optionaler Cross-Platform-Support)-Tool‑Kit,  
das Zensur in Anime- und Comicbildern **vollautomatisch** erkennt und entfernt.  
Es kombiniert modernste Open‑Source‑Modelle:

* **anime_censor_detection** (ONNX) – erkennt Zensurbalken / Mosaik / Blur  
* **SAM-HQ** – präzise Maskensegmentierung auf Knopfdruck  
* **Inpainting-Modelle** (AnimeMangaInpainting, revAnimated, LaMa, Stable Diffusion) – rekonstruiert verdeckte Bereiche

> Alles läuft **offline** auf deiner GPU/CPU, keine Cloud‑Abhängigkeit.

---

## Projektziele

| Ziel | Status |
|------|--------|
| 🔄 Volle **Automatisierung** ohne manuelle Klicks | ⬜ |
| 🖼️ Intuitive **GUI** für Einzel‑ & Batch‑Modus (Electron + React) | ⬜ |
| 🧩 **Modular** – jeder Verarbeitungsschritt als eigenständiges Modul | ⬜ |
| ⚡ **Schnellstart**: `start.py` erledigt Git‑Pull + `pip install` | ✅ |
| 📦 **Selbst‑Updater** & automatischer Modell‑Download | ⬜ |
| 📝 Saubere **Code‑Doku**, **Tests** & **CI** | ✅ |
| 🧪 **Erweiterbar** (Video‑Support, neue Modelle, LoRAs) | ⬜ |

---

## Funktionsübersicht

1. **Bild-/Ordner‑Import** über `File → Add Images…` oder Drag & Drop  
2. **Automatische Zensur‑Erkennung** (Bounding‑Boxen via `anime_censor_detection`)  
3. **Masken‑Verfeinerung** mit SAM‑HQ  
4. **Inpainting** der Maskenbereiche (modell‑wählbar)  
5. **Batch‑Modus** für ganze Verzeichnisse  
6. **Protokoll & Export** (Original, Maske, Ergebnis, Log)  
7. **Voll funktionsfähige Buttons** für Projektverwaltung und Fenstersteuerung (ab Version 1.7.8)  
   - Das Ordnersymbol in der App‑Bar setzt nun den Arbeitsordner.  
   - Der ▶‑Knopf startet die Zensurerkennung via tRPC.  

---

## TODO‑Liste (vollständig)

> **So nutzt du die Liste:**  
> Jede Aufgabe ist als GitHub‑Checkbox angelegt.  
> Wenn du etwas fertiggestellt hast, ersetze das `[ ]` durch `[x]` und committe die Änderung – GitHub zeigt sie dann ✅ an.

### 1 — Kern‑Pipeline
- [ ] **Bild‑Import** (Dialog & Drag‑&‑Drop) landet in `originals/`
- [ ] **Projektverwaltung** (Neu / Öffnen / Speichern `.dezproj`)
- [ ] **Zensur‑Erkennung** (anime_censor_detection) aus GUI triggern
- [ ] **Maske verfeinern** mit SAM‑HQ
- [ ] **Masken‑Editor** (Konva) inkl. Undo / Redo
- [ ] **Inpainting** (LaMa, revAnimated, SD2) inkl. Prompt‑Eingabe
- [ ] **GPU/CPU Auto‑Fallback** & Modell‑Auswahl
- [ ] **Batch‑Modus** (ganze Ordner, Parallel‑Worker)
- [ ] **Fortschritts‑Overlay** & Job‑Queue

### 2 — GUI & UX
- [ ] Desktop‑Layout mit Titelleiste / Menü / Sidepanel
- [ ] Galerie‑Komponente mit Thumbnails
- [ ] Sidepanel‑Einstellungen (Modelle, Output‑Ordner, Anatomie‑Tags)
- [ ] Einstellungen speichern / laden pro Projekt
- [ ] Kontext‑Menü & Shortcuts (Ctrl+O, Ctrl+S, …)
- [ ] Mehrsprachigkeit (i18n) – EN/DE

### 3 — Erweiterungen
- [ ] **Video‑Pipeline** (ffmpeg, frame‑by‑frame)
- [ ] **Self‑Updater** (Python + npm Abhängigkeitsmanager)
- [ ] **Portable EXE** (PyInstaller) & Cross‑Platform‑Builds
- [ ] **Plugin‑System** (LoRA‑/Model‑Hot‑Swap)

### 4 — Qualität
- [ ] Automatische Modell‑Downloads mit SHA‑Check
- [ ] Bootstrap‑Script `start.py` inkl. venv & Git‑Pull
- [ ] End‑to‑End‑Tests (Playwright)
- [ ] Unit‑/Integration‑Tests (PyTest) für alle Module
- [ ] CI/CD Release‑Pipeline (GitHub Actions, Signierte Builds)

---

## Lizenz
MIT – siehe [LICENSE](LICENSE).
