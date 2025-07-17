import { create } from 'zustand';

export interface TaskState {
  progress: number;
  setProgress: (val: number) => void;
}

// Speichert den Fortschritt laufender AI-Jobs
export const useTaskStore = create<TaskState>((set) => ({
  progress: 0,
  setProgress: (val) => set({ progress: val }),
}));
