import { create } from 'zustand';

// Speichert den aktuellen Projektpfad und geladene Bilder
export interface ProjectState {
  path: string | null;
  images: string[];
  setProject: (path: string) => void;
  addImages: (paths: string[]) => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  path: null,
  images: [],
  setProject: (path) => set({ path }),
  addImages: (paths) => set((s) => ({ images: [...s.images, ...paths] })),
}));
