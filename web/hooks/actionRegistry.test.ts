import { describe, it, expect, vi } from 'vitest';
import { ActionRegistry, createDefaultRegistry } from './actionRegistry';

describe('ActionRegistry', () => {
  it('executes a registered action', async () => {
    const registry = new ActionRegistry();
    const handler = vi.fn();
    registry.register('test', handler);
    await registry.execute('test', { x: 1 });
    expect(handler).toHaveBeenCalledWith({ x: 1 });
  });

  it('throws for unknown action', async () => {
    const registry = new ActionRegistry();
    await expect(registry.execute('unknown', {})).rejects.toThrow();
  });

  it('createDefaultRegistry includes openWindow action', () => {
    const registry = createDefaultRegistry(() => {});
    expect(registry.has('openWindow')).toBe(true);
  });
});
