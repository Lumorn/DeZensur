import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import RightInspector from '../components/RightInspector.jsx';
import { useStore } from '../store.js';

describe('RightInspector', () => {
  beforeEach(() => {
    useStore.setState({ prefs: {} });
  });

  test('modellwechsel aktualisiert prefs', () => {
    const { getByLabelText } = render(<RightInspector />);
    const select = getByLabelText('Inpainting-Modell auswählen');
    fireEvent.change(select, { target: { value: 'revanimated' } });
    expect(useStore.getState().prefs.inpaintModel).toBe('revanimated');
  });
});
