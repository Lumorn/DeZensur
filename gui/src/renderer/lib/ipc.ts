import { createIPCClient } from 'electron-trpc/renderer';
import type { AppRouter } from '../../main/ipc';

// Client fuer den Zugriff auf die im Preload registrierten IPC-Routen
export const ipc = createIPCClient<AppRouter>('api');
