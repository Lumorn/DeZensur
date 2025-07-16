// Werkzeugleiste für den Masken-Editor
import React from 'react';

export default function MaskToolbar({ mode, setMode, brush, setBrush, undo, redo }) {
  return (
    <div className="flex gap-2 p-2">
      <button className={`btn ${mode === 'draw' ? 'btn-primary' : ''}`} onClick={() => setMode('draw')} aria-label="Zeichnen">✏️</button>
      <button className={`btn ${mode === 'erase' ? 'btn-primary' : ''}`} onClick={() => setMode('erase')} aria-label="Radieren">🩹</button>
      <button className="btn" onClick={() => setBrush(brush + 10)} aria-label="Brush größer">➕</button>
      <button className="btn" onClick={() => setBrush(Math.max(1, brush - 10))} aria-label="Brush kleiner">➖</button>
      <button className="btn" onClick={undo} aria-label="Undo">↩️</button>
      <button className="btn" onClick={redo} aria-label="Redo">↪️</button>
    </div>
  );
}
