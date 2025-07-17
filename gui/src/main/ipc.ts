import { ipcMain } from 'electron';
import { initTRPC } from '@trpc/server';
import { createIPCHandler } from 'electron-trpc/main';

// tRPC-Router fuer alle IPC-Kanaele
const t = initTRPC.create();

export const appRouter = t.router({
  ping: t.procedure.input((val: string) => val).query(({ input }) => input),
  censorDetect: t.procedure
    .input<string>()
    .mutation(async ({ input }) => ({ score: 0, masks: [] })),
  samSegment: t.procedure
    .input<string>()
    .mutation(async ({ input }) => ({ mask: '' })),
  inpaint: t.procedure
    .input<string>()
    .mutation(async ({ input }) => ({ result: input })),
  progress: t.procedure.input<string>().subscription(() => {
    // Platzhalter fuer Progress Events
    return () => {};
  }),
  log: t.procedure.input<string>().mutation(async () => true),
});

export type AppRouter = typeof appRouter;

// Registriert die Handler im Main-Prozess
export function registerIpc() {
  createIPCHandler({ router: appRouter, ipcMain });
}
