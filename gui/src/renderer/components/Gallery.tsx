import React from 'react';
import Thumb from './Thumb';
import { useGalleryStore } from '../stores/useGalleryStore';
import { useProjectStore } from '../stores/useProjectStore';

// Zeigt die Bildliste als Grid an
export default function Gallery() {
  const images = useGalleryStore((s) => s.images);
  const addImages = useGalleryStore((s) => s.addImages);
  const addProjImages = useProjectStore((s) => s.addImages);

  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    const paths = Array.from(e.dataTransfer.files)
      .map((f: any) => f.path)
      .filter(Boolean);
    if (paths.length) {
      addImages(paths);
      addProjImages(paths);
    }
  }

  const content = images.length ? (
    <div className="grid grid-cols-[repeat(auto-fill,minmax(180px,1fr))] gap-4 p-4">
      {images.map((img) => (
        <Thumb key={img.id} image={img} />
      ))}
    </div>
  ) : (
    <div className="p-4 text-center text-sm text-gray-400">
      Drag &amp; Drop images or use <strong>File → Add Images…</strong>
    </div>
  );

  return (
    <div
      data-testid="gallery"
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      className="h-full"
    >
      {content}
    </div>
  );
}

