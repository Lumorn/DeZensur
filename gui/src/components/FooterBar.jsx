import React from 'react';

// Statusleiste am unteren Rand
export default function FooterBar() {
  return (
    <div className="h-8 flex items-center justify-between px-2 bg-bg-secondary text-white text-xs">
      <div className="flex-1">Fortschritt...</div>
      <div className="flex-1 text-center">Tipp: STRG+Z / STRG+Y</div>
      <div className="flex-1 text-right">FPS 60</div>
    </div>
  );
}
