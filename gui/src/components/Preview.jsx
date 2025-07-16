// Großansicht eines ausgewählten Bildes
import React from 'react';

export default function Preview({ src }) {
  return (
    <div className="flex justify-center items-center h-full">
      {src && <img src={src} alt="preview" className="max-h-full" />}
    </div>
  );
}
