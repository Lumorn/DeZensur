// Canvas-Komponente zum Bearbeiten von Masken
import Konva from 'konva';
import { Stage, Layer, Line, Image as KonvaImage } from 'react-konva';

// Erhöhe Performance bei großen Bildern
Konva.hitCanvas.pixelRatio = 1;
import React, { useState, useRef, useEffect } from 'react';
import useImage from 'use-image';
import MaskToolbar from './MaskToolbar.jsx';
import { useHistory } from '../hooks/useHistory.js';

export default function MaskEditor({ imgSrc, maskSrc, onMaskChange }) {
  const [image] = useImage(imgSrc);
  const [mask] = useImage(maskSrc);
  const stageRef = useRef(null);
  const isDrawing = useRef(false);
  const isPanning = useRef(false);
  const lastPos = useRef({ x: 0, y: 0 });
  const [lines, setLines] = useState([]);
  const { pushHistory, undo, redo, current } = useHistory();

  const [mode, setMode] = useState('draw');
  const [brush, setBrush] = useState(20);
  const [scale, setScale] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });

  useEffect(() => {
    function onKeyDown(e) {
      if (e.code === 'Space') isPanning.current = true;
    }
    function onKeyUp(e) {
      if (e.code === 'Space') isPanning.current = false;
    }
    window.addEventListener('keydown', onKeyDown);
    window.addEventListener('keyup', onKeyUp);
    return () => {
      window.removeEventListener('keydown', onKeyDown);
      window.removeEventListener('keyup', onKeyUp);
    };
  }, []);

  useEffect(() => {
    if (current && onMaskChange) onMaskChange(current);
  }, [current, onMaskChange]);

  function startDraw(e) {
    if (isPanning.current) {
      lastPos.current = e.target.getStage().getPointerPosition();
      return;
    }
    isDrawing.current = true;
    const pos = e.target.getStage().getPointerPosition();
    setLines([...lines, { tool: mode, points: [pos.x, pos.y], brush }]);
  }

  function draw(e) {
    if (isPanning.current) {
      const stage = e.target.getStage();
      const pos = stage.getPointerPosition();
      if (!pos) return;
      const dx = pos.x - lastPos.current.x;
      const dy = pos.y - lastPos.current.y;
      lastPos.current = pos;
      setOffset((o) => ({ x: o.x + dx, y: o.y + dy }));
      return;
    }
    if (!isDrawing.current) return;
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    setLines((ls) => {
      const last = ls[ls.length - 1];
      last.points = last.points.concat([point.x, point.y]);
      const copy = ls.slice();
      copy[copy.length - 1] = last;
      return copy;
    });
  }

  function endDraw() {
    if (isPanning.current) {
      isPanning.current = false;
      return;
    }
    isDrawing.current = false;
    if (stageRef.current) {
      const url = stageRef.current.toDataURL({ mimeType: 'image/png', pixelRatio: 1 });
      pushHistory(url);
    }
  }

  function handleWheel(e) {
    if (!e.evt.ctrlKey) return;
    e.evt.preventDefault();
    const stage = e.target.getStage();
    const pointer = stage.getPointerPosition();
    if (!pointer) return;
    const scaleBy = 1.1;
    const direction = e.evt.deltaY > 0 ? -1 : 1;
    const newScale = direction > 0 ? scale * scaleBy : scale / scaleBy;
    const x = pointer.x - (pointer.x - offset.x) * (newScale / scale);
    const y = pointer.y - (pointer.y - offset.y) * (newScale / scale);
    setScale(newScale);
    setOffset({ x, y });
  }

  return (
    <>
      <Stage
        width={image?.width}
        height={image?.height}
        ref={stageRef}
        scaleX={scale}
        scaleY={scale}
        x={offset.x}
        y={offset.y}
        onWheel={handleWheel}
        onMouseDown={startDraw}
        onMouseMove={draw}
        onMouseUp={endDraw}
      >
        <Layer>
          {image && <KonvaImage image={image} />}
          {mask && <KonvaImage image={mask} opacity={0.5} globalCompositeOperation="source-over" />}
          {lines.map((line, i) => (
            <Line
              key={i}
              points={line.points}
              stroke="red"
              strokeWidth={line.brush}
              lineCap="round"
              lineJoin="round"
              globalCompositeOperation={line.tool === 'erase' ? 'destination-out' : 'source-over'}
            />
          ))}
        </Layer>
      </Stage>
      <MaskToolbar
        mode={mode}
        setMode={setMode}
        brush={brush}
        setBrush={setBrush}
        undo={undo}
        redo={redo}
      />
    </>
  );
}
