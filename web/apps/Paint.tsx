import React, { useRef, useState, useEffect } from 'react';
import { Eraser, Pencil, Trash2 } from 'lucide-react';
import { cn } from '../utils';
import type { AppMeta } from '../types';

export const appMeta: AppMeta = { id: 'paint', title: 'Paint Studio', category: 'Utilities' };

export const Paint: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [color, setColor] = useState('#000000');
  const [tool, setTool] = useState<'pencil' | 'eraser'>('pencil');
  const [lineWidth, setLineWidth] = useState(3);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    // Set canvas size to parent size
    const parent = canvas.parentElement;
    if (parent) {
      canvas.width = parent.clientWidth;
      canvas.height = parent.clientHeight;
    }

    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
  }, []);

  const startDrawing = (e: React.MouseEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    ctx.beginPath();
    ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
    setIsDrawing(true);
  };

  const draw = (e: React.MouseEvent) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
    ctx.strokeStyle = tool === 'eraser' ? '#ffffff' : color;
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';
    ctx.stroke();
  };

  const stopDrawing = () => {
    setIsDrawing(false);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  };

  return (
    <div className="h-full flex flex-col bg-os-bg">
      <div className="p-2 bg-os-header border-b border-os-border flex items-center gap-4">
        <div className="flex items-center gap-1 bg-os-window p-1 rounded-lg border border-os-border">
          <button
            onClick={() => setTool('pencil')}
            className={cn("p-1.5 rounded hover:bg-os-bg focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-os-accent", tool === 'pencil' && "bg-os-accent text-white")}
            aria-label="Pencil"
            aria-pressed={tool === 'pencil'}
          >
            <Pencil size={16} />
          </button>
          <button
            onClick={() => setTool('eraser')}
            className={cn("p-1.5 rounded hover:bg-os-bg focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-os-accent", tool === 'eraser' && "bg-os-accent text-white")}
            aria-label="Eraser"
            aria-pressed={tool === 'eraser'}
          >
            <Eraser size={16} />
          </button>
        </div>

        <input
          type="color"
          value={color}
          onChange={(e) => setColor(e.target.value)}
          className="w-8 h-8 rounded cursor-pointer border-0"
          aria-label="Stroke colour"
        />

        <input
          type="range"
          min="1"
          max="20"
          value={lineWidth}
          onChange={(e) => setLineWidth(parseInt(e.target.value))}
          className="w-24"
          aria-label="Stroke width"
        />

        <button onClick={clearCanvas} className="ml-auto p-1.5 text-red-400 hover:bg-red-900/20 rounded focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-red-400" aria-label="Clear canvas">
          <Trash2 size={16} />
        </button>
      </div>
      <div className="flex-1 relative bg-neutral-200 overflow-hidden cursor-crosshair">
        <canvas
          ref={canvasRef}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          className="absolute inset-0"
        />
      </div>
    </div>
  );
};
