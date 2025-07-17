// Bindet IPC-Funktionen für das Renderer-Frontend ein
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  openFileDialog: () => ipcRenderer.invoke('dialog:openFile'),
  openFolderDialog: () => ipcRenderer.invoke('dialog:openFolder'),
  project: {
    new: (root) => ipcRenderer.invoke('project:new', root),
    open: (path) => ipcRenderer.invoke('project:open', path),
    save: () => ipcRenderer.invoke('project:save'),
    addImages: (paths) => ipcRenderer.invoke('project:addImages', paths),
  },
  backend: {
    call: (endpoint, payload) => ipcRenderer.invoke('backend:call', endpoint, payload),
  },
});

contextBridge.exposeInMainWorld('maskEditor', {
  saveMask: (id, png) => ipcRenderer.invoke('save-mask', id, png),
});
