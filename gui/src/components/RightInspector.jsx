import React from 'react';
import { useStore } from '../store.js';

// Unterstützte Inpainting-Modelle
const MODELS = ['lama', 'sd2_inpaint', 'revanimated'];

// Rechte Seitenleiste mit Eigenschaften & Einstellungen
export default function RightInspector() {
  const prefs = useStore((s) => s.prefs);
  const updatePrefs = useStore((s) => s.updatePrefs);

  function handleModelChange(e) {
    updatePrefs({ inpaintModel: e.target.value });
  }

  return (
    <div className="w-72 bg-bg-secondary text-white overflow-auto">
      <div className="p-2 font-semibold">Eigenschaften</div>
      <div className="p-2 text-xs">
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
