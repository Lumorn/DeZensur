import { create } from 'zustand';
import de from '../../i18n/de.json';
import en from '../../i18n/en.json';

// Unterstuetzte Sprachen
export type Lang = 'de' | 'en';

const bundles: Record<Lang, Record<string, string>> = { de, en };

// Zustand mit aktueller Sprache und Uebersetzungsfunktion
export const useLocaleStore = create<{
  lang: Lang;
  setLang: (l: Lang) => void;
  t: (key: string) => string;
}>((set, get) => ({
  lang: 'de',
  setLang: (l) => set({ lang: l }),
  t: (key) => bundles[get().lang][key] ?? key,
}));
