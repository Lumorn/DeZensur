import React from 'react';

// Befehlsleiste mit den Hauptaktionen
export default function CommandBar() {
  return (
    <div className="h-12 flex items-center justify-between px-2 bg-bg-primary text-white shadow">
      <div className="flex gap-2">
        <button className="neu px-2" aria-label="Neu">Neu</button>
        <button className="neu px-2" aria-label="Öffnen">Öffnen</button>
        <button className="neu px-2" aria-label="Bilder hinzufügen">Bilder</button>
        <button className="neu px-2" aria-label="Batch">Batch</button>
        <button className="neu px-2" aria-label="Export">Export</button>
      </div>
      <div className="flex items-center gap-4">
        <label className="flex items-center gap-1 text-xs">
          GPU
          <input type="checkbox" className="ml-1" />
        </label>
        <select className="bg-bg-secondary text-white text-xs">
          <option>DE</option>
          <option>EN</option>
        </select>
      </div>
    </div>
  );
}
