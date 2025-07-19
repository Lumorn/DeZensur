import React from 'react';
import { useGalleryStore } from '../stores/useGalleryStore';

// Rechte Seitenleiste mit Accordions
export default function SidePanel() {
  const images = useGalleryStore((s) => s.images);
  const selectedId = useGalleryStore((s) => s.selectedId);
  const active = images.find((img) => img.id === selectedId);

  return (
    <aside className="w-72 bg-gray-800 text-white p-2 overflow-auto">
      <div className="font-semibold mb-2">Eigenschaften</div>
      {active ? (
        <div data-testid="img-props" className="text-xs">
          <div className="mb-1">ID: {active.id}</div>
          <div className="break-all">{active.name}</div>
        </div>
      ) : (
        <div className="text-xs text-gray-400">Kein Bild ausgewählt</div>
      )}
    </aside>
  );
}
