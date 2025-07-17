import React from 'react';
import Gallery from './Gallery';

// Anzeige der Thumbnails im Hauptbereich
export default function GalleryPane() {
  return (
    <section className="flex-1 overflow-auto bg-gray-900 text-white">
      <Gallery />
    </section>
  );
}
