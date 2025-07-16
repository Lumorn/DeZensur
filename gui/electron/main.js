// Startpunkt des Electron-Hauptprozesses
import { app, BrowserWindow, ipcMain } from 'electron';
import { spawn, execSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
    },
  });

  // Backend-Server bei Bedarf starten
  if (!isServerRunning()) {
    spawn('python', ['-m', 'core.server_stub'], { stdio: 'ignore' });
  }

  const dev = !app.isPackaged;
  if (dev) {
    mainWindow.loadURL('http://localhost:5173');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }
}

function isServerRunning() {
  // Testet, ob der Stub-Server bereits läuft
  try {
    execSync('curl -sf http://127.0.0.1:8787/detect', { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

ipcMain.handle('dialog:openFile', async () => {
  const { dialog } = await import('electron');
  const result = await dialog.showOpenDialog({ properties: ['openFile', 'multiSelections'] });
  return result.filePaths;
});

ipcMain.handle('dialog:openFolder', async () => {
  const { dialog } = await import('electron');
  const result = await dialog.showOpenDialog({ properties: ['openDirectory'] });
  return result.filePaths;
});

import { ProjectIPC } from './project.js';
ProjectIPC(ipcMain);
