import React from 'react';
import Preview from './Preview.jsx';

// Zentraler Arbeitsbereich
export default function CanvasArea({ activeImage }) {
  if (!activeImage) {
    return <div className="flex-1 flex items-center justify-center text-gray-400">Bild auswählen</div>;
  }
  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <div className="h-8 bg-bg-secondary flex items-center px-2 text-white text-sm">Tab {activeImage.id}</div>
      <div className="flex-1 bg-surface-card flex justify-center items-center">
        <Preview src={activeImage.path} imgId={activeImage.id} maskSrc="" />
      </div>
    </div>
  );
}
