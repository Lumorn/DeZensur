import { createTRPCProxyClient } from '@trpc/client';
import { ipcLink } from 'electron-trpc/renderer';
import type { AppRouter } from '../../main/ipc';

// Baut den tRPC-Client für die IPC-Kommunikation auf
export const ipc = createTRPCProxyClient<AppRouter>({
  links: [ipcLink()],
});
