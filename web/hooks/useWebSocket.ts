import { useEffect, useRef, useCallback, useState } from 'react';

export interface WsMessage {
  type: string;
  [key: string]: unknown;
}

export interface UseWebSocketOptions {
  onMessage?: (msg: WsMessage) => void;
  reconnectDelay?: number;
}

export function useWebSocket(url: string, options: UseWebSocketOptions = {}) {
  const wsRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);
  const { onMessage, reconnectDelay = 2000 } = options;

  useEffect(() => {
    let active = true;
    function connect() {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => { if (active) setConnected(true); };
      ws.onclose = () => {
        if (active) {
          setConnected(false);
          setTimeout(connect, reconnectDelay);
        }
      };
      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data) as WsMessage;
          onMessage?.(msg);
        } catch { /* ignore malformed messages */ }
      };
    }
    connect();
    return () => {
      active = false;
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
