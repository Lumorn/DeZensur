import React from 'react';
import { useInView } from 'react-intersection-observer';
import { ImageMeta, useGalleryStore } from '../stores/useGalleryStore';

// Einzelnes Thumbnail in der Galerie
export default function Thumb({ image }: { image: ImageMeta }) {
  const { ref, inView } = useInView({ triggerOnce: true });
  const selectedId = useGalleryStore((s) => s.selectedId);
  const select = useGalleryStore((s) => s.select);
  return (
    <button
      ref={ref}
      onClick={() => select(image.id)}
      className={`w-40 h-40 rounded-lg shadow-sm overflow-hidden ${
        selectedId === image.id ? 'ring-2 ring-blue-500' : ''
      }`}
    >
      {inView && (
        <img
          src={image.path}
          alt={image.name}
          className="w-full h-full object-cover"
        />
      )}
    </button>
  );
}

