import React from 'react';

// Rechte Seitenleiste mit Eigenschaften & Einstellungen
export default function RightInspector() {
  return (
    <div className="w-72 bg-bg-secondary text-white overflow-auto">
      <div className="p-2 font-semibold">Eigenschaften</div>
      <div className="p-2 text-xs">Bild-Metadaten...</div>
    </div>
  );
}
