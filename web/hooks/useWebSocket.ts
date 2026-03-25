import { useEffect, useRef, useCallback, useState } from 'react';

export interface WsMessage {
  type: string;
  [key: string]: unknown;
}

export interface UseWebSocketOptions {
  onMessage?: (msg: WsMessage) => void;
  /** @deprecated Use baseDelay instead. Kept for backwards compatibility. */
  reconnectDelay?: number;
  /** Initial reconnect delay in ms before jitter (default: 1000). */
  baseDelay?: number;
  /** Maximum reconnect delay cap in ms (default: 30000). */
  maxDelay?: number;
  /** Maximum number of reconnect attempts before giving up (default: Infinity). */
  maxRetries?: number;
}

// Custom hook for managing a WebSocket connection with automatic reconnection,
// exponential backoff, and jitter to prevent thundering-herd reconnect storms.
export function useWebSocket(url: string, options: UseWebSocketOptions = {}) {
  const wsRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);

  const {
    onMessage,
    reconnectDelay,
    baseDelay = reconnectDelay ?? 1000,
    maxDelay = 30000,
    maxRetries = Infinity,
  } = options;

  // Keep latest values in refs so the effect never captures stale closures.
  const onMessageRef = useRef(onMessage);
  const baseDelayRef = useRef(baseDelay);
  const maxDelayRef = useRef(maxDelay);
  const maxRetriesRef = useRef(maxRetries);
  onMessageRef.current = onMessage;
  baseDelayRef.current = baseDelay;
  maxDelayRef.current = maxDelay;
  maxRetriesRef.current = maxRetries;

  useEffect(() => {
    let active = true;
    let attempt = 0;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

    function connect() {
      if (!active) return;
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        if (!active) return;
        attempt = 0;
        setReconnectAttempts(0);
        setConnected(true);
      };

      ws.onclose = () => {
        if (!active) return;
        setConnected(false);
        if (attempt >= maxRetriesRef.current) return;
        // Exponential backoff: baseDelay * 2^attempt, capped at maxDelay.
        const exp = Math.min(maxDelayRef.current, baseDelayRef.current * Math.pow(2, attempt));
        // Full jitter: random value in [0.5 * exp, exp] to spread reconnect load.
        const jittered = exp * (0.5 + Math.random() * 0.5);
        attempt += 1;
        setReconnectAttempts(attempt);
        reconnectTimer = setTimeout(connect, jittered);
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data) as WsMessage;
          onMessageRef.current?.(msg);
        } catch { /* ignore malformed messages */ }
      };
    }

    connect();

    return () => {
      active = false;
      if (reconnectTimer !== null) clearTimeout(reconnectTimer);
      wsRef.current?.close();
    };
  }, [url]);

  const send = useCallback((msg: WsMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(msg));
    }
  }, []);

  return { send, connected, reconnectAttempts };
}

