import React, { useState, useEffect } from 'react';
import type { AppMeta } from '../types';

export const appMeta: AppMeta = { id: 'pluginmarketplace', title: 'Plugin Marketplace', category: 'System' };

interface Plugin {
  id: string;
  name: string;
  description: string;
  author: string;
  version: string;
  tags: string[];
  installed: boolean;
}

interface PluginsResponse {
  plugins: Plugin[];
}

export function PluginMarketplace() {
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetch('/api/plugins')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<PluginsResponse>;
      })
      .then((data) => {
        setPlugins(data.plugins);
        setLoading(false);
      })
      .catch((err: Error) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const toggleInstall = (id: string) => {
    setPlugins((prev) =>
      prev.map((p) => (p.id === id ? { ...p, installed: !p.installed } : p))
    );
  };

  const filtered = plugins.filter((p) => {
    const q = search.toLowerCase();
    return (
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.tags.some((t) => t.toLowerCase().includes(q))
    );
  });

  return (
    <div className="p-4 h-full overflow-auto bg-os-bg text-os-text flex flex-col gap-4">
      {/* Header + search */}
      <div className="flex items-center gap-2">
        <span className="text-xl">🧩</span>
        <h1 className="text-base font-semibold flex-1">Plugin Marketplace</h1>
        <input
          type="text"
          placeholder="Search plugins…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-os-window border border-os-border rounded px-3 py-1.5 text-sm text-os-text placeholder-os-text/40 focus:outline-none focus:ring-1 focus:ring-os-accent w-56"
        />
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex-1 flex items-center justify-center text-os-text/50 text-sm">
          Loading plugins…
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex-1 flex items-center justify-center text-red-400 text-sm">
          Failed to load plugins: {error}
        </div>
      )}

      {/* Grid */}
      {!loading && !error && (
        <>
          {filtered.length === 0 ? (
            <div className="flex-1 flex items-center justify-center text-os-text/50 text-sm">
              No plugins match &ldquo;{search}&rdquo;
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {filtered.map((plugin) => (
                <div
                  key={plugin.id}
                  className="bg-os-window border border-os-border rounded-xl p-4 flex flex-col gap-2 shadow-sm"
                >
                  {/* Name + version */}
                  <div className="flex items-start justify-between gap-2">
                    <span className="font-semibold text-sm leading-tight">{plugin.name}</span>
                    <span className="text-[10px] font-mono bg-os-border/60 text-os-text/70 px-1.5 py-0.5 rounded shrink-0">
                      v{plugin.version}
                    </span>
                  </div>

                  {/* Description */}
                  <p className="text-xs text-os-text/70 leading-relaxed flex-1">
                    {plugin.description}
                  </p>

                  {/* Author */}
                  <p className="text-[10px] text-os-text/50">by {plugin.author}</p>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-1">
                    {plugin.tags.map((tag) => (
                      <span
                        key={tag}
                        className="text-[10px] bg-os-accent/20 text-os-accent px-1.5 py-0.5 rounded"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  {/* Install / Uninstall toggle */}
                  <button
                    onClick={() => toggleInstall(plugin.id)}
                    className={`mt-1 w-full py-1.5 rounded text-xs font-medium transition-colors ${
                      plugin.installed
                        ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30'
                        : 'bg-os-accent/20 text-os-accent hover:bg-os-accent/30'
                    }`}
                  >
                    {plugin.installed ? 'Uninstall' : 'Install'}
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
