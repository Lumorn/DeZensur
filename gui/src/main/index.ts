import { app, BrowserWindow, ipcMain } from 'electron';
import { join } from 'path';
import { createContextBridge } from './preload';

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

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

// Beispiel: ein simpler Echo-Handler über electron-trpc
ipcMain.handle('ping', (_evt, msg: string) => msg);
