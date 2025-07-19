import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SettingsModal from '../components/SettingsModal.jsx';
import { useStore } from '../store.js';

describe('SettingsModal', () => {
  beforeEach(() => {
    useStore.setState({ prefs: {} });
  });

  test('aktualisiert das Prefs-Objekt', () => {
    const { getByLabelText, getByPlaceholderText } = render(<SettingsModal />);

    const modelSelect = getByLabelText('Inpainting-Modell');
    fireEvent.change(modelSelect, { target: { value: 'revanimated' } });
    expect(useStore.getState().prefs.inpaintModel).toBe('revanimated');

    const deviceSelect = getByLabelText('Hardware');
    fireEvent.change(deviceSelect, { target: { value: 'cpu' } });
    expect(useStore.getState().prefs.device).toBe('cpu');

    const checkbox = getByLabelText('Automatische Anatomie-Tags');
    fireEvent.click(checkbox);
    expect(useStore.getState().prefs.autoTags).toBe(false);

    const input = getByPlaceholderText('Prompt');
    fireEvent.change(input, { target: { value: 'test' } });
    expect(useStore.getState().prefs.prompt).toBe('test');
  });
});
