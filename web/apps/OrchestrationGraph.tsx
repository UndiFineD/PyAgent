import React, { useState, useEffect, useCallback } from 'react';
import type { AppMeta } from '../types';

export const appMeta: AppMeta = { id: 'orchestrationgraph', title: 'Orchestration Graph', category: 'AI Agents' };

// ── Types ────────────────────────────────────────────────────────────────────

type StageStatus = 'idle' | 'active' | 'done' | 'error';

interface StageState {
  id: string;
  label: string;
  description: string;
  status: StageStatus;
}

// ── Stage definitions ────────────────────────────────────────────────────────

const INITIAL_STAGES: StageState[] = [
  { id: '0master',  label: '@0master',  description: 'Orchestrator',      status: 'idle' },
  { id: '10idea',   label: '@10idea',   description: 'Idea Curator',      status: 'idle' },
  { id: '1project', label: '@1project', description: 'Project Manager',   status: 'idle' },
  { id: '2think',   label: '@2think',   description: 'Options Explorer',  status: 'idle' },
  { id: '3design',  label: '@3design',  description: 'Architect',         status: 'idle' },
  { id: '4plan',    label: '@4plan',    description: 'Planner (TDD)',      status: 'idle' },
  { id: '5test',    label: '@5test',    description: 'QA / Red Phase',     status: 'idle' },
  { id: '6code',    label: '@6code',    description: 'Developer',          status: 'idle' },
  { id: '7exec',    label: '@7exec',    description: 'Runtime Validator',  status: 'idle' },
  { id: '8ql',      label: '@8ql',      description: 'Security Scanner',   status: 'idle' },
  { id: '9git',     label: '@9git',     description: 'Git / GitHub',       status: 'idle' },
];

const POLL_INTERVAL_MS = 3_000;
const PRJ_RE = /prj\d{7}/;

// ── Helpers ──────────────────────────────────────────────────────────────────

function inferStatus(content: string): StageStatus {
  if (!content || content.trim() === '') return 'idle';
  const lower = content.toLowerCase();
  if (lower.includes('error') || lower.includes('❌') || lower.includes('failed')) return 'error';
  if (lower.includes('done') || lower.includes('✅')) return 'done';
  if (lower.includes('active') || lower.includes('in progress')) return 'active';
  // Non-empty log with content likely means something ran
  if (content.trim().length > 0) return 'done';
  return 'idle';
}

function extractProjectId(content: string): string | null {
  const match = PRJ_RE.exec(content);
  return match ? match[0] : null;
}

// ── Stage box colors ─────────────────────────────────────────────────────────

function stageColors(status: StageStatus): { border: string; bg: string; text: string; dot: string } {
  switch (status) {
    case 'done':
      return { border: '#22c55e', bg: 'rgba(34,197,94,0.08)', text: '#86efac', dot: '#22c55e' };
    case 'active':
      return { border: '#3b82f6', bg: 'rgba(59,130,246,0.08)', text: '#93c5fd', dot: '#3b82f6' };
    case 'error':
      return { border: '#ef4444', bg: 'rgba(239,68,68,0.08)', text: '#fca5a5', dot: '#ef4444' };
    default:
      return { border: '#374151', bg: 'rgba(55,65,81,0.3)', text: '#6b7280', dot: '#4b5563' };
  }
}

// ── Component ────────────────────────────────────────────────────────────────

