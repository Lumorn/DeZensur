// Steuert das Anlegen und Laden von Projekten
import React from 'react';
import { useStore } from '../store.js';

export default function ProjectMenu() {
  const setProject = useStore((s) => s.setProject);
  const setImages = useStore((s) => s.setImages);

  async function newProject() {
    const folder = await window.api.openFolderDialog();
    if (folder && folder[0]) {
      const data = await window.api.project.new(folder[0]);
      setProject(data);
      setImages([]);
    }
  }

  async function addImages() {
    const files = await window.api.openFileDialog();
    if (files && files.length) {
      const data = await window.api.project.addImages(files);
      // Falls kein Projekt offen ist, liefert der IPC-Handler null
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

  function folderPath(proj, rel) {
    return proj.root ? proj.root + '/' + rel : rel;
  }

  return (
    <div className="p-2 flex gap-2 bg-gray-800 text-white">
      <button onClick={newProject}>Projekt neu</button>
      <button onClick={addImages}>Bilder hinzufügen</button>
    </div>
  );
}
