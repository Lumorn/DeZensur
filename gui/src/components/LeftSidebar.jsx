import React from 'react';

// Seitenleiste mit Projektdateien und Historie
export default function LeftSidebar({ images }) {
  return (
    <div className="w-60 flex flex-col bg-bg-secondary text-white overflow-auto">
      <div className="p-2 font-semibold">Projekt-Dateien</div>
      <ul className="flex-1 px-2 space-y-2">
        {images.map((img) => (
          <li key={img.id} className="neu p-1 text-xs flex items-center gap-2">
            <img src={img.path} alt="thumb" className="w-10 h-10 object-cover" />
            <span>{img.id}</span>
          </li>
        ))}
      </ul>
      <div className="p-2">
        <input
          type="text"
          placeholder="Suchen"
          className="w-full text-black text-xs p-1"
        />
      </div>
    </div>
  );
}
