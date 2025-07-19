import { ipcMain } from 'electron';
import { initTRPC } from '@trpc/server';
import { observable } from '@trpc/server/observable';
import { createIPCHandler } from 'electron-trpc/main';
import { EventEmitter } from 'events';

// Emitter zum Weiterreichen von Fortschrittswerten
const progressEmitter = new EventEmitter();

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
  // Simuliert einen lang laufenden Task und sendet Fortschritt
  startDummy: t.procedure.mutation(() => {
    let val = 0;
    const timer = setInterval(() => {
      val += 10;
      progressEmitter.emit('progress', val);
      if (val >= 100) {
        clearInterval(timer);
      }
    }, 200);
    return true;
  }),
  progress: t.procedure.subscription(() => {
    return observable<number>((emit) => {
      const handler = (v: number) => emit.next(v);
      progressEmitter.on('progress', handler);
      return () => {
        progressEmitter.off('progress', handler);
      };
    });
  }),
  log: t.procedure.input<string>().mutation(async () => true),
});

export type AppRouter = typeof appRouter;

// Registriert die Handler im Main-Prozess
export function registerIpc() {
  createIPCHandler({ router: appRouter, ipcMain });
}
