import React, { useRef, useState, useEffect } from 'react';
import Draggable, { DraggableData, DraggableEvent } from 'react-draggable';
import { X, Minus, Square, Maximize2, Menu, Settings, Info, FilePlus } from 'lucide-react';
import { WindowState } from '../types';
import { cn } from '../utils';

interface WindowProps {
  window: WindowState;
  isActive: boolean;
  onClose: (id: string) => void;
  onMinimize: (id: string) => void;
  onMaximize: (id: string) => void;
  onFocus: (id: string) => void;
  onUpdate: (id: string, updates: Partial<WindowState>) => void;
}

export const Window: React.FC<WindowProps> = ({
  window,
  isActive,
  onClose,
  onMinimize,
  onMaximize,
  onFocus,
  onUpdate,
}) => {
  const nodeRef = useRef<HTMLDivElement>(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isResizing, setIsResizing] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsMenuOpen(false);
      }
    };

    if (isMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isMenuOpen]);

  const handleResize = (direction: string) => (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsResizing(true);
    onFocus(window.id);
    
    const startX = e.clientX;
    const startY = e.clientY;
    const startWidth = window.width;
    const startHeight = window.height;
    const startPosX = window.x;
    const startPosY = window.y;

    const onMouseMove = (moveEvent: MouseEvent) => {
      const deltaX = moveEvent.clientX - startX;
      const deltaY = moveEvent.clientY - startY;
      
      let newWidth = startWidth;
      let newHeight = startHeight;
      let newX = startPosX;
      let newY = startPosY;

      if (direction.includes('e')) newWidth = Math.max(200, startWidth + deltaX);
      if (direction.includes('w')) {
        const w = Math.max(200, startWidth - deltaX);
        newWidth = w;
        newX = startPosX + (startWidth - w);
      }
      if (direction.includes('s')) newHeight = Math.max(150, startHeight + deltaY);
      if (direction.includes('n')) {
        const h = Math.max(150, startHeight - deltaY);
        newHeight = h;
        newY = startPosY + (startHeight - h);
      }

      onUpdate(window.id, { width: newWidth, height: newHeight, x: newX, y: newY });
    };

    const onMouseUp = () => {
      setIsResizing(false);
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    };

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
  };

  const handleDragStop = (e: DraggableEvent, data: DraggableData) => {
    onUpdate(window.id, { x: data.x, y: data.y });
  };

  if (window.isMinimized) return null;

  // Maximized State
  if (window.isMaximized) {
    return (
      <div
        className={cn(
          "absolute top-0 left-0 w-full h-full flex flex-col bg-os-window border-0 shadow-none z-[50]",
          isActive ? "z-[50]" : "z-[40]"
        )}
        style={{ zIndex: window.zIndex }}
      >
        <WindowHeader 
          window={window} 
          isActive={isActive} 
          onClose={onClose} 
          onMinimize={onMinimize} 
          onMaximize={onMaximize} 
          isMenuOpen={isMenuOpen}
          setIsMenuOpen={setIsMenuOpen}
          menuRef={menuRef}
        />
        <div className="flex-1 overflow-hidden relative">
          {window.component}
        </div>
      </div>
    );
  }

  // Normal State
  return (
    <Draggable
      handle=".window-header"
      position={{ x: window.x, y: window.y }}
      onStart={() => onFocus(window.id)}
      onStop={handleDragStop}
      nodeRef={nodeRef}
      bounds="parent"
      disabled={isResizing}
    >
      <div
        ref={nodeRef}
        className={cn(
          "nebula-window absolute flex flex-col bg-os-window border border-os-border shadow-2xl rounded-lg overflow-hidden transition-shadow duration-200",
          isActive ? "shadow-os-accent/20 ring-1 ring-os-border" : "opacity-95"
        )}
        style={{
          width: window.width,
          height: window.height,
          zIndex: window.zIndex,
        }}
        onMouseDown={() => onFocus(window.id)}
      >
        {/* Resize Handles */}
        <div className="absolute top-0 left-0 w-full h-1 cursor-n-resize z-20" onMouseDown={handleResize('n')} />
        <div className="absolute bottom-0 left-0 w-full h-1 cursor-s-resize z-20" onMouseDown={handleResize('s')} />
        <div className="absolute top-0 left-0 h-full w-1 cursor-w-resize z-20" onMouseDown={handleResize('w')} />
        <div className="absolute top-0 right-0 h-full w-1 cursor-e-resize z-20" onMouseDown={handleResize('e')} />
        
        <div className="absolute top-0 left-0 w-3 h-3 cursor-nw-resize z-30" onMouseDown={handleResize('nw')} />
        <div className="absolute top-0 right-0 w-3 h-3 cursor-ne-resize z-30" onMouseDown={handleResize('ne')} />
        <div className="absolute bottom-0 left-0 w-3 h-3 cursor-sw-resize z-30" onMouseDown={handleResize('sw')} />
        <div className="absolute bottom-0 right-0 w-3 h-3 cursor-se-resize z-30" onMouseDown={handleResize('se')} />

        <WindowHeader 
          window={window} 
          isActive={isActive} 
          onClose={onClose} 
          onMinimize={onMinimize} 
          onMaximize={onMaximize} 
          isMenuOpen={isMenuOpen}
          setIsMenuOpen={setIsMenuOpen}
          menuRef={menuRef}
        />

        {/* Content Overlay during resize to prevent iframe/canvas stealing mouse events */}
        {isResizing && <div className="absolute inset-0 z-50 bg-transparent" />}

        <div className="flex-1 overflow-hidden relative">
          {window.component}
        </div>
      </div>
    </Draggable>
  );
};

