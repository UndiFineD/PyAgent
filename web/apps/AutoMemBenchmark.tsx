import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  LineChart, Line, BarChart, Bar, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  ReferenceLine, Cell,
} from 'recharts';
import type { AppMeta } from '../types';

export const appMeta: AppMeta = { id: 'autobenchmark', title: 'AutoMem Benchmark', category: 'AI Agents' };

// ---------------------------------------------------------------------------
// Types (mirrors BenchmarkRunner.py dataclasses)
// ---------------------------------------------------------------------------

interface OperationResult {
  backend:      'postgres' | 'memory' | string;
  operation:     'write' | 'read' | 'sort' | 'search';
  method:        string;
  rows:          number;
  latency_ms:    number;
  rows_returned: number;
  status?:       'ok' | 'fallback' | 'unavailable' | string;
  metadata?:     Record<string, unknown>;
}

interface BenchmarkReport {
  run_id:       string;
  total_rows:   number;
  results:      OperationResult[];
  errors:       string[];
  completed_at: string | null;
  backends?:    string[];
}

// ---------------------------------------------------------------------------
// Colour palette — one distinct colour per method
// ---------------------------------------------------------------------------
const METHOD_COLORS: Record<string, string> = {
  btree_insert:       '#6366f1',
  btree_pk:           '#3b82f6',
  hash_agent_id:      '#22d3ee',
  btree_importance_desc: '#10b981',
  btree_created_desc:    '#84cc16',
  btree_access_count:    '#a3e635',
  hnsw_vector:        '#f59e0b',
  gin_fulltext:       '#ef4444',
  gin_keywords:       '#ec4899',
  brin_timestamp:     '#8b5cf6',
  full_seqscan:       '#6b7280',
  ltree_subtree:      '#f97316',
};

function methodColor(method: string): string {
  return METHOD_COLORS[method] ?? '#94a3b8';
}

// Nice human-readable label per method
const METHOD_LABEL: Record<string, string> = {
  btree_insert:              'B-tree INSERT',
  btree_pk:                  'B-tree PK read',
  hash_agent_id:             'Hash equality',
  btree_importance_desc:     'B-tree sort (importance)',
  btree_created_desc:        'B-tree sort (recency)',
  btree_access_count:        'B-tree sort (access)',
  hnsw_vector:               'HNSW vector ANN',
  gin_fulltext:              'GIN full-text',
  gin_keywords:              'GIN keywords',
  brin_timestamp:            'BRIN range scan',
  full_seqscan:              'Seq-scan (baseline)',
  ltree_subtree:             'LTREE subtree',
};

function fmtLabel(method: string): string {
  return METHOD_LABEL[method] ?? method;
}

function backendLabel(backend: string): string {
  return backend.toLowerCase() === 'postgres' ? 'Postgres' : 'Memory';
}

function seriesKey(result: OperationResult): string {
  return `${result.backend}::${result.method}`;
}

function splitSeriesKey(key: string): { backend: string; method: string } {
  const [backend, method] = key.split('::');
  return { backend: backend ?? 'unknown', method: method ?? key };
}

function fmtSeriesLabel(key: string): string {
  const { backend, method } = splitSeriesKey(key);
  return `${backendLabel(backend)} · ${fmtLabel(method)}`;
}

function seriesColor(key: string): string {
  const { backend, method } = splitSeriesKey(key);
  const base = methodColor(method);
  if (backend.toLowerCase() === 'postgres') return base;
  return `${base}99`;
}

// ---------------------------------------------------------------------------
// Derived data helpers
// ---------------------------------------------------------------------------

/** Build data for a line chart: x = rows, y = latency_ms, one series per method. */
function latencyLineData(
  results: OperationResult[],
  operationFilter: string,
): { rows: number; [series: string]: number }[] {
  const filtered = results.filter(r => r.operation === operationFilter);
  const rowTiers = [...new Set(filtered.map(r => r.rows))].sort((a, b) => a - b);
  const series  = [...new Set(filtered.map(r => seriesKey(r)))];
  return rowTiers.map(rows => {
    const point: { rows: number; [k: string]: number } = { rows };
    for (const key of series) {
      const entry = filtered.find(r => r.rows === rows && seriesKey(r) === key);
      if (entry) point[key] = entry.latency_ms;
    }
    return point;
  });
}

