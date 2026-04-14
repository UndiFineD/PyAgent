import React, { useState, useEffect } from 'react';
import type { AppMeta } from '../types';

export const appMeta: AppMeta = { id: 'flmdashboard', title: 'FLM Dashboard', category: 'System' };

interface FLMSample {
  timestamp: number;
  tokens_per_second: number;
  model: string;
  queue_depth: number;
}

interface FLMMetrics {
  samples: FLMSample[];
  avg_tokens_per_second: number;
  peak_tokens_per_second: number;
  model: string;
}

export function FLMDashboard() {
  const [data, setData] = useState<FLMMetrics | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const tick = async () => {
      try {
        const res = await fetch('/api/metrics/flm');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json: FLMMetrics = await res.json();
        setData(json);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Fetch error');
      }
    };

    tick();
    const id = setInterval(tick, 2000);
    return () => clearInterval(id);
  }, []);

  const samples = data?.samples ?? [];
  const maxTps = samples.length > 0 ? Math.max(...samples.map(s => s.tokens_per_second)) : 1;
  const latestQueueDepth = samples.length > 0 ? samples[samples.length - 1].queue_depth : 0;

  const BAR_WIDTH = 18;
  const BAR_GAP = 4;
  const MAX_HEIGHT = 100;
  const CHART_WIDTH = samples.length * (BAR_WIDTH + BAR_GAP);
  const CHART_HEIGHT = 110;

  return (
    <div
      style={{
        padding: '16px',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        fontFamily: 'monospace',
        color: 'var(--os-text, #e2e8f0)',
        background: 'var(--os-window, #1e293b)',
        borderRadius: '8px',
        overflow: 'auto',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span style={{ fontSize: '18px' }}>📊</span>
        <span style={{ fontSize: '14px', fontWeight: 700, letterSpacing: '0.05em' }}>
          FLM Token Throughput
        </span>
      </div>

      {error && (
        <div style={{ color: '#f87171', fontSize: '12px' }}>Error: {error}</div>
      )}

      {!data && !error && (
        <div style={{ fontSize: '12px', opacity: 0.6 }}>Loading…</div>
      )}

      {data && (
        <>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px',
              fontSize: '12px',
            }}
          >
            <div>
              <div style={{ opacity: 0.6, fontSize: '10px', textTransform: 'uppercase' }}>
                Model
              </div>
              <div style={{ fontWeight: 600 }}>{data.model}</div>
            </div>
            <div>
              <div style={{ opacity: 0.6, fontSize: '10px', textTransform: 'uppercase' }}>
                Queue Depth
              </div>
              <div style={{ fontWeight: 600 }}>{latestQueueDepth}</div>
            </div>
            <div>
              <div style={{ opacity: 0.6, fontSize: '10px', textTransform: 'uppercase' }}>
                Avg TPS
              </div>
              <div style={{ fontWeight: 600, color: '#4ade80' }}>
                {data.avg_tokens_per_second.toFixed(1)}
              </div>
            </div>
            <div>
              <div style={{ opacity: 0.6, fontSize: '10px', textTransform: 'uppercase' }}>
                Peak TPS
              </div>
              <div style={{ fontWeight: 600, color: '#facc15' }}>
                {data.peak_tokens_per_second.toFixed(1)}
              </div>
            </div>
          </div>

          <div>
            <div
              style={{
                opacity: 0.6,
                fontSize: '10px',
                textTransform: 'uppercase',
                marginBottom: '4px',
              }}
            >
              Tokens / sec — last 10 samples
            </div>
            <svg
              viewBox={`0 0 ${CHART_WIDTH || 220} ${CHART_HEIGHT}`}
              width="100%"
              style={{ maxWidth: '360px', display: 'block' }}
              aria-label="FLM token throughput bar chart"
            >
              {samples.map((s, i) => {
                const barH = Math.max(2, (s.tokens_per_second / maxTps) * MAX_HEIGHT);
                const x = i * (BAR_WIDTH + BAR_GAP);
                const y = MAX_HEIGHT - barH + 4; // +4 for top padding
                return (
                  <rect
                    key={i}
                    x={x}
                    y={y}
                    width={BAR_WIDTH}
                    height={barH}
                    rx={3}
                    fill="#4ade80"
                    opacity={0.85}
                  />
                );
              })}
            </svg>
          </div>

          <div style={{ fontSize: '10px', opacity: 0.4, marginTop: 'auto' }}>
            Refreshes every 2 s · simulated data
          </div>
        </>
      )}
    </div>
  );
}
