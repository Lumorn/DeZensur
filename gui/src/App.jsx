// Hauptkomponente der React-Oberfläche
import React from 'react';
import { useStore } from './store.js';
import Gallery from './components/Gallery.jsx';
import ProjectMenu from './components/ProjectMenu.jsx';

export default function App() {
  const images = useStore((s) => s.images);
  return (
    <div className="h-screen flex flex-col" data-theme="light">
      <ProjectMenu />
      <div className="flex-1 overflow-auto">
        <Gallery images={images} />
      </div>
    </div>
  );
}
