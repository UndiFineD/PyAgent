export type ActionHandler = (params: Record<string, unknown>) => Promise<void> | void;

export class ActionRegistry {
  private _handlers = new Map<string, ActionHandler>();

  register(action: string, handler: ActionHandler): void {
    this._handlers.set(action, handler);
  }

  has(action: string): boolean {
    return this._handlers.has(action);
  }

  async execute(action: string, params: Record<string, unknown>): Promise<void> {
    const handler = this._handlers.get(action);
    if (!handler) {
      throw new Error(`Unknown action: "${action}". Not registered in ActionRegistry.`);
    }
    await handler(params);
  }
}

/** Build a default registry wired to the NebulaOS app state. */
export function createDefaultRegistry(openApp: (appId: string) => void): ActionRegistry {
  const registry = new ActionRegistry();

  registry.register('openWindow', async (params) => {
    const appId = params['appId'] as string;
    if (!appId) throw new Error('openWindow requires appId param');
    openApp(appId);
  });

  registry.register('log', async (params) => {
    console.log('[ActionRegistry:log]', params);
  });

  return registry;
}