export function OrchestrationGraph() {
  const [stages, setStages] = useState<StageState[]>(INITIAL_STAGES);
  const [projectId, setProjectId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);

  const fetchAll = useCallback(async () => {
    try {
      const results = await Promise.allSettled(
        INITIAL_STAGES.map(s =>
          fetch(`/api/agent-log/${s.id}`).then(r => {
            if (!r.ok) return { content: '' };
            return r.json() as Promise<{ content: string }>;
          })
        )
      );

      let foundProjectId: string | null = null;
      const updated: StageState[] = INITIAL_STAGES.map((stage, i) => {
        const result = results[i];
        if (result.status === 'fulfilled') {
          const content = result.value?.content ?? '';
          if (!foundProjectId) {
            foundProjectId = extractProjectId(content);
          }
          return { ...stage, status: inferStatus(content) };
        }
        return { ...stage, status: 'error' };
      });

      setStages(updated);
      if (foundProjectId) setProjectId(foundProjectId);
      setFetchError(null);
    } catch (err) {
      setFetchError(err instanceof Error ? err.message : 'Fetch failed');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAll();
    const timer = setInterval(fetchAll, POLL_INTERVAL_MS);
    return () => clearInterval(timer);
  }, [fetchAll]);

  const doneCount = stages.filter(s => s.status === 'done').length;
  const progressPct = Math.round((doneCount / stages.length) * 100);

  return (
    <div style={{
      display: 'flex', flexDirection: 'column', height: '100%',
      background: '#0d1117', color: '#e6edf3', fontFamily: 'monospace',
      fontSize: '13px', overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: '10px',
        padding: '12px 16px', borderBottom: '1px solid #21262d',
        background: '#161b22', flexShrink: 0,
      }}>
        <span style={{ fontSize: '18px' }}>🕸️</span>
        <span style={{ fontWeight: 700, fontSize: '14px', color: '#e6edf3' }}>
          Agent Pipeline
        </span>
        {projectId && (
          <span style={{
            marginLeft: 'auto', background: '#1f6feb', color: '#e6edf3',
            borderRadius: '4px', padding: '2px 8px', fontSize: '11px', fontWeight: 600,
          }}>
            {projectId}
          </span>
        )}
        {loading && (
          <span style={{ marginLeft: projectId ? '8px' : 'auto', color: '#6b7280', fontSize: '11px' }}>
            Loading…
          </span>
        )}
      </div>

      {/* Error banner */}
      {fetchError && (
        <div style={{
          background: 'rgba(239,68,68,0.1)', border: '1px solid #ef4444',
          borderRadius: '4px', margin: '8px 16px', padding: '6px 10px',
          color: '#fca5a5', fontSize: '11px',
        }}>
          ⚠ {fetchError}
        </div>
      )}

      {/* Progress bar */}
      <div style={{ padding: '10px 16px 6px', flexShrink: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
          <span style={{ color: '#6b7280', fontSize: '11px' }}>Progress</span>
          <span style={{ color: '#22c55e', fontSize: '11px', fontWeight: 600 }}>
            {doneCount}/{stages.length} done ({progressPct}%)
          </span>
        </div>
        <div style={{ height: '6px', background: '#21262d', borderRadius: '3px', overflow: 'hidden' }}>
          <div style={{
            height: '100%', width: `${progressPct}%`,
            background: doneCount === stages.length ? '#22c55e' : '#3b82f6',
            borderRadius: '3px', transition: 'width 0.4s ease',
          }} />
        </div>
      </div>

      {/* Pipeline: horizontal scrollable */}
      <div style={{
        flex: 1, overflowX: 'auto', overflowY: 'hidden',
        padding: '10px 16px 16px', display: 'flex', alignItems: 'flex-start',
      }}>
        <div style={{ display: 'flex', gap: '6px', alignItems: 'stretch', minWidth: 'max-content' }}>
          {stages.map((stage, index) => {
            const colors = stageColors(stage.status);
            return (
              <React.Fragment key={stage.id}>
                {/* Stage box */}
                <div style={{
                  border: `1px solid ${colors.border}`,
                  background: colors.bg,
                  borderRadius: '6px',
                  padding: '10px 12px',
                  width: '110px',
                  minHeight: '90px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px',
                  transition: 'border-color 0.3s, background 0.3s',
                }}>
                  <div style={{ fontWeight: 700, color: colors.text, fontSize: '12px' }}>
                    {stage.label}
                  </div>
                  <div style={{ color: '#6b7280', fontSize: '10px', lineHeight: '1.3' }}>
                    {stage.description}
                  </div>
                  <div style={{ marginTop: 'auto', display: 'flex', alignItems: 'center', gap: '5px' }}>
                    <span style={{
                      width: '7px', height: '7px', borderRadius: '50%',
                      background: colors.dot, flexShrink: 0,
                      boxShadow: stage.status === 'active' ? `0 0 6px ${colors.dot}` : 'none',
                    }} />
                    <span style={{ color: colors.text, fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                      {stage.status}
                    </span>
                  </div>
                </div>

                {/* Connector arrow (not after last) */}
                {index < stages.length - 1 && (
                  <div style={{
                    display: 'flex', alignItems: 'center',
                    color: '#374151', fontSize: '16px', flexShrink: 0,
                  }}>
                    →
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>

      {/* Legend */}
      <div style={{
        display: 'flex', gap: '16px', padding: '8px 16px',
        borderTop: '1px solid #21262d', background: '#161b22',
        flexShrink: 0,
      }}>
        {(['idle', 'active', 'done', 'error'] as StageStatus[]).map(s => {
          const c = stageColors(s);
          return (
            <div key={s} style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: c.dot, flexShrink: 0 }} />
              <span style={{ color: '#6b7280', fontSize: '10px', textTransform: 'capitalize' }}>{s}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
