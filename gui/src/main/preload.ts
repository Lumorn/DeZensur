import { contextBridge, ipcRenderer } from 'electron';

// IPC-Hilfsfunktionen per contextBridge bereitstellen
contextBridge.exposeInMainWorld('api', {
  ping: (msg: string) => ipcRenderer.invoke('ping', msg),
});
