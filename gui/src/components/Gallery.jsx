// Zeigt importierte Bilder als Thumbnails an
import React from 'react';

export default function Gallery({ images }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-2 p-2">
      {images.map((img) => (
        <img key={img.id} src={img.path} alt="thumb" className="w-full" />
      ))}
    </div>
  );
}
