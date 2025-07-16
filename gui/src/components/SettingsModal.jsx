import React from 'react';
import { useStore } from '../store.js';

export default function SettingsModal() {
  const [model, setModel] = React.useState('lama');
  const [prompt, setPrompt] = React.useState('');
  const { prefs } = useStore();

  React.useEffect(() => {
    prefs.inpaintModel = model;
    prefs.prompt = prompt;
  }, [model, prompt, prefs]);

  return (
    <div>
      <label className="block mb-2">Inpainting-Modell</label>
      <select
        value={model}
        onChange={(e) => setModel(e.target.value)}
        className="border p-1 mb-4"
      >
        <option value="lama">LaMa</option>
        <option value="sd2_inpaint">SD-2-Inpaint</option>
        <option value="revanimated">revAnimated</option>
      </select>
      {model !== 'lama' && (
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Prompt"
          className="border p-1 w-full"
        />
      )}
    </div>
  );
}
