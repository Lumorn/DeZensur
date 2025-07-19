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
  const activeId = useStore((s) => s.activeImageId);
  const project = useStore((s) => s.project);
  const theme = useStore((s) => s.prefs.theme || 'dark');
  const activeImage = images.find((img) => img.id === activeId);
  return (
    <div className="h-screen flex flex-col bg-bg-primary" data-theme={theme}>
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
