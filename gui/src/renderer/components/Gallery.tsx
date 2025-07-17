import React from 'react';
import Thumb from './Thumb';
import { useGalleryStore } from '../stores/useGalleryStore';

// Zeigt die Bildliste als Grid an
export default function Gallery() {
  const images = useGalleryStore((s) => s.images);
  if (!images.length) {
    return (
      <div className="p-4 text-center text-sm text-gray-400">
        Drag &amp; Drop images or use <strong>File → Add Images…</strong>
      </div>
    );
  }
  return (
    <div className="grid grid-cols-[repeat(auto-fill,minmax(180px,1fr))] gap-4 p-4">
      {images.map((img) => (
        <Thumb key={img.id} image={img} />
      ))}
    </div>
  );
}

