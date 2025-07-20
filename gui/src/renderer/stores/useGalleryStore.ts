import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

// Metadaten eines Bildes
export interface ImageMeta {
  id: string;
  path: string;
  name: string;
  thumb?: string;
}

interface GalleryState {
  images: ImageMeta[];
  selectedId: string | null;
  addImages: (paths: string[]) => void;
  select: (id: string) => void;
}

// Zustand für die Galerie
let worker: Worker | null = null;

function ensureWorker(set: (fn: (s: GalleryState) => GalleryState) => void) {
  if (!worker && typeof Worker !== 'undefined') {
    worker = new Worker(new URL('../lib/thumbWorker.ts', import.meta.url), {
      type: 'module',
    });
    worker.onmessage = (e) => {
      const { id, thumb } = e.data;
      set((s) => ({
        ...s,
        images: s.images.map((img) =>
          img.id === id ? { ...img, thumb } : img,
        ),
      }));
    };
  }
  return worker;
}

export const useGalleryStore = create<GalleryState>((set, get) => ({
  images: [],
  selectedId: null,
  addImages: (paths) => {
    // Bereits geladene Pfade
    const existing = new Set(get().images.map((i) => i.path));
    // Doppelte innerhalb des Aufrufs entfernen
    const unique = Array.from(new Set(paths));
    const added = unique
      .filter((p) => !existing.has(p))
      .map((p) => ({
        id: uuidv4(),
        path: 'file://' + p,
        name: p.split(/[/\\]/).pop() || '',
      }));
    if (added.length) {
      set((s) => ({ images: [...s.images, ...added] }));
      const w = ensureWorker(set);
      if (w) {
        for (const img of added) {
          w.postMessage({ id: img.id, path: img.path });
        }
      }
    }
  },
  select: (id) => set({ selectedId: id }),
}));
