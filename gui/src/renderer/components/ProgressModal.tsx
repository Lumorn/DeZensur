import React from 'react';
import { useTaskStore } from '../stores/useTaskStore';

// Zeigt den Fortschritt laufender Aufgaben in einem Overlay
export default function ProgressModal() {
  const progress = useTaskStore((s) => s.progress);
  if (progress <= 0 || progress >= 100) {
    return null;
  }
  return (
    <div className="absolute inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-gray-800 p-4 rounded shadow w-72 text-white">
        <div className="h-2 bg-gray-700 rounded overflow-hidden">
          <div
            className="bg-accent-primary h-full"
            style={{ width: `${progress}%` }}
          />
        </div>
        <div className="text-center mt-2 text-sm">{Math.round(progress)}%</div>
      </div>
    </div>
  );
}
