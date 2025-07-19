import { contextBridge, ipcRenderer } from 'electron';
import { exposeElectronTRPC } from 'electron-trpc/main';

// Initialisiert electron-trpc und macht es dem Renderer zugänglich
process.once('loaded', () => {
  exposeElectronTRPC();
});

// Stellt eine Funktion bereit, um Bilddateien auszuwählen
contextBridge.exposeInMainWorld('dialogs', {
  openImages: () => ipcRenderer.invoke('dialog:openImages'),
});
