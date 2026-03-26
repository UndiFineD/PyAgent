import React, { useState } from 'react';
import { Code, Eye } from 'lucide-react';
import { cn } from '../utils';
import type { AppMeta } from '../types';

export const appMeta: AppMeta = { id: 'editor', title: 'Text Editor', category: 'Utilities' };

export const Editor: React.FC = () => {
  const [content, setContent] = useState('# Welcome to NebulaOS\n\nStart typing...');
  const [mode, setMode] = useState<'code' | 'preview'>('code');

  return (
    <div className="h-full flex flex-col bg-os-bg text-os-text">
      <div className="flex items-center gap-2 p-2 border-b border-os-border bg-os-header">
        <button
          onClick={() => setMode('code')}
          className={cn(
            "px-3 py-1.5 rounded-md text-sm flex items-center gap-2 transition-colors",
            mode === 'code' ? "bg-os-accent text-white" : "hover:bg-os-window"
          )}
        >
          <Code size={14} /> Code
        </button>
        <button
          onClick={() => setMode('preview')}
          className={cn(
            "px-3 py-1.5 rounded-md text-sm flex items-center gap-2 transition-colors",
            mode === 'preview' ? "bg-os-accent text-white" : "hover:bg-os-window"
          )}
        >
          <Eye size={14} /> Preview
        </button>
      </div>
      
      <div className="flex-1 relative overflow-hidden">
        {mode === 'code' ? (
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full h-full p-4 bg-os-bg text-os-text font-mono resize-none focus:outline-none focus:ring-2 focus:ring-os-accent"
            spellCheck={false}
          />
        ) : (
          <div className="w-full h-full p-4 bg-white text-slate-900 overflow-auto prose prose-sm max-w-none">
            {/* Simple markdown-like rendering for demo purposes */}
            {content.split('\n').map((line, i) => {
              if (line.startsWith('# ')) return <h1 key={i} className="text-2xl font-bold mb-2">{line.slice(2)}</h1>;
              if (line.startsWith('## ')) return <h2 key={i} className="text-xl font-bold mb-2">{line.slice(3)}</h2>;
              if (line.startsWith('- ')) return <li key={i} className="ml-4">{line.slice(2)}</li>;
              if (line === '') return <br key={i} />;
              return <p key={i} className="mb-1">{line}</p>;
            })}
          </div>
        )}
      </div>
    </div>
  );
};
