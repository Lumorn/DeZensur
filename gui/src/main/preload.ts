import { contextBridge, ipcRenderer } from 'electron';
import { exposeElectronTRPC } from 'electron-trpc/preload';

// Initialisiert electron-trpc und macht es dem Renderer zugänglich
process.once('loaded', () => {
  // Bindet die electron-trpc Schnittstelle an das Fenster
  exposeElectronTRPC({ ipcRenderer });
});

// Stellt eine Funktion bereit, um Bilddateien auszuwählen
contextBridge.exposeInMainWorld('dialogs', {
  openImages: () => ipcRenderer.invoke('dialog:openImages'),
});
