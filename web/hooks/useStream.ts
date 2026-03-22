/**
 * useStream — SSE-based streaming hook for PyAgent.
 *
 * Connects to a Server-Sent Events endpoint and exposes the accumulated text,
 * a streaming flag, any error message, and a trigger function.
 */
import { useState, useRef, useCallback } from 'react';

export interface StreamOptions {
  /** SSE endpoint URL (default: /api/stream) */
  url?: string;
  /** Additional headers to send with the POST that initiates the stream */
  headers?: Record<string, string>;
}

export interface StreamState {
  /** Accumulated text received from the stream */
  output: string;
  /** True while the EventSource is open */
  streaming: boolean;
  /** Last error message, or null */
  error: string | null;
  /** Call this to start a new streaming request */
  start: (prompt: string) => void;
  /** Abort the current stream */
  stop: () => void;
}

/**
 * Hook that manages a streaming SSE connection to the PyAgent backend.
 *
 * Usage:
 *   const { output, streaming, error, start, stop } = useStream({ url: '/api/stream' });
 */
export function useStream(options: StreamOptions = {}): StreamState {
  const { url = '/api/stream', headers = {} } = options;

  const [output, setOutput] = useState('');
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const esRef = useRef<EventSource | null>(null);

  const stop = useCallback(() => {
    if (esRef.current) {
      esRef.current.close();
      esRef.current = null;
    }
    setStreaming(false);
  }, []);

  const start = useCallback(
    (prompt: string) => {
      // Close any existing connection first
      stop();
      setOutput('');
      setError(null);
      setStreaming(true);

      // POST the prompt to trigger the stream, then connect via SSE
      const params = new URLSearchParams({ prompt });
      const fullUrl = `${url}?${params.toString()}`;

      // Merge caller-provided headers (note: EventSource doesn't support custom headers
      // natively; callers requiring auth should proxy via a fetch-based approach instead)
      void headers; // reserved for future fetch-based streaming

      const es = new EventSource(fullUrl);
      esRef.current = es;

      es.onmessage = (event) => {
        if (event.data === '[DONE]') {
          stop();
          return;
        }
        try {
          const parsed = JSON.parse(event.data) as { delta?: string; text?: string };
          const chunk = parsed.delta ?? parsed.text ?? event.data;
          setOutput((prev) => prev + chunk);
        } catch {
          // plain-text chunk
          setOutput((prev) => prev + event.data);
        }
      };

      es.onerror = () => {
        setError('Stream connection error');
        stop();
      };
    },
    [url, headers, stop],
  );

  return { output, streaming, error, start, stop };
}
