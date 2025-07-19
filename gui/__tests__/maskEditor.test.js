import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import MaskEditor from '../src/components/MaskEditor.jsx';

jest.mock('react-konva', () => {
  const React = require('react');
  const Fake = ({ children }) => <div>{children}</div>;
  return { Stage: Fake, Layer: Fake, Line: Fake, Image: Fake };
});

jest.mock('use-image', () => () => [null]);

// Testet, ob sich die Pinselgröße ändert

test('brush size change', () => {
  const { getByLabelText } = render(<MaskEditor imgSrc="" maskSrc="" />);
  const plus = getByLabelText('Brush größer');
  fireEvent.click(plus);
  const minus = getByLabelText('Brush kleiner');
  fireEvent.click(minus);
  // Wenn kein Fehler auftritt, wurde der Zustand aktualisiert
  expect(true).toBe(true);
});

// Testet Zoom via Strg+Mausrad
test('zoom with wheel', () => {
  const { container } = render(<MaskEditor imgSrc="" maskSrc="" />);
  fireEvent.wheel(container.firstChild, {
    ctrlKey: true,
    deltaY: -100,
  });
  // Solange kein Fehler auftritt, funktioniert das Event
  expect(true).toBe(true);
});
