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
  const [lines, setLines] = useState([]);
  const { pushHistory, undo, redo, current } = useHistory();

  const [mode, setMode] = useState('draw');
  const [brush, setBrush] = useState(20);

  useEffect(() => {
    if (current && onMaskChange) onMaskChange(current);
  }, [current, onMaskChange]);

  function startDraw(e) {
    isDrawing.current = true;
    const pos = e.target.getStage().getPointerPosition();
    setLines([...lines, { tool: mode, points: [pos.x, pos.y], brush }]);
  }

  function draw(e) {
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
    isDrawing.current = false;
    if (stageRef.current) {
      const url = stageRef.current.toDataURL({ mimeType: 'image/png', pixelRatio: 1 });
      pushHistory(url);
    }
  }

  return (
    <>
      <Stage
        width={image?.width}
        height={image?.height}
        ref={stageRef}
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
