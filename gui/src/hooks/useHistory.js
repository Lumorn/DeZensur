// Einfacher Undo/Redo-Stack
import { useRef, useState } from 'react';

export function useHistory() {
  const past = useRef([]);
  const future = useRef([]);
  const [current, setCurrent] = useState(null);

  function pushHistory(dataUrl) {
    if (current) past.current.push(current);
    setCurrent(dataUrl);
    future.current = [];
  }

  function undo() {
    if (past.current.length === 0) return;
    const prev = past.current.pop();
    if (current) future.current.push(current);
    setCurrent(prev);
  }

  function redo() {
    if (future.current.length === 0) return;
    const next = future.current.pop();
    if (current) past.current.push(current);
    setCurrent(next);
  }

  return { pushHistory, undo, redo, current };
}
