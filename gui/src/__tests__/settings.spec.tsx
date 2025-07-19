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
    const { getByRole, getByLabelText, getByPlaceholderText } = render(<SettingsModal />);

    const select = getByRole('combobox');
    fireEvent.change(select, { target: { value: 'revanimated' } });
    expect(useStore.getState().prefs.inpaintModel).toBe('revanimated');

    const checkbox = getByLabelText('Automatische Anatomie-Tags');
    fireEvent.click(checkbox);
    expect(useStore.getState().prefs.autoTags).toBe(false);

    const input = getByPlaceholderText('Prompt');
    fireEvent.change(input, { target: { value: 'test' } });
    expect(useStore.getState().prefs.prompt).toBe('test');
  });
});
