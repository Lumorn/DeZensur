// Großansicht eines ausgewählten Bildes
import React, { useState } from 'react';
import MaskEditor from './MaskEditor.jsx';

export default function Preview({ src, maskSrc, imgId }) {
  const [showEditor, setShowEditor] = useState(false);
  const [editedMask, setEditedMask] = useState(null);

  function saveMask() {
    if (editedMask) {
      window.maskEditor.saveMask(imgId, editedMask);
    }
    setShowEditor(false);
  }

  return (
    <div className="flex justify-center items-center h-full relative">
      {src && <img src={src} alt="preview" className="max-h-full" />}
      {src && (
        <button className="btn absolute top-2 right-2" onClick={() => setShowEditor(true)}>
          Maske editieren
        </button>
      )}
      {showEditor && (
        <div className="absolute inset-0 bg-black/50 flex justify-center items-center">
          <div className="bg-white p-2">
            <MaskEditor imgSrc={src} maskSrc={maskSrc} onMaskChange={setEditedMask} />
            <div className="flex justify-end gap-2 mt-2">
              <button className="btn" onClick={() => setShowEditor(false)}>Abbrechen</button>
              <button className="btn btn-primary" onClick={saveMask}>Speichern</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
