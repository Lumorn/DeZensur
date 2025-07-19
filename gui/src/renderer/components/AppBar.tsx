import React, { useState, useEffect } from 'react';
import { useGalleryStore } from '../stores/useGalleryStore';
import { useProjectStore } from '../stores/useProjectStore';
import { useLocaleStore, Lang } from '../stores/useLocaleStore';

declare global {
  interface Window {
    dialogs: { openImages: () => Promise<string[]> };
    // "api" umfasst die per electron-trpc bereitgestellten Aufrufe
    api: any;
  }
}

// Oberste App-Bar mit Logo und Menüs
export default function AppBar() {
  const addImages = useGalleryStore((s) => s.addImages);
  const addProjImages = useProjectStore((s) => s.addImages);
  const setProject = useProjectStore((s) => s.setProject);
  const [openFile, setOpenFile] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [gpu, setGpu] = useState(true);
  const lang = useLocaleStore((s) => s.lang);
  const setLang = useLocaleStore((s) => s.setLang);
  const t = useLocaleStore((s) => s.t);

  async function handleAdd() {
    // Bilder auswählen und sowohl in die Galerie
    // als auch ins Projekt laden
    const paths = await window.dialogs.openImages();
    if (paths && paths.length) {
      addImages(paths);
      addProjImages(paths);
    }
  }

  // Öffnet die Einstellungen
  function toggleSettings() {
    setShowSettings(!showSettings);
  }

  // Wechselt zwischen GPU- und CPU-Modus
  function toggleGpu() {
    setGpu(!gpu);
  }

  // Zeigt ein Dialog zum Auswählen eines Arbeitsordners
  async function chooseDir() {
    const paths = await window.api.openFolderDialog();
    if (paths && paths[0]) {
      // Gewählten Ordner als aktuelles Projekt setzen
      setProject(paths[0]);
    }
  }

  useEffect(() => {
    const key = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
        e.preventDefault();
        handleAdd();
      }
    };
    window.addEventListener('keydown', key);
    return () => window.removeEventListener('keydown', key);
  }, []);

  return (
    <header className="h-15 flex items-center px-4 bg-[#1e1e2f] text-white relative">
      <h1 className="font-semibold mr-auto">DeZensur</h1>
      <nav className="space-x-4 hidden md:block">
        <div className="inline-block relative">
          <button className="hover:underline" onClick={() => setOpenFile(!openFile)}>{t('file')}</button>
          {openFile && (
            <div className="absolute left-0 mt-1 w-40 bg-gray-800 border border-gray-700 z-10">
              <button className="block w-full text-left px-2 py-1 hover:bg-gray-700" onClick={handleAdd}>
                {t('add_images')}
              </button>
            </div>
          )}
        </div>
        <button className="hover:underline">Edit</button>
        <button className="hover:underline">View</button>
        <button className="hover:underline">Help</button>
      </nav>
      <div className="ml-auto flex space-x-2">
        <button aria-label="Settings" onClick={toggleSettings}>⚙</button>
        <button aria-label="GPU-Status" onClick={toggleGpu}>{gpu ? '🖥' : '💻'}</button>
        <button aria-label="Working-Dir" onClick={chooseDir}>📁</button>
        <select
          value={lang}
          onChange={(e) => setLang(e.target.value as Lang)}
          className="bg-gray-800 text-white text-xs"
        >
          <option value="de">DE</option>
          <option value="en">EN</option>
        </select>
      </div>
      {showSettings && (
        <div className="absolute right-2 top-12 bg-gray-800 border border-gray-700 p-2 z-10">
          Einstellungen folgen…
        </div>
      )}
    </header>
  );
}
