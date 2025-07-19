// Zentraler Zustand der Anwendung
import create from 'zustand';

export const useStore = create((set) => ({
  project: null,
  images: [],
  // Voreinstellungen inklusive Design-Theme
  prefs: { theme: 'dark' },
  setProject: (p) => set({ project: p }),
  setImages: (imgs) => set({ images: imgs }),
  // Aktualisiert einzelne Einstellungen
  updatePrefs: (patch) =>
    set((state) => ({ prefs: { ...state.prefs, ...patch } })),
}));
