import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

// Metadaten eines Bildes
export interface ImageMeta {
  id: string;
  path: string;
  name: string;
}

interface GalleryState {
  images: ImageMeta[];
  selectedId: string | null;
  addImages: (paths: string[]) => void;
  select: (id: string) => void;
}

// Zustand für die Galerie
export const useGalleryStore = create<GalleryState>((set, get) => ({
  images: [],
  selectedId: null,
  addImages: (paths) => {
    const existing = new Set(get().images.map((i) => i.path));
    const added = paths
      .filter((p) => !existing.has(p))
      .map((p) => ({
        id: uuidv4(),
        path: 'file://' + p,
        name: p.split(/[/\\]/).pop() || '',
      }));
    if (added.length) {
      set((s) => ({ images: [...s.images, ...added] }));
    }
  },
  select: (id) => set({ selectedId: id }),
}));
