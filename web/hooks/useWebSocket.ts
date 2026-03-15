import { useEffect, useRef, useCallback, useState } from 'react';

export interface WsMessage {
  type: string;
  [key: string]: unknown;
}

export interface UseWebSocketOptions {
  onMessage?: (msg: WsMessage) => void;
  reconnectDelay?: number;
}

// Custom hook for managing a WebSocket connection with automatic reconnection.
export function useWebSocket(url: string, options: UseWebSocketOptions = {}) {
  const wsRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const { onMessage, reconnectDelay = 2000 } = options;

  // Keep latest values in refs so the effect never captures stale closures.
  const onMessageRef = useRef(onMessage);
  const reconnectDelayRef = useRef(reconnectDelay);
  onMessageRef.current = onMessage;
  reconnectDelayRef.current = reconnectDelay;

  useEffect(() => {
    let active = true;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
    function connect() {
      if (!active) return;
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => { if (active) setConnected(true); };
      ws.onclose = () => {
        if (active) {
          setConnected(false);
          reconnectTimer = setTimeout(connect, reconnectDelayRef.current);
        }
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

  return { send, connected };
}
