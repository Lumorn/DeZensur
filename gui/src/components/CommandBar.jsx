import React from 'react';
import { useStore } from '../store.js';

// Befehlsleiste mit den Hauptaktionen
export default function CommandBar() {
  // Zugriff auf den globalen Zustand
  const project = useStore((s) => s.project);
  const setProject = useStore((s) => s.setProject);
  const images = useStore((s) => s.images);
  const setImages = useStore((s) => s.setImages);
  const [gpu, setGpu] = React.useState(true);

  // Legt ein neues Projekt an
  async function handleNew() {
    const folder = await window.api.openFolderDialog();
    if (folder && folder[0]) {
      const data = await window.api.project.new(folder[0]);
      setProject(data);
      setImages([]);
    }
  }

  // Öffnet ein bestehendes Projekt
  async function handleOpen() {
    const files = await window.api.openFileDialog();
    if (files && files[0]) {
      const data = await window.api.project.open(files[0]);
      setProject(data);
      const imgs = data.images.map((img) => ({
        id: img.id,
        path: 'file://' + folderPath(data, img.file),
      }));
      setImages(imgs);
    }
  }

  // Fügt Bilder zum Projekt hinzu
  async function handleAddImages() {
    const files = await window.api.openFileDialog();
    if (files && files.length) {
      const data = await window.api.project.addImages(files);
      if (!data) {
        alert('Bitte erst ein Projekt anlegen oder öffnen.');
        return;
      }
      const imgs = data.images.map((img) => ({
        id: img.id,
        path: 'file://' + folderPath(data, img.file),
      }));
      setImages(imgs);
    }
  }

  // Startet die Batch-Verarbeitung
  async function handleBatch() {
    if (!project) {
      alert('Kein Projekt geöffnet.');
      return;
    }
    await window.api.backend.call('/batch', { project: project.root });
  }

  // Speichert das Projekt
  async function handleExport() {
    await window.api.project.save();
    alert('Projekt gespeichert.');
  }

  function folderPath(proj, rel) {
    return proj.root ? proj.root + '/' + rel : rel;
  }

  return (
    <div className="h-12 flex items-center justify-between px-2 bg-bg-primary text-white shadow">
      <div className="flex gap-2">
        <button className="neu px-2" aria-label="Neu" onClick={handleNew}>Neu</button>
        <button className="neu px-2" aria-label="Öffnen" onClick={handleOpen}>Öffnen</button>
        <button className="neu px-2" aria-label="Bilder hinzufügen" onClick={handleAddImages}>Bilder</button>
        <button className="neu px-2" aria-label="Batch" onClick={handleBatch}>Batch</button>
        <button className="neu px-2" aria-label="Export" onClick={handleExport}>Export</button>
      </div>
      <div className="flex items-center gap-4">
        <label className="flex items-center gap-1 text-xs">
          GPU
          <input type="checkbox" className="ml-1" checked={gpu} onChange={(e) => setGpu(e.target.checked)} />
        </label>
        <select className="bg-bg-secondary text-white text-xs">
          <option>DE</option>
          <option>EN</option>
        </select>
      </div>
    </div>
  );
}