/** Build bar chart data: one bar per method at the highest row-count tier. */
function latencyBarData(
  results: OperationResult[],
  operationFilter: string,
): { method: string; backend: string; series: string; label: string; latency_ms: number }[] {
  const filtered = results.filter(r => r.operation === operationFilter);
  const maxRows  = Math.max(...filtered.map(r => r.rows), 0);
  const bySeries = new Map<string, { method: string; backend: string; latency_ms: number }>();
  for (const r of filtered) {
    if (r.rows === maxRows) {
      const key = seriesKey(r);
      bySeries.set(key, {
        method: r.method,
        backend: r.backend,
        latency_ms: r.latency_ms,
      });
    }
  }
  return [...bySeries.entries()].map(([series, info]) => ({
    method: info.method,
    backend: info.backend,
    series,
    label: `${backendLabel(info.backend)} · ${fmtLabel(info.method)}`,
    latency_ms: info.latency_ms,
  }));
}

/** Build scatter data: all results mapped to {rows, latency_ms, method}. */
function scatterData(
  results: OperationResult[],
): { rows: number; latency_ms: number; method: string; backend: string; series: string }[] {
  return results.map(r => ({
    rows: r.rows,
    latency_ms: r.latency_ms,
    method: r.method,
    backend: r.backend,
    series: seriesKey(r),
  }));
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

interface SectionProps { title: string; children: React.ReactNode }

function Section({ title, children }: SectionProps) {
  return (
    <div style={{ marginBottom: 32 }}>
      <h3 style={{ color: '#e2e8f0', marginBottom: 12, fontSize: 15, fontWeight: 600 }}>{title}</h3>
      {children}
    </div>
  );
}

function CustomTooltipContent({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: '#1e293b', border: '1px solid #334155',
      borderRadius: 6, padding: '8px 12px', fontSize: 12,
    }}>
      <p style={{ color: '#94a3b8', marginBottom: 4 }}>rows: {label?.toLocaleString()}</p>
      {payload.map((p: any) => (
        <p key={p.dataKey} style={{ color: p.color, margin: '2px 0' }}>
          {fmtSeriesLabel(p.dataKey)}: <strong>{p.value} ms</strong>
        </p>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// MAIN COMPONENT
// ---------------------------------------------------------------------------

export function AutoMemBenchmark() {
  const [report, setReport]       = useState<BenchmarkReport | null>(null);
  const [running, setRunning]     = useState(false);
  const [progress, setProgress]   = useState(0);   // 0-100
  const [error, setError]         = useState<string | null>(null);
  const [liveMode, setLiveMode]   = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // ---- Fetch latest benchmark from backend  ----
  const fetchLatest = useCallback(async () => {
    try {
      const res = await fetch('/api/automem/benchmark/latest');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: BenchmarkReport = await res.json();
      setReport(data);
      setError(null);
    } catch {
      setError('Unable to load benchmark data from backend.');
    }
  }, []);

  // ---- Trigger a new benchmark run ----
  const runBenchmark = useCallback(async () => {
    setRunning(true);
    setProgress(0);
    setError(null);
    // Simulate progress while the server processes
    let p = 0;
    const ticker = setInterval(() => {
      p = Math.min(p + 4, 92);
      setProgress(p);
    }, 300);
    try {
      const res = await fetch('/api/automem/benchmark/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ row_counts: [100, 500, 1000], backends: ['postgres', 'memory'] }),
      });
      clearInterval(ticker);
      setProgress(100);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: BenchmarkReport = await res.json();
      setReport(data);
    } catch {
      clearInterval(ticker);
      setError('Benchmark run failed. Verify backend connection and try again.');
    } finally {
      setRunning(false);
      setTimeout(() => setProgress(0), 800);
    }
  }, []);

  // ---- Live-refresh mode ----
  useEffect(() => {
    if (liveMode) {
      fetchLatest();
      timerRef.current = setInterval(fetchLatest, 4000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [liveMode, fetchLatest]);

  // Initial load
  useEffect(() => { fetchLatest(); }, [fetchLatest]);

  // ---- Derived chart data ----
  const results = report?.results ?? [];

  const writeLineData  = latencyLineData(results, 'write');
  const readLineData   = latencyLineData(results, 'read');
  const sortLineData   = latencyLineData(results, 'sort');
  const searchBarData  = latencyBarData(results, 'search');
  const scatter        = scatterData(results);

  const allSeriesOnWrite  = [...new Set(results.filter(r => r.operation === 'write' ).map(seriesKey))];
  const allSeriesOnRead   = [...new Set(results.filter(r => r.operation === 'read'  ).map(seriesKey))];
  const allSeriesOnSort   = [...new Set(results.filter(r => r.operation === 'sort'  ).map(seriesKey))];
  const statusNotes = results.filter(r => (r.status && r.status !== 'ok') || (r.metadata && Object.keys(r.metadata).length > 0));

  // ---- Render ----
  return (
    <div style={{
      background: '#0f172a', color: '#e2e8f0',
      padding: 24, fontFamily: 'system-ui, sans-serif',
      minHeight: '100vh',
    }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 24 }}>
        <div>
          <h2 style={{ margin: 0, fontSize: 20, color: '#f1f5f9' }}>
            AutoMem Index Benchmark
          </h2>
          {report && (
            <p style={{ margin: 0, fontSize: 12, color: '#64748b' }}>
              Run&nbsp;{report.run_id} · {report.total_rows.toLocaleString()} rows ·{' '}
              {report.completed_at
                ? new Date(report.completed_at).toLocaleTimeString()
                : 'in progress…'}
            </p>
          )}
        </div>

        <div style={{ marginLeft: 'auto', display: 'flex', gap: 10, alignItems: 'center' }}>
          {/* Live toggle */}
          <button
            onClick={() => setLiveMode(v => !v)}
            style={{
              padding: '6px 14px', borderRadius: 6, border: 'none',
              background: liveMode ? '#16a34a' : '#334155',
              color: '#f1f5f9', cursor: 'pointer', fontSize: 12,
            }}
          >
            {liveMode ? '● LIVE' : '○ Live'}
          </button>

          {/* Run benchmark */}
          <button
            onClick={runBenchmark}
            disabled={running}
            style={{
              padding: '6px 18px', borderRadius: 6, border: 'none',
              background: running ? '#475569' : '#6366f1',
              color: '#f1f5f9', cursor: running ? 'not-allowed' : 'pointer',
              fontSize: 13, fontWeight: 600,
            }}
          >
            {running ? 'Running…' : 'Run Benchmark'}
          </button>
        </div>
      </div>

      {/* Progress bar */}
      {progress > 0 && (
        <div style={{
          height: 4, background: '#1e293b', borderRadius: 2,
          marginBottom: 20, overflow: 'hidden',
        }}>
          <div style={{
            height: '100%', width: `${progress}%`,
            background: 'linear-gradient(90deg,#6366f1,#22d3ee)',
            transition: 'width 0.3s',
          }} />
        </div>
      )}

      {error && (
        <div style={{
          padding: '8px 12px', background: '#450a0a', borderRadius: 6,
          color: '#fca5a5', marginBottom: 16, fontSize: 12,
        }}>{error}</div>
      )}

      {/* Legend / index type reference */}
      <div style={{
        display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 24,
      }}>
        {Object.entries(METHOD_LABEL).map(([k, label]) => (
          <span key={k} style={{
            padding: '3px 10px', borderRadius: 12,
            background: '#1e293b', border: `1px solid ${methodColor(k)}`,
            color: methodColor(k), fontSize: 11,
          }}>
            {label}
          </span>
        ))}
      </div>

      {/* ① WRITE latency per row tier */}
      <Section title="① WRITE — Insert latency per row tier (ms / row)">
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={writeLineData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="rows" stroke="#64748b" tickFormatter={v => v.toLocaleString()} label={{ value: 'Rows', position: 'insideBottom', offset: -5, fill: '#64748b', fontSize: 11 }} />
            <YAxis stroke="#64748b" label={{ value: 'ms / row', angle: -90, position: 'insideLeft', fill: '#64748b', fontSize: 11 }} />
            <Tooltip content={<CustomTooltipContent />} />
            <Legend formatter={v => <span style={{ color: seriesColor(String(v)), fontSize: 11 }}>{fmtSeriesLabel(String(v))}</span>} />
            {allSeriesOnWrite.map(s => (
              <Line key={s} type="monotone" dataKey={s} stroke={seriesColor(s)} dot={false} strokeWidth={2} />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </Section>

      {/* ② READ latency */}
      <Section title="② READ — Point-lookup latency by index type (ms)">
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={readLineData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="rows" stroke="#64748b" tickFormatter={v => v.toLocaleString()} />
            <YAxis stroke="#64748b" />
            <Tooltip content={<CustomTooltipContent />} />
            <Legend formatter={v => <span style={{ color: seriesColor(String(v)), fontSize: 11 }}>{fmtSeriesLabel(String(v))}</span>} />
            {allSeriesOnRead.map(s => (
              <Line key={s} type="monotone" dataKey={s} stroke={seriesColor(s)} dot={false} strokeWidth={2} />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </Section>

      {/* ③ SORT latency */}
      <Section title="③ SORT — ORDER BY latency by column (ms)">
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={sortLineData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="rows" stroke="#64748b" tickFormatter={v => v.toLocaleString()} />
            <YAxis stroke="#64748b" />
            <Tooltip content={<CustomTooltipContent />} />
            <Legend formatter={v => <span style={{ color: seriesColor(String(v)), fontSize: 11 }}>{fmtSeriesLabel(String(v))}</span>} />
            {allSeriesOnSort.map(s => (
              <Line key={s} type="monotone" dataKey={s} stroke={seriesColor(s)} dot={false} strokeWidth={2} />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </Section>

      {/* ④ SEARCH bar comparison */}
      <Section title="④ SEARCH — At-scale latency comparison by search method (ms)">
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={searchBarData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis type="number" stroke="#64748b" domain={[0, 'auto']} label={{ value: 'ms', position: 'insideBottomRight', fill: '#64748b', fontSize: 11 }} />
            <YAxis type="category" dataKey="label" stroke="#64748b" width={160} tick={{ fontSize: 11, fill: '#94a3b8' }} />
            <Tooltip formatter={(v: number) => [`${v} ms`, 'Latency']} contentStyle={{ background: '#1e293b', border: '1px solid #334155', fontFamily: 'monospace' }} />
            <ReferenceLine x={10} stroke="#ef4444" strokeDasharray="4 2" label={{ value: '10ms', fill: '#ef4444', fontSize: 10 }} />
            <Bar dataKey="latency_ms" radius={[0, 4, 4, 0]}>
              {searchBarData.map((entry) => (
                <Cell key={entry.series} fill={seriesColor(entry.series)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Section>

      {/* ⑤ Scatter: all operations */}
      <Section title="⑤ SCATTER — All operations: rows × latency  (every index type)">
        <ResponsiveContainer width="100%" height={260}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="rows" name="Rows" stroke="#64748b" tickFormatter={v => v.toLocaleString()} label={{ value: 'Rows in table', position: 'insideBottom', offset: -5, fill: '#64748b', fontSize: 11 }} />
            <YAxis dataKey="latency_ms" name="Latency (ms)" stroke="#64748b" label={{ value: 'ms', angle: -90, position: 'insideLeft', fill: '#64748b', fontSize: 11 }} />
            <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ background: '#1e293b', border: '1px solid #334155', fontSize: 12 }} formatter={(value: number, name: string, props: any) => {
              const key = props?.payload?.series ?? '';
              return [`${value} ms`, fmtSeriesLabel(key) || name];
            }} />
            {[...new Set(scatter.map(d => d.series))].map(key => (
              <Scatter
                key={key}
                name={fmtSeriesLabel(key)}
                data={scatter.filter(d => d.series === key)}
                fill={seriesColor(key)}
              />
            ))}
            <Legend formatter={v => <span style={{ color: seriesColor(String(v)), fontSize: 11 }}>{fmtSeriesLabel(String(v))}</span>} />
          </ScatterChart>
        </ResponsiveContainer>
      </Section>

      {statusNotes.length > 0 && (
        <Section title="⑦ Backend notes — fallback/unavailable markers">
          <div style={{ display: 'grid', gap: 8 }}>
            {statusNotes.map((entry, idx) => (
              <div
                key={`${entry.backend}-${entry.operation}-${entry.method}-${entry.rows}-${idx}`}
                style={{
                  border: '1px solid #334155',
                  background: '#1e293b',
                  borderRadius: 6,
                  padding: '8px 10px',
                  fontSize: 12,
                  color: '#cbd5e1',
                }}
              >
                <strong>{backendLabel(entry.backend)} · {fmtLabel(entry.method)}</strong>
                <span style={{ marginLeft: 8, color: '#94a3b8' }}>
                  status: {entry.status ?? 'ok'}
                </span>
                {entry.metadata && Object.keys(entry.metadata).length > 0 && (
                  <div style={{ marginTop: 4, color: '#a5b4fc' }}>
                    {JSON.stringify(entry.metadata)}
                  </div>
                )}
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* ⑥ Index type summary table */}
      <Section title="⑥ Index Reference Table">
        <div style={{ overflowX: 'auto' }}>
          <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: 12 }}>
            <thead>
              <tr style={{ background: '#1e293b', color: '#94a3b8' }}>
                {['Index', 'Type', 'Column(s)', 'Used for'].map(h => (
                  <th key={h} style={{ padding: '8px 12px', textAlign: 'left', borderBottom: '1px solid #334155' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {INDEX_TABLE.map((row, i) => (
                <tr key={i} style={{ background: i % 2 === 0 ? '#0f172a' : '#131e2e' }}>
                  <td style={{ padding: '6px 12px', fontFamily: 'monospace', color: '#7dd3fc' }}>{row.name}</td>
                  <td style={{ padding: '6px 12px', color: methodColor(METHOD_TYPE_MAP[row.type] ?? '') }}>{row.type}</td>
                  <td style={{ padding: '6px 12px', fontFamily: 'monospace', color: '#a78bfa' }}>{row.cols}</td>
                  <td style={{ padding: '6px 12px', color: '#94a3b8' }}>{row.purpose}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Static data — index reference table
// ---------------------------------------------------------------------------

const METHOD_TYPE_MAP: Record<string, string> = {
  'B-tree':  'btree_pk',
  'HNSW':    'hnsw_vector',
  'GIN':     'gin_fulltext',
  'GiST':    'ltree_subtree',
  'SP-GiST': 'ltree_subtree',
  'BRIN':    'brin_timestamp',
  'Hash':    'hash_agent_id',
};

const INDEX_TABLE = [
  { name: 'idx_mem_agent_id',          type: 'B-tree',  cols: 'agent_id',              purpose: 'Agent scoping' },
  { name: 'idx_mem_created_at',         type: 'B-tree',  cols: 'created_at DESC',        purpose: 'Recency sort (component ⑨)' },
  { name: 'idx_mem_importance',         type: 'B-tree',  cols: 'importance DESC',         purpose: 'Importance sort (component ⑥)' },
  { name: 'idx_mem_access',             type: 'B-tree',  cols: 'access_count DESC',       purpose: 'Frecency query (component ⑨)' },
  { name: 'idx_mem_agent_recent',       type: 'B-tree',  cols: '(agent_id, created_at)',  purpose: 'Hot-path composite read' },
  { name: 'idx_mem_hnsw',               type: 'HNSW',    cols: 'embedding (cosine)',       purpose: 'Vector ANN (component ①)' },
  { name: 'idx_mem_tsv',                type: 'GIN',     cols: 'tsv tsvector',             purpose: 'Full-text / lexical (component ⑤)' },
  { name: 'idx_mem_keywords',           type: 'GIN',     cols: 'keywords TEXT[]',           purpose: 'Keyword match (component ④)' },
  { name: 'idx_mem_tags',               type: 'GIN',     cols: 'tags TEXT[]',              purpose: 'Tag filter' },
  { name: 'idx_mem_metadata',           type: 'GIN',     cols: 'metadata JSONB',            purpose: 'Metadata / JSONB filter' },
  { name: 'idx_mem_path',               type: 'GiST',    cols: 'path LTREE',                purpose: 'Hierarchy traversal (component ⑧)' },
  { name: 'idx_mem_content_trgm',       type: 'GiST',    cols: 'content (trgm)',             purpose: 'LIKE / trigram similarity' },
  { name: 'idx_mem_path_spgist',        type: 'SP-GiST', cols: 'path LTREE',                purpose: 'Alt. hierarchy index (space-partitioned)' },
  { name: 'idx_mem_brin_created',       type: 'BRIN',    cols: 'created_at',                purpose: 'Range scan on large tables (component ③)' },
  { name: 'idx_mem_hash_agent',         type: 'Hash',    cols: 'agent_id',                  purpose: 'Equality-only fast agent lookup' },
  { name: 'idx_mem_hash_session',       type: 'Hash',    cols: 'session_id',                purpose: 'Equality-only session lookup' },
];

export default AutoMemBenchmark;