// Helper Component for Header to reduce duplication
const WindowHeader = ({ window, isActive, onClose, onMinimize, onMaximize, isMenuOpen, setIsMenuOpen, menuRef }: any) => {
  const headerHeightClass = window.isMaximized ? "h-6 text-xs" : "h-8 text-sm";
  const iconSize = window.isMaximized ? 12 : 14;

  return (
    <div className={cn(
      "window-header flex items-center justify-between px-3 select-none relative transition-all shrink-0",
      headerHeightClass,
      isActive ? "bg-os-header text-os-text" : "bg-os-bg text-os-text/60",
      !window.isMaximized && "cursor-move"
    )}>
      <div className="flex items-center gap-3 font-medium">
        {window.hasMenu && (
          <div className="relative" ref={menuRef}>
            <button 
              onClick={(e) => { 
                e.stopPropagation(); 
                setIsMenuOpen(!isMenuOpen); 
              }} 
              className={cn(
                "p-0.5 rounded hover:bg-white/10 transition-colors",
                isMenuOpen && "bg-white/10"
              )}
              onMouseDown={(e) => e.stopPropagation()}
            >
              <Menu size={iconSize} />
            </button>
            
            {isMenuOpen && (
              <div 
                className="absolute top-full left-0 mt-1 w-48 bg-os-window border border-os-border rounded-lg shadow-xl py-1 z-[100] text-os-text animate-in fade-in zoom-in-95 duration-100"
                onMouseDown={(e) => e.stopPropagation()}
              >
                <div className="px-3 py-2 border-b border-os-border mb-1">
                  <div className="font-bold text-xs">{window.title}</div>
                  <div className="text-[10px] opacity-50">v1.0.0</div>
                </div>
                
                <button className="w-full px-3 py-1.5 text-left text-xs hover:bg-os-header flex items-center gap-2">
                  <FilePlus size={12} /> New Window
                </button>
                <button className="w-full px-3 py-1.5 text-left text-xs hover:bg-os-header flex items-center gap-2">
                  <Settings size={12} /> Settings
                </button>
                <button className="w-full px-3 py-1.5 text-left text-xs hover:bg-os-header flex items-center gap-2">
                  <Info size={12} /> About
                </button>
                
                <div className="h-px bg-os-border my-1" />
                
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    onClose(window.id);
                  }}
                  className="w-full px-3 py-1.5 text-left text-xs hover:bg-red-500/20 hover:text-red-400 flex items-center gap-2"
                >
                  <X size={12} /> Close
                </button>
              </div>
            )}
          </div>
        )}
        {window.title}
      </div>
      
      <div className="flex items-center gap-1.5" onMouseDown={(e) => e.stopPropagation()}>
        <button onClick={(e) => { e.stopPropagation(); onMinimize(window.id); }} className="p-0.5 hover:bg-white/10 rounded">
          <Minus size={iconSize} />
        </button>
        <button onClick={(e) => { e.stopPropagation(); onMaximize(window.id); }} className="p-0.5 hover:bg-white/10 rounded">
          {window.isMaximized ? <Square size={iconSize - 2} /> : <Maximize2 size={iconSize - 2} />}
        </button>
        <button onClick={(e) => { e.stopPropagation(); onClose(window.id); }} className="p-0.5 hover:bg-red-500 hover:text-white rounded">
          <X size={iconSize} />
        </button>
      </div>
    </div>
  );
};
