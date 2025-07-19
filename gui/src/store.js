// Zentraler Zustand der Anwendung
import create from 'zustand';

export const useStore = create((set) => ({
  project: null,
  images: [],
  // aktuell ausgewähltes Bild
  activeImageId: null,
  // Voreinstellungen inklusive Design-Theme
  prefs: { theme: 'dark' },
  setProject: (p) => set({ project: p }),
  // ersetzt die Bildliste und wählt das erste Bild aus
  setImages: (imgs) =>
    set({ images: imgs, activeImageId: imgs[0] ? imgs[0].id : null }),
  // setzt das aktive Bild explizit
  setActiveImageId: (id) => set({ activeImageId: id }),
  // Aktualisiert einzelne Einstellungen
  updatePrefs: (patch) =>
    set((state) => ({ prefs: { ...state.prefs, ...patch } })),
}));
