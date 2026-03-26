/**
 * AgentChat — full-screen streaming chat app for desktop-like UI.
 *
 * Connects to the PyAgent backend WebSocket for real-time agent responses.
 * Each message delta is appended to the current assistant bubble as it arrives.
 */
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Bot, User, Send, StopCircle, Loader2, Trash2 } from 'lucide-react';
import { useWebSocket, WsMessage } from '../hooks/useWebSocket';
import { cn } from '../utils';
import type { AppMeta } from '../types';

export const appMeta: AppMeta = { id: 'agentchat', title: 'Agent Chat', category: 'AI Agents' };

interface Message {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  done: boolean;
}

function newId(): string {
  return crypto.randomUUID();
}

export const AgentChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [activeTaskId, setActiveTaskId] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  // Auto-scroll to bottom when new content arrives
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleMessage = useCallback((msg: WsMessage) => {
    if (msg.type === 'taskStarted') {
      const taskId = msg.task_id as string;
      setActiveTaskId(taskId);
      setMessages((prev) => [
        ...prev,
        { id: taskId, role: 'assistant', text: '', done: false },
      ]);
    } else if (msg.type === 'taskDelta') {
      const taskId = msg.task_id as string;
      const delta = (msg.delta as string) ?? '';
      setMessages((prev) =>
        prev.map((m) => (m.id === taskId ? { ...m, text: m.text + delta } : m)),
      );
    } else if (msg.type === 'taskComplete') {
      const taskId = msg.task_id as string;
      setMessages((prev) =>
        prev.map((m) => (m.id === taskId ? { ...m, done: true } : m)),
      );
      setActiveTaskId(null);
    } else if (msg.type === 'error') {
      setMessages((prev) => [
        ...prev,
        {
          id: newId(),
          role: 'assistant',
          text: `⚠ Error: ${String(msg.message ?? 'Unknown error')}`,
          done: true,
        },
      ]);
      setActiveTaskId(null);
    }
  }, []);

  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
  const { send, connected } = useWebSocket(wsUrl, { onMessage: handleMessage });

  const submit = useCallback(() => {
    const text = input.trim();
    if (!text || activeTaskId) return;
    const taskId = newId();
    setMessages((prev) => [
      ...prev,
      { id: newId(), role: 'user', text, done: true },
    ]);
    send({ type: 'runTask', task_id: taskId, task: 'chat', payload: { prompt: text } });
    setInput('');
  }, [input, activeTaskId, send]);

  const stopStream = useCallback(() => {
    if (activeTaskId) {
      send({ type: 'cancelTask', task_id: activeTaskId });
    }
  }, [activeTaskId, send]);

  const clearHistory = useCallback(() => {
    setMessages([]);
    setActiveTaskId(null);
  }, []);

  return (
    <div className="flex flex-col h-full bg-os-bg text-os-text">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-os-window border-b border-os-border text-sm">
        <div className="flex items-center gap-2">
          <Bot size={16} className="text-os-accent" />
          <span className="font-semibold">Agent Chat</span>
          <span
            className={cn(
              'text-xs px-1.5 py-0.5 rounded-full',
              connected ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400',
            )}
          >
            {connected ? 'Live' : 'Connecting…'}
          </span>
        </div>
        <button
          onClick={clearHistory}
          title="Clear chat"
          className="p-1 rounded hover:bg-os-hover text-os-text/60 hover:text-os-text"
        >
          <Trash2 size={14} />
        </button>
      </div>

      {/* Message list */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {messages.length === 0 && (
          <div className="text-center text-os-text/40 text-sm mt-8">
            Send a message to start chatting with the AI agent.
          </div>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={cn('flex gap-2 items-start', msg.role === 'user' ? 'flex-row-reverse' : '')}
          >
            <div
              className={cn(
                'shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs',
                msg.role === 'user'
                  ? 'bg-os-accent/20 text-os-accent'
                  : 'bg-os-window border border-os-border text-os-text/60',
              )}
            >
              {msg.role === 'user' ? <User size={12} /> : <Bot size={12} />}
            </div>
            <div
              className={cn(
                'max-w-[80%] rounded-xl px-3 py-2 text-sm font-mono whitespace-pre-wrap leading-relaxed',
                msg.role === 'user'
                  ? 'bg-os-accent/10 border border-os-accent/30'
                  : 'bg-os-window border border-os-border',
              )}
            >
              {msg.text}
              {!msg.done && (
                <span className="inline-block ml-1 w-1.5 h-3.5 bg-os-text/60 animate-pulse rounded-sm" />
              )}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div className="flex items-center gap-2 px-3 py-2 bg-os-window border-t border-os-border">
        <textarea
          rows={1}
          className="flex-1 resize-none bg-os-bg border border-os-border rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-os-accent"
          placeholder="Message the agent…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              submit();
            }
          }}
        />
        {activeTaskId ? (
          <button
            onClick={stopStream}
            title="Stop generation"
            className="p-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30"
          >
            <StopCircle size={16} />
          </button>
        ) : (
          <button
            onClick={submit}
            disabled={!input.trim() || !connected}
            title="Send"
            className="p-2 rounded-lg bg-os-accent/20 text-os-accent hover:bg-os-accent/30 disabled:opacity-40"
          >
            {!connected ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
          </button>
        )}
      </div>
    </div>
  );
};
