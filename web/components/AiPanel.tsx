import React, { useState, useCallback } from 'react';
import { Bot, Loader2 } from 'lucide-react';
import { useWebSocket, WsMessage } from '../hooks/useWebSocket';
import { VoiceInput } from './VoiceInput';
import { cn } from '../utils';

interface AiPanelProps {
  onActionRequest: (action: string, params: Record<string, unknown>) => void;
}

export const AiPanel: React.FC<AiPanelProps> = ({ onActionRequest }) => {
  const [output, setOutput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [prompt, setPrompt] = useState('');

  const handleMessage = useCallback((msg: WsMessage) => {
    if (msg.type === 'taskDelta') {
      setOutput((prev) => prev + (msg.delta as string));
    } else if (msg.type === 'taskStarted') {
      setIsStreaming(true);
      setOutput('');
    } else if (msg.type === 'taskComplete') {
      setIsStreaming(false);
    } else if (msg.type === 'actionRequest') {
      onActionRequest(msg.action as string, (msg.params ?? {}) as Record<string, unknown>);
    }
  }, [onActionRequest]);

  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
  const { send, connected } = useWebSocket(wsUrl, { onMessage: handleMessage });

  const submitPrompt = useCallback((text: string) => {
    if (!text.trim()) return;
    send({ type: 'runTask', task_id: crypto.randomUUID(), task: 'generateText', payload: { prompt: text } });
    setPrompt('');
  }, [send]);

  return (
    <div className="flex flex-col h-full bg-os-bg text-os-text p-3 gap-2">
      <div className={cn("text-xs flex items-center gap-1", connected ? "text-green-400" : "text-yellow-400")}>
        <Bot size={14} />
        {connected ? 'AI Connected' : 'Connecting…'}
        {isStreaming && <Loader2 size={12} className="animate-spin ml-1" />}
      </div>

      <div className="flex-1 bg-os-window border border-os-border rounded-lg p-2 font-mono text-xs overflow-y-auto whitespace-pre-wrap min-h-[100px]">
        {output || <span className="text-os-text/40">AI output will appear here…</span>}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 bg-os-window border border-os-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-os-accent"
          placeholder="Ask AI…"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && submitPrompt(prompt)}
        />
        <VoiceInput onTranscript={(t, final) => final && submitPrompt(t)} />
      </div>
    </div>
  );
};
