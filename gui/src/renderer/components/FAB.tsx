import React from 'react';
import { useGalleryStore } from '../stores/useGalleryStore';

// Floating Action Button Bar
export default function FAB() {
  const selectedId = useGalleryStore((s) => s.selectedId);
  const images = useGalleryStore((s) => s.images);

  // Startet die Verarbeitung des ausgewählten Bildes
  async function handleRun() {
    const img = images.find((i) => i.id === selectedId);
    if (!img) {
      alert('Bitte zuerst ein Bild auswählen.');
      return;
    }
    await window.api.backend.call('/detect', { path: img.path.replace('file://', '') });
    alert('Erkennung abgeschlossen.');
  }

  return (
    <div className="fixed bottom-4 right-4 space-y-2">
      <button className="rounded-full p-3 bg-accent text-white" onClick={handleRun}>▶</button>
    </div>
  );
}
