import { RootRoute, Route, Router } from '@tanstack/react-router';
import { useEffect } from 'react';
import AppBar from './components/AppBar';
import GalleryPane from './components/GalleryPane';
import SidePanel from './components/SidePanel';
import ProgressModal from './components/ProgressModal';
import { ipc } from './lib/ipc';
import { useTaskStore } from './stores/useTaskStore';

function RootLayout() {
  // Abonnement auf Fortschrittswerte aus dem Main-Prozess
  useEffect(() => {
    const sub = ipc.progress.subscribe(undefined, {
      next: (val: number) => useTaskStore.getState().setProgress(val),
    });
    return () => sub.unsubscribe();
  }, []);

  return (
    <div className="h-screen flex flex-col">
      <AppBar />
      <div className="flex flex-1 overflow-hidden">
        <GalleryPane />
        <SidePanel />
      </div>
      <ProgressModal />
    </div>
  );
}

const rootRoute = new RootRoute({
  component: RootLayout,
});

const indexRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/',
  component: () => null,
});

const routeTree = rootRoute.addChildren([indexRoute]);

export const router = new Router({ routeTree });

export type AppRouter = typeof router;
