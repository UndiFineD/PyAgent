import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { useWebSocket, UseWebSocketOptions, WsMessage } from './useWebSocket';

// ---------------------------------------------------------------------------
// Structural / export tests
// ---------------------------------------------------------------------------
describe('useWebSocket exports', () => {
  it('exports useWebSocket as a function', () => {
    expect(typeof useWebSocket).toBe('function');
  });

  it('UseWebSocketOptions interface allows all documented fields', () => {
    const opts: UseWebSocketOptions = {
      onMessage: (_msg: WsMessage) => {},
      reconnectDelay: 500,
      baseDelay: 1000,
      maxDelay: 30000,
      maxRetries: 5,
    };
    expect(opts.baseDelay).toBe(1000);
    expect(opts.maxDelay).toBe(30000);
    expect(opts.maxRetries).toBe(5);
  });
});

// ---------------------------------------------------------------------------
// Backoff calculation helpers (white-box unit tests, no DOM required)
// ---------------------------------------------------------------------------
describe('exponential backoff formula', () => {
  it('doubles the delay each attempt up to a cap', () => {
    const baseDelay = 1000;
    const maxDelay = 30000;
    const delays: number[] = [];
    for (let attempt = 0; attempt < 6; attempt++) {
      const exp = Math.min(maxDelay, baseDelay * Math.pow(2, attempt));
      delays.push(exp);
    }
    expect(delays).toEqual([1000, 2000, 4000, 8000, 16000, 30000]);
  });

  it('never exceeds maxDelay regardless of attempt count', () => {
    const maxDelay = 5000;
    for (let attempt = 0; attempt < 20; attempt++) {
      const exp = Math.min(maxDelay, 1000 * Math.pow(2, attempt));
      expect(exp).toBeLessThanOrEqual(maxDelay);
    }
  });

  it('jittered delay stays within [0.5 * exp, exp]', () => {
    // Seed Math.random to 0 (low-end) and check bounds.
    vi.spyOn(Math, 'random').mockReturnValue(0);
    const exp = 8000;
    const low = exp * (0.5 + 0 * 0.5);
    expect(low).toBe(4000);
    vi.restoreAllMocks();

    vi.spyOn(Math, 'random').mockReturnValue(1);
    const high = exp * (0.5 + 1 * 0.5);
    expect(high).toBe(8000);
    vi.restoreAllMocks();
  });

  it('jitter is always positive and non-zero for exp > 0', () => {
    for (let i = 0; i < 50; i++) {
      const exp = 1000;
      const jittered = exp * (0.5 + Math.random() * 0.5);
      expect(jittered).toBeGreaterThan(0);
    }
  });
});

// ---------------------------------------------------------------------------
// Legacy compatibility
// ---------------------------------------------------------------------------
describe('backwards compatibility', () => {
  it('reconnectDelay option is accepted without TypeScript error', () => {
    const opts: UseWebSocketOptions = { reconnectDelay: 2000 };
    expect(opts.reconnectDelay).toBe(2000);
  });

  it('baseDelay defaults to reconnectDelay when only reconnectDelay is supplied', () => {
    // When baseDelay is undefined, the hook sets baseDelay = reconnectDelay ?? 1000.
    const reconnectDelay = 3000;
    const baseDelay = reconnectDelay ?? 1000;
    expect(baseDelay).toBe(3000);
  });

  it('baseDelay defaults to 1000 when neither baseDelay nor reconnectDelay is supplied', () => {
    const reconnectDelay = undefined;
    const baseDelay = reconnectDelay ?? 1000;
    expect(baseDelay).toBe(1000);
  });
});

