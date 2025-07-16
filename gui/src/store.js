// Zentraler Zustand der Anwendung
import create from 'zustand';

export const useStore = create((set) => ({
  project: null,
  images: [],
  prefs: {},
  setProject: (p) => set({ project: p }),
  setImages: (imgs) => set({ images: imgs }),
}));
