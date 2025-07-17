import React from 'react';

// Obere Titelleiste mit Logo und Fensterknöpfen
export default function TitleBar({ projectName }) {
  return (
    <div className="h-8 flex items-center justify-between px-2 bg-bg-secondary text-white select-none">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-accent-primary rounded-full flex items-center justify-center">
          <span className="text-sm">\u{1F4F7}</span>
        </div>
        <span className="text-sm">DeZensur › {projectName || 'Kein Projekt'}</span>
      </div>
      <div className="flex gap-2">
        <button className="w-3 h-3 rounded-full bg-red-500" aria-label="Schließen"></button>
        <button className="w-3 h-3 rounded-full bg-yellow-500" aria-label="Minimieren"></button>
        <button className="w-3 h-3 rounded-full bg-green-500" aria-label="Maximieren"></button>
      </div>
    </div>
  );
}
