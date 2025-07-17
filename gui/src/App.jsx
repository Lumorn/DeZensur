// Hauptkomponente der React-Oberfläche
import React from 'react';
import { useStore } from './store.js';
import TitleBar from './components/TitleBar.jsx';
import CommandBar from './components/CommandBar.jsx';
import LeftSidebar from './components/LeftSidebar.jsx';
import CanvasArea from './components/CanvasArea.jsx';
import RightInspector from './components/RightInspector.jsx';
import FooterBar from './components/FooterBar.jsx';

export default function App() {
  const images = useStore((s) => s.images);
  const project = useStore((s) => s.project);
  const activeImage = images[0];
  return (
    <div className="h-screen flex flex-col bg-bg-primary" data-theme="dark">
      <TitleBar projectName={project?.title} />
      <CommandBar />
      <div className="flex flex-1 overflow-hidden">
        <LeftSidebar images={images} />
        <CanvasArea activeImage={activeImage} />
        <RightInspector />
      </div>
      <FooterBar />
    </div>
  );
}
