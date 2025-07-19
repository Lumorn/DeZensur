import React from 'react';
import { useStore } from '../store.js';

// Unterstützte Inpainting-Modelle
const MODELS = ['lama', 'sd2_inpaint', 'revanimated'];

// Rechte Seitenleiste mit Eigenschaften & Einstellungen
export default function RightInspector() {
  const prefs = useStore((s) => s.prefs);
  const updatePrefs = useStore((s) => s.updatePrefs);
  const images = useStore((s) => s.images);
  const activeId = useStore((s) => s.activeImageId);
  const activeImg = images.find((img) => img.id === activeId);

  function handleModelChange(e) {
    updatePrefs({ inpaintModel: e.target.value });
  }

  const imageProps = activeImg ? (
    <div className="p-2 text-xs" data-testid="img-props">
      <div className="mb-2">Bild-ID: {activeImg.id}</div>
      <div className="break-all">Pfad: {activeImg.path}</div>
    </div>
  ) : null;

  return (
    <div className="w-72 bg-bg-secondary text-white overflow-auto">
      <div className="p-2 font-semibold">Eigenschaften</div>
      {imageProps}
      <div className="p-2 text-xs" data-testid="model-select">
        <label className="block mb-2">Inpainting-Modell</label>
        <select
          aria-label="Inpainting-Modell auswählen"
          value={prefs.inpaintModel || 'lama'}
          onChange={handleModelChange}
          className="border p-1 text-black"
        >
          {MODELS.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
