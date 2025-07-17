import { contextBridge } from 'electron';
import { createIPCInvoker } from 'electron-trpc/preload';
import type { AppRouter } from './ipc';

// Stellt die tRPC-API im Renderer bereit
const api = createIPCInvoker<AppRouter>();
contextBridge.exposeInMainWorld('api', api);
