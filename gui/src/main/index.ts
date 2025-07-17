import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import { join } from 'path';
import { registerIpc } from './ipc';

// Einfacher Main-Prozess mit Platzhaltern für IPC-Handler
let mainWindow: BrowserWindow | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      contextIsolation: true,
    },
  });

  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'));
  }
}

app.whenReady().then(() => {
  createWindow();
  registerIpc();
  ipcMain.handle('dialog:openImages', async () => {
    const result = await dialog.showOpenDialog({
      filters: [{ name: 'Images', extensions: ['png', 'jpg', 'jpeg', 'webp', 'bmp'] }],
      properties: ['openFile', 'multiSelections'],
    });
    return result.filePaths;
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

