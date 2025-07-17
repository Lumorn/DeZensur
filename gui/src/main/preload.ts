import { contextBridge, ipcRenderer } from 'electron';
import { createIPCInvoker } from 'electron-trpc/preload';
import type { AppRouter } from './ipc';

// Stellt die tRPC-API im Renderer bereit
const api = createIPCInvoker<AppRouter>();
contextBridge.exposeInMainWorld('api', api);

// Stellt eine Funktion bereit, um Bilddateien auszuwählen
contextBridge.exposeInMainWorld('dialogs', {
  openImages: () => ipcRenderer.invoke('dialog:openImages'),
});
