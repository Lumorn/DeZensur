import { RootRoute, Route, Router } from '@tanstack/react-router';
import AppBar from './components/AppBar';
import GalleryPane from './components/GalleryPane';
import SidePanel from './components/SidePanel';

const rootRoute = new RootRoute({
  component: () => (
    <div className="h-screen flex flex-col">
      <AppBar />
      <div className="flex flex-1 overflow-hidden">
        <GalleryPane />
        <SidePanel />
      </div>
    </div>
  ),
});

const indexRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/',
  component: () => null,
});

const routeTree = rootRoute.addChildren([indexRoute]);

export const router = new Router({ routeTree });

export type AppRouter = typeof router;
