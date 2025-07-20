import React from 'react';
import { useStore } from '../store.js';

export default function SettingsModal() {
  const [model, setModel] = React.useState('lama');
  const [prompt, setPrompt] = React.useState('');
  const [autoTags, setAutoTags] = React.useState(true);
  const [device, setDevice] = React.useState('gpu');
  const { prefs } = useStore();

  React.useEffect(() => {
    // Einstellungen im globalen Store aktualisieren
    prefs.inpaintModel = model;
    prefs.prompt = prompt;
    prefs.autoTags = autoTags;
    prefs.device = device;
  }, [model, prompt, autoTags, device, prefs]);

  function handleModelChange(e) {
    const val = e.target.value;
    setModel(val);
    if (val !== 'lama') {
      setPrompt('masterpiece, best quality, anime illustration, detailed anatomy, soft shading');
    }
  }

  return (
    <div>
      <label htmlFor="model" className="block mb-2">Inpainting-Modell</label>
      <select
        id="model"
        value={model}
        onChange={handleModelChange}
        className="border p-1 mb-4"
      >
        <option value="lama">LaMa</option>
        {!autoTags && <option value="sd2_inpaint">SD-2-Inpaint</option>}
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
      <label className="mt-2 block">
        <input
          type="checkbox"
          checked={autoTags}
          onChange={(e) => setAutoTags(e.target.checked)}
          className="mr-1"
        />
        Automatische Anatomie-Tags
      </label>
      <label htmlFor="device" className="block mt-4">Hardware</label>
      <select
        id="device"
        value={device}
        onChange={(e) => setDevice(e.target.value)}
        className="border p-1"
      >
        <option value="gpu">GPU</option>
        <option value="cpu">CPU</option>
      </select>
    </div>
  );
}
