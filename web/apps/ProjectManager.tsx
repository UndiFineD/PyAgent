/**
 * ProjectManager — NebulaOS editable Kanban board for all PyAgent projects.
 *
 * Data source : GET  /api/projects           (read all)
 *               PATCH /api/projects/:id       (update fields / lane)
 *               POST  /api/projects           (create new)
 *
 * Features:
 *  • Drag-and-drop lane transitions
 *  • Double-click card → full edit modal
 *  • "New project" button
 *  • Project folder path shown on every card (docs/project/prjNNNNNNN/)
 */
import React, { useState, useEffect, useRef } from 'react';
import {
  GitBranch, ExternalLink, Search, Loader2, AlertTriangle,
  ChevronDown, ChevronUp, Tag, Pencil, FolderOpen, Plus, X, Check, BarChart2, Copy,
} from 'lucide-react';
import { cn } from '../utils';
import kanbanJson from '../../docs/project/kanban.json';
import nextProjectRaw from '../../data/nextproject.md?raw';
import type { AppMeta } from '../types';

const importedIdeaMarkdownFiles = import.meta.glob('../../docs/project/ideas/idea*.md', {
  eager: true,
  query: '?raw',
  import: 'default',
}) as Record<string, string>;

export const appMeta: AppMeta = { id: 'projectmanager', title: 'Project Manager', category: 'AI Agents' };

// ── Types ────────────────────────────────────────────────────────────────────

type Lane = 'Ideas' | 'Discovery' | 'Design' | 'In Sprint' | 'Review' | 'Released' | 'Archived';
type Priority = 'P1' | 'P2' | 'P3' | 'P4';
type BudgetTier = 'XS' | 'S' | 'M' | 'L' | 'XL' | 'unknown';

interface Project {
  id: string;
  name: string;
  lane: Lane;
  summary: string;
  branch: string | null;
  pr: number | null;
  priority: Priority;
  budget_tier: BudgetTier;
  tags: string[];
  created: string | null;
  updated: string | null;
}

interface Idea {
  idea_id: string;
  rank: number | null;
  title: string;
  summary: string;
  source_path: string;
  mapped_project_ids: string[];
}

type InsightMode = 'swot' | 'risk';

interface AgentFlowInboxItem {
  agentId: '0master';
  text: string;
  createdAt: string;
}

// ── Constants ────────────────────────────────────────────────────────────────

const LANES: Lane[] = ['Ideas', 'Discovery', 'Design', 'In Sprint', 'Review', 'Released', 'Archived'];
const FLOW_LANES: Lane[] = ['Discovery', 'Design', 'In Sprint'];
const BOARD_LANES: Lane[] = ['Review', 'Released', 'Archived'];
const PRIORITIES: Priority[] = ['P1', 'P2', 'P3', 'P4'];
const BUDGET_TIERS: BudgetTier[] = ['XS', 'S', 'M', 'L', 'XL', 'unknown'];

const LANE_COLORS: Record<Lane, string> = {
  'Ideas':     '#3b82f6',
  'Discovery': '#8b5cf6',
  'Design':    '#6366f1',
  'In Sprint': '#fbbf24',
  'Review':    '#fb923c',
  'Released':  '#10b981',
  'Archived':  '#6b7280',
};

const PRIORITY_COLORS: Record<Priority, string> = {
  P1: '#ef4444',
  P2: '#fb923c',
  P3: '#60a5fa',
  P4: '#9ca3af',
};

const GITHUB_PR_BASE = 'https://github.com/UndiFineD/PyAgent/pull';
const GITHUB_DIR_BASE = 'https://github.com/UndiFineD/PyAgent/tree/main/docs/project';
const TODAY = new Date().toISOString().slice(0, 10);
const API_FALLBACK_BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.replace(/\/$/, '') ?? 'http://127.0.0.1:444';

function toFallbackUrl(path: string): string {
  const normalized = path.startsWith('/') ? path : `/${path}`;
  return `${API_FALLBACK_BASE}${normalized}`;
}

async function fetchApi(path: string, init?: RequestInit): Promise<Response> {
  const primary = await fetch(path, init).catch(() => null);
  if (primary?.ok) return primary;

  // In some local setups (e.g., static serving without Vite proxy), /api routes can fail
  // with 404 (no route) or 502/503/504 (proxy target down) before fallback is needed.
  const shouldTryFallback = primary === null || [404, 502, 503, 504].includes(primary.status);
  if (!shouldTryFallback) return primary;

  return fetch(toFallbackUrl(path), init);
}

// ── API helpers ───────────────────────────────────────────────────────────────

async function apiPatch(id: string, patch: Partial<Project>): Promise<Project> {
  const r = await fetchApi(`/api/projects/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...patch, updated: TODAY }),
  });
  if (!r.ok) throw new Error(`PATCH ${id}: HTTP ${r.status}`);
  return r.json();
}

async function apiCreate(project: Project): Promise<Project> {
  const r = await fetchApi('/api/projects', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(project),
  });
  if (!r.ok) throw new Error(`POST: HTTP ${r.status}`);
  return r.json();
}

async function apiPatchIdea(
  ideaId: string,
  patch: { title?: string; summary?: string; mapped_project_ids?: string[]; ensure_swot_risk_data?: boolean },
): Promise<Idea> {
  const r = await fetchApi(`/api/ideas/${ideaId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(patch),
  });
  if (!r.ok) throw new Error(`PATCH idea ${ideaId}: HTTP ${r.status}`);
  return r.json();
}

async function apiRunPipeline(task: string): Promise<{ pipeline_id: string; status: string }> {
  const r = await fetchApi('/api/pipeline/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task }),
  });
  if (!r.ok) throw new Error(`POST pipeline/run: HTTP ${r.status}`);
  return r.json();
}

async function appendAgentLog(agentId: string, linesToAppend: string[]): Promise<void> {
  const readResp = await fetchApi(`/api/agent-log/${agentId}`);
  const previous = readResp.ok ? ((await readResp.json()) as { content?: string }).content ?? '' : '';
  const next = [previous.trimEnd(), ...linesToAppend].filter(Boolean).join('\n');
  await fetchApi(`/api/agent-log/${agentId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: `${next}\n` }),
  });
}

function enqueueAgentflowInbox(item: AgentFlowInboxItem): void {
  const key = 'pyagent.agentflow.inbox';
  const raw = localStorage.getItem(key);
  let queue: AgentFlowInboxItem[] = [];
  if (raw) {
    try {
      queue = JSON.parse(raw) as AgentFlowInboxItem[];
    } catch {
      queue = [];
    }
  }
  queue.push(item);
  localStorage.setItem(key, JSON.stringify(queue));
}

interface IdeaEditModalProps {
  idea: Idea;
  onSave: (idea: Idea) => void;
  onClose: () => void;
}

const IdeaEditModal: React.FC<IdeaEditModalProps> = ({ idea, onSave, onClose }) => {
  const [title, setTitle] = useState(idea.title);
  const [summary, setSummary] = useState(idea.summary);
  const [mappedProjects, setMappedProjects] = useState(idea.mapped_project_ids.join(', '));
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const save = async () => {
    setSaving(true);
    setErr(null);
    try {
      const mapped = mappedProjects
        .split(',')
        .map(token => token.trim().toLowerCase())
        .filter(Boolean);
      const updated = await apiPatchIdea(idea.idea_id, {
        title: title.trim(),
        summary: summary.trim(),
        mapped_project_ids: mapped,
      });
      onSave(updated);
    } catch (e) {
      setErr(String((e as Error).message));
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="bg-os-window border border-os-border rounded-xl shadow-2xl w-[560px] max-h-[90vh] overflow-y-auto p-5">
        <div className="flex items-center justify-between mb-4">
          <span className="font-semibold text-sm text-os-text">Edit {idea.idea_id}</span>
          <button onClick={onClose} className="text-os-text/40 hover:text-os-text"><X size={14} /></button>
        </div>

        <div className="space-y-3">
          <div>
            <div className="text-[10px] text-os-text/50 mb-0.5">Title</div>
            <input
              className="w-full bg-os-bg border border-os-border rounded px-2 py-1 text-xs text-os-text outline-none focus:border-os-accent"
              value={title}
              onChange={e => setTitle(e.target.value)}
            />
          </div>

          <div>
            <div className="text-[10px] text-os-text/50 mb-0.5">Summary</div>
            <textarea
              className="w-full h-20 bg-os-bg border border-os-border rounded px-2 py-1 text-xs text-os-text outline-none focus:border-os-accent resize-none"
              value={summary}
              onChange={e => setSummary(e.target.value)}
            />
          </div>

          <div>
            <div className="text-[10px] text-os-text/50 mb-0.5">Mapped projects (comma-separated)</div>
            <input
              className="w-full bg-os-bg border border-os-border rounded px-2 py-1 text-xs text-os-text outline-none focus:border-os-accent font-mono"
              value={mappedProjects}
              onChange={e => setMappedProjects(e.target.value)}
              placeholder="prj0000001, prj0000002"
            />
          </div>
        </div>

        {err && <div className="mt-3 text-[10px] text-red-400 font-mono">{err}</div>}

        <div className="flex justify-end gap-2 mt-4">
          <button onClick={onClose} className="text-xs px-3 py-1.5 border border-os-border rounded text-os-text/60 hover:text-os-text">
            Cancel
          </button>
          <button
            onClick={save}
            disabled={saving}
            className="text-xs px-3 py-1.5 bg-os-accent text-black rounded font-semibold hover:opacity-90 disabled:opacity-50 flex items-center gap-1"
          >
            {saving ? <Loader2 size={11} className="animate-spin" /> : <Check size={11} />}
            Save Idea
          </button>
        </div>
      </div>
    </div>
  );
};

// ── EditModal ─────────────────────────────────────────────────────────────────

interface EditModalProps {
  project: Project | null;   // null = create-new mode
  onSave: (p: Project) => void;
  onClose: () => void;
}

const NEXT_PROJECT_ID = nextProjectRaw.trim();

function blankProject(): Project {
  return {
    id: NEXT_PROJECT_ID,
    name: '',
    lane: 'Ideas',
    summary: '',
    branch: null,
    pr: null,
    priority: 'P4',
    budget_tier: 'unknown',
    tags: [],
    created: TODAY,
    updated: TODAY,
  };
}

const EditModal: React.FC<EditModalProps> = ({ project, onSave, onClose }) => {
  const isNew = project === null;
  const [form, setForm] = useState<Project>(project ?? blankProject());
  const [tagInput, setTagInput] = useState('');
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const set = <K extends keyof Project>(key: K, val: Project[K]) =>
    setForm(f => ({ ...f, [key]: val }));

  const addTag = () => {
    const t = tagInput.trim().toLowerCase();
    if (t && !form.tags.includes(t)) setForm(f => ({ ...f, tags: [...f.tags, t] }));
    setTagInput('');
  };

  const removeTag = (t: string) => setForm(f => ({ ...f, tags: f.tags.filter(x => x !== t) }));

  const handleSave = async () => {
    setSaving(true);
    setErr(null);
    try {
      let saved: Project;
      if (isNew) {
        saved = await apiCreate(form);
      } else {
        saved = await apiPatch(form.id, form);
      }
      onSave(saved);
    } catch (e) {
      setErr(String((e as Error).message));
      setSaving(false);
    }
  };

  const inputCls = 'w-full bg-os-bg border border-os-border rounded px-2 py-1 text-xs text-os-text outline-none focus:border-os-accent';
  const labelCls = 'text-[10px] text-os-text/50 mb-0.5';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="bg-os-window border border-os-border rounded-xl shadow-2xl w-[520px] max-h-[90vh] overflow-y-auto p-5">
        <div className="flex items-center justify-between mb-4">
          <span className="font-semibold text-sm text-os-text">{isNew ? 'New Project' : `Edit ${form.id}`}</span>
          <button onClick={onClose} className="text-os-text/40 hover:text-os-text"><X size={14} /></button>
        </div>

        <div className="grid grid-cols-2 gap-3">
          {isNew && (
            <div className="col-span-2">
              <div className={labelCls}>ID (prjNNNNNNN)</div>
              <input className={inputCls} value={form.id} onChange={e => set('id', e.target.value)} placeholder="prjNNNNNNN" />
            </div>
          )}

          <div className="col-span-2">
            <div className={labelCls}>Name</div>
            <input className={inputCls} value={form.name} onChange={e => set('name', e.target.value)} />
          </div>

          <div className="col-span-2">
            <div className={labelCls}>Summary</div>
            <textarea
              className={cn(inputCls, 'resize-none h-16')}
              value={form.summary}
              onChange={e => set('summary', e.target.value)}
            />
          </div>

          <div>
            <div className={labelCls}>Lane</div>
            <select className={inputCls} value={form.lane} onChange={e => set('lane', e.target.value as Lane)}>
              {LANES.map(l => <option key={l}>{l}</option>)}
            </select>
          </div>

          <div>
            <div className={labelCls}>Priority</div>
            <select className={inputCls} value={form.priority} onChange={e => set('priority', e.target.value as Priority)}>
              {PRIORITIES.map(p => <option key={p}>{p}</option>)}
            </select>
          </div>

          <div>
            <div className={labelCls}>Budget tier</div>
            <select className={inputCls} value={form.budget_tier} onChange={e => set('budget_tier', e.target.value as BudgetTier)}>
              {BUDGET_TIERS.map(b => <option key={b}>{b}</option>)}
            </select>
          </div>

          <div>
            <div className={labelCls}>PR #</div>
            <input
              className={inputCls}
              type="number"
              value={form.pr ?? ''}
              onChange={e => set('pr', e.target.value ? Number(e.target.value) : null)}
            />
          </div>

          <div className="col-span-2">
            <div className={labelCls}>Branch</div>
            <input className={inputCls} value={form.branch ?? ''} onChange={e => set('branch', e.target.value || null)} />
          </div>

          <div className="col-span-2">
            <div className={labelCls}>Tags (press Enter to add)</div>
            <div className="flex gap-1 flex-wrap mb-1">
              {form.tags.map(t => (
                <span key={t} className="flex items-center gap-1 text-[10px] bg-os-bg border border-os-border rounded px-1.5 py-0.5 text-os-text/60">
                  {t}
                  <button onClick={() => removeTag(t)} className="text-os-text/30 hover:text-os-text"><X size={9} /></button>
                </span>
              ))}
            </div>
            <input
              className={inputCls}
              value={tagInput}
              onChange={e => setTagInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addTag(); } }}
              placeholder="e.g. security"
            />
          </div>
        </div>

        {err && <div className="mt-3 text-[10px] text-red-400 font-mono">{err}</div>}

        <div className="flex justify-end gap-2 mt-4">
          <button onClick={onClose} className="text-xs px-3 py-1.5 border border-os-border rounded text-os-text/60 hover:text-os-text">
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="text-xs px-3 py-1.5 bg-os-accent text-black rounded font-semibold hover:opacity-90 disabled:opacity-50 flex items-center gap-1"
          >
            {saving ? <Loader2 size={11} className="animate-spin" /> : <Check size={11} />}
            {isNew ? 'Create' : 'Save'}
          </button>
        </div>
      </div>
    </div>
  );
};

// ── ProjectCard ──────────────────────────────────────────────────────────────

interface ProjectCardProps {
  project: Project;
  onEdit: (p: Project) => void;
  onDragStart: (id: string) => void;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project, onEdit, onDragStart }) => {
  const [expanded, setExpanded] = useState(false);
  const laneColor = LANE_COLORS[project.lane];
  const priorityColor = PRIORITY_COLORS[project.priority];
  const folderPath = `docs/project/${project.id}`;

  return (
    <div
      draggable
      role="button"
      tabIndex={0}
      aria-expanded={expanded}
      onDragStart={e => { e.dataTransfer.effectAllowed = 'move'; onDragStart(project.id); }}
      onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setExpanded(v => !v); } }}
      className="bg-os-window border border-os-border rounded-lg p-3 mb-2 cursor-grab active:cursor-grabbing hover:border-os-accent/50 transition-colors group focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-os-accent"
      onClick={() => setExpanded(e => !e)}
    >
      <div className="flex items-center gap-2 mb-2 flex-wrap">
        <span
          className="text-[10px] font-semibold px-2 py-0.5 rounded-full text-black"
          style={{ backgroundColor: laneColor }}
        >
          {project.lane}
        </span>
        <span className="font-mono text-[10px] text-os-text/50 bg-os-bg border border-os-border rounded px-1.5 py-0.5">
          {project.id}
        </span>
        <span
          className="ml-auto text-[10px] font-bold px-1.5 py-0.5 rounded"
          style={{ color: priorityColor, borderColor: priorityColor, border: `1px solid ${priorityColor}` }}
        >
          {project.priority}
        </span>
        <span className="text-[10px] text-os-text/50 bg-os-bg border border-os-border rounded px-1.5 py-0.5">
          {project.budget_tier}
        </span>
        {/* Edit button — visible on hover */}
        <button
          onClick={e => { e.stopPropagation(); onEdit(project); }}
          className="opacity-0 group-hover:opacity-70 hover:!opacity-100 text-os-text/50 hover:text-os-accent transition-opacity ml-1"
          title="Edit project"
        >
          <Pencil size={11} />
        </button>
      </div>

      <div className="font-semibold text-sm text-os-text mb-1 leading-tight">
        {project.name}
      </div>

      {/* Project folder path — always visible */}
      <div className="flex items-center gap-1 mb-1">
        <FolderOpen size={10} className="text-os-text/30 shrink-0" />
        <a
          href={`${GITHUB_DIR_BASE}/${project.id}`}
          target="_blank"
          rel="noopener noreferrer"
          className="font-mono text-[9px] text-os-accent/60 hover:text-os-accent hover:underline truncate"
          onClick={e => e.stopPropagation()}
          title={folderPath}
        >
          {folderPath}
        </a>
      </div>

      <div className={cn('text-xs text-os-text/60 leading-relaxed', !expanded && 'line-clamp-2')}>
        {project.summary}
      </div>

      {expanded && (
        <div className="mt-3 space-y-2 border-t border-os-border pt-2">
          {project.branch && project.branch !== 'merged' && (
            <div className="flex items-center gap-1.5 text-xs text-os-text/70">
              <GitBranch size={12} className="shrink-0" />
              <span className="font-mono truncate">{project.branch}</span>
            </div>
          )}
          {project.branch === 'merged' && (
            <div className="flex items-center gap-1.5 text-xs text-emerald-400">
              <GitBranch size={12} className="shrink-0" />
              <span className="font-mono">merged</span>
            </div>
          )}
          {project.pr !== null && (
            <div className="flex items-center gap-1.5 text-xs">
              <ExternalLink size={12} className="shrink-0 text-os-text/50" />
              <a
                href={`${GITHUB_PR_BASE}/${project.pr}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-os-accent hover:underline"
                onClick={e => e.stopPropagation()}
              >
                PR #{project.pr}
              </a>
            </div>
          )}
          {project.tags.length > 0 && (
            <div className="flex items-center gap-1 flex-wrap">
              <Tag size={11} className="text-os-text/40 shrink-0" />
              {project.tags.map(tag => (
                <span key={tag} className="text-[10px] bg-os-bg border border-os-border rounded px-1.5 py-0.5 text-os-text/60">
                  {tag}
                </span>
              ))}
            </div>
          )}
          <div className="text-[10px] text-os-text/40 font-mono">
            created: {project.created} · updated: {project.updated}
          </div>
        </div>
      )}

      <div className="flex justify-center mt-1">
        {expanded
          ? <ChevronUp size={12} className="text-os-text/30" />
          : <ChevronDown size={12} className="text-os-text/30" />
        }
      </div>
    </div>
  );
};

// ── LaneColumn ───────────────────────────────────────────────────────────────

interface LaneColumnProps {
  lane: Lane;
  projects: Project[];
  onEdit: (p: Project) => void;
  onDragStart: (id: string) => void;
  onDrop: (lane: Lane) => void;
}

const LaneColumn: React.FC<LaneColumnProps> = ({ lane, projects, onEdit, onDragStart, onDrop }) => {
  const [over, setOver] = useState(false);
  const color = LANE_COLORS[lane];

  return (
    <div
      className={cn(
        'min-w-[240px] w-64 flex flex-col shrink-0 rounded-lg transition-colors',
        over && 'ring-2 ring-os-accent/60 bg-os-accent/5',
      )}
      onDragOver={e => { e.preventDefault(); setOver(true); }}
      onDragLeave={() => setOver(false)}
      onDrop={e => { e.preventDefault(); setOver(false); onDrop(lane); }}
    >
      <div
        className="flex items-center justify-between px-3 py-2 rounded-t-lg mb-2 text-black"
        style={{ backgroundColor: color }}
      >
        <span className="text-xs font-bold uppercase tracking-wide">{lane}</span>
        <span className="text-xs font-mono bg-black/20 rounded-full px-2 py-0.5">{projects.length}</span>
      </div>
      <div className="flex-1 overflow-y-auto min-h-[60px] max-h-[calc(100vh-240px)]">
        {projects.length === 0
          ? (
            <div className={cn(
              'text-[10px] text-os-text/30 text-center py-6 italic border-2 border-dashed rounded-lg mx-1',
              over ? 'border-os-accent/40' : 'border-os-border/30'
            )}>
              drop here
            </div>
          )
          : projects.map(p => (
            <ProjectCard key={p.id} project={p} onEdit={onEdit} onDragStart={onDragStart} />
          ))
        }
      </div>
    </div>
  );
};

interface FlowColumnProps {
  projectsByLane: Record<Lane, Project[]>;
  onEdit: (p: Project) => void;
  onDragStart: (id: string) => void;
  onDrop: (lane: Lane) => void;
}

const FlowColumn: React.FC<FlowColumnProps> = ({ projectsByLane, onEdit, onDragStart, onDrop }) => {
  const [over, setOver] = useState(false);
  const total = FLOW_LANES.reduce((sum, lane) => sum + projectsByLane[lane].length, 0);

  return (
    <div
      className={cn(
        'min-w-[280px] w-72 flex flex-col shrink-0 rounded-lg transition-colors',
        over && 'ring-2 ring-os-accent/60 bg-os-accent/5',
      )}
      onDragOver={e => { e.preventDefault(); setOver(true); }}
      onDragLeave={() => setOver(false)}
      onDrop={e => {
        e.preventDefault();
        setOver(false);
        // Dropping on the combined flow moves work to the first lane in the sequence.
        onDrop('Discovery');
      }}
    >
      <div
        className="flex items-center justify-between px-3 py-2 rounded-t-lg mb-2 text-black"
        style={{ backgroundColor: '#a78bfa' }}
      >
        <span className="text-xs font-bold uppercase tracking-wide">Flow (Discovery to Design to In Sprint)</span>
        <span className="text-xs font-mono bg-black/20 rounded-full px-2 py-0.5">{total}</span>
      </div>
      <div className="flex-1 overflow-y-auto min-h-[60px] max-h-[calc(100vh-240px)] px-2 pb-2 space-y-2">
        {total === 0 && (
          <div className={cn(
            'text-[10px] text-os-text/30 text-center py-6 italic border-2 border-dashed rounded-lg',
            over ? 'border-os-accent/40' : 'border-os-border/30'
          )}>
            drop here
          </div>
        )}

        {FLOW_LANES.map(lane => (
          <div key={lane} className="border border-os-border/60 rounded-md bg-os-bg/25">
            <div
              className="flex items-center justify-between px-2 py-1 text-[10px] font-semibold uppercase tracking-wide text-black rounded-t-md"
              style={{ backgroundColor: LANE_COLORS[lane] }}
            >
              <span>{lane}</span>
              <span className="font-mono bg-black/20 rounded-full px-1.5 py-0.5">{projectsByLane[lane].length}</span>
            </div>
            <div className="p-1">
              {projectsByLane[lane].length === 0
                ? <div className="text-[10px] text-os-text/30 italic text-center py-2">empty</div>
                : projectsByLane[lane].map(p => (
                  <ProjectCard key={p.id} project={p} onEdit={onEdit} onDragStart={onDragStart} />
                ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

interface IdeasColumnProps {
  ideas: Idea[];
  ideasLoading: boolean;
  ideasError: string | null;
  promotingIdeaId: string | null;
  onDragStartIdea: (ideaId: string) => void;
  onEditIdea: (idea: Idea) => void;
  onOpenInsightForIdea: (mode: InsightMode, ideaId: string) => void;
  onPromoteIdea: (idea: Idea) => void;
}

const IdeasColumn: React.FC<IdeasColumnProps> = ({
  ideas,
  ideasLoading,
  ideasError,
  promotingIdeaId,
  onDragStartIdea,
  onEditIdea,
  onOpenInsightForIdea,
  onPromoteIdea,
}) => (
  <div className="min-w-[240px] w-64 flex flex-col shrink-0 rounded-lg transition-colors">
    <div
      className="flex items-center justify-between px-3 py-2 rounded-t-lg mb-2 text-black"
      style={{ backgroundColor: LANE_COLORS.Ideas }}
    >
      <span className="text-xs font-bold uppercase tracking-wide">Active Ideas Queue</span>
      <span className="text-xs font-mono bg-black/20 rounded-full px-2 py-0.5">{ideas.length} ideas</span>
    </div>
    <div className="flex-1 overflow-y-auto min-h-[60px] max-h-[calc(100vh-240px)] p-2 space-y-2">
      {ideasLoading && (
        <div className="flex items-center gap-1.5 text-xs text-os-text/60 px-1 py-2">
          <Loader2 size={12} className="animate-spin text-os-accent" />
          <span>Loading ideas…</span>
        </div>
      )}
      {!ideasLoading && ideasError && (
        <div className="text-[10px] rounded border border-amber-400/40 bg-amber-500/10 text-amber-200 px-2 py-1.5">
          Ideas unavailable: {ideasError}
        </div>
      )}
      {!ideasLoading && !ideasError && ideas.length === 0 && (
        <div className={cn(
          'text-[10px] text-os-text/30 text-center py-6 italic border-2 border-dashed rounded-lg mx-1',
          'border-os-border/30'
        )}>
          no active ideas
        </div>
      )}
      {!ideasLoading && !ideasError && ideas.map(idea => (
        <div
          key={idea.idea_id}
          draggable
          onDragStart={e => {
            e.dataTransfer.effectAllowed = 'move';
            onDragStartIdea(idea.idea_id);
          }}
          className="border border-os-border rounded-md px-2 py-1.5 bg-os-bg/40 cursor-grab active:cursor-grabbing"
        >
          <div className="flex items-center gap-1.5 mb-1">
            <span className="text-[10px] font-mono text-os-text/50 bg-os-window border border-os-border rounded px-1">
              #{idea.rank ?? '-'}
            </span>
            <span className="text-xs font-semibold leading-tight text-os-text truncate" title={idea.title}>
              {idea.title}
            </span>
          </div>
          <div className="text-[10px] font-mono text-os-text/45 mb-1.5">{idea.idea_id}</div>
          <div className="text-[10px] text-os-text/60 mb-1.5 line-clamp-2">{idea.summary}</div>
          <div className="text-[10px] text-os-text/50 font-mono truncate" title={idea.source_path}>
            {idea.source_path}
          </div>
          {idea.mapped_project_ids.length > 0 && (
            <div className="mt-1.5 flex flex-wrap gap-1">
              {idea.mapped_project_ids.slice(0, 3).map(projectId => (
                <span
                  key={projectId}
                  className="text-[10px] font-mono px-1 py-0.5 rounded border border-os-border bg-os-window text-os-text/55"
                >
                  {projectId}
                </span>
              ))}
            </div>
          )}
          <div className="mt-2.5 grid grid-cols-2 gap-1.5">
            <button
              onClick={() => onEditIdea(idea)}
              className="text-[10px] px-1.5 py-1 rounded border border-os-border text-os-text/70 hover:text-os-text hover:border-os-accent"
            >
              Edit
            </button>
            <button
              onClick={() => onOpenInsightForIdea('swot', idea.idea_id)}
              className="text-[10px] px-1.5 py-1 rounded border border-blue-400/60 text-blue-200 hover:bg-blue-500/15"
            >
              SWOT
            </button>
            <button
              onClick={() => onOpenInsightForIdea('risk', idea.idea_id)}
              className="text-[10px] px-1.5 py-1 rounded border border-yellow-400/60 text-yellow-200 hover:bg-yellow-500/15"
            >
              Risk
            </button>
            <button
              onClick={() => onPromoteIdea(idea)}
              disabled={promotingIdeaId === idea.idea_id}
              className="text-[10px] px-1.5 py-1 rounded border border-purple-400/70 text-purple-200 hover:bg-purple-500/15 disabled:opacity-50"
            >
              {promotingIdeaId === idea.idea_id ? 'Starting…' : 'To Discovery'}
            </button>
          </div>
        </div>
      ))}
    </div>
  </div>
);

// ── Helpers ──────────────────────────────────────────────────────────────────

interface RiskEntry {
  id: string;
  risk: string;
  likelihood: string;
  impact: string;
  status: string;
  mitigation: string;
}

interface SwotData {
  strengths: string[];
  weaknesses: string[];
  opportunities: string[];
  threats: string[];
}

interface KanbanEnvelope {
  projects?: Project[];
  swot?: {
    strengths?: string[];
    weaknesses?: string[];
    opportunities?: string[];
    threats?: string[];
  };
  risk_register?: RiskEntry[];
}

const importedKanbanJson: KanbanEnvelope = kanbanJson as KanbanEnvelope;

function getLocalProjectSnapshot(): Project[] {
  if (!Array.isArray(importedKanbanJson.projects)) return [];
  return importedKanbanJson.projects as Project[];
}

function parseRiskRegister(raw: unknown): RiskEntry[] {
  if (!Array.isArray(raw)) return [];

  return raw
    .filter(item => item && typeof item === 'object')
    .map(item => item as Partial<RiskEntry>)
    .map(item => ({
      id: String(item.id ?? ''),
      risk: String(item.risk ?? ''),
      likelihood: String(item.likelihood ?? ''),
      impact: String(item.impact ?? ''),
      status: String(item.status ?? ''),
      mitigation: String(item.mitigation ?? ''),
    }))
    .filter(item => item.id.length > 0 && item.risk.length > 0);
}

function parseSwot(raw: unknown): SwotData {
  const swot = (raw && typeof raw === 'object' ? raw as KanbanEnvelope['swot'] : undefined) ?? {};
  return {
    strengths: Array.isArray(swot.strengths) ? swot.strengths.map(String) : [],
    weaknesses: Array.isArray(swot.weaknesses) ? swot.weaknesses.map(String) : [],
    opportunities: Array.isArray(swot.opportunities) ? swot.opportunities.map(String) : [],
    threats: Array.isArray(swot.threats) ? swot.threats.map(String) : [],
  };
}

function toTitleCase(text: string): string {
  return text
    .split(' ')
    .filter(Boolean)
    .map(token => token.charAt(0).toUpperCase() + token.slice(1))
    .join(' ');
}

function buildSlugTitle(stem: string): string {
  const compactIdea = stem.match(/^(idea)(\d+)$/i);
  if (compactIdea) {
    return `Idea ${compactIdea[2]}`;
  }
  const readable = stem.replace(/[_-]+/g, ' ').trim();
  if (readable.length === 0) return 'Untitled Idea';
  return toTitleCase(readable);
}

function firstMeaningfulNonHeadingLine(lines: string[]): string | null {
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.length === 0) continue;
    if (/^#+\s+/.test(trimmed)) continue;
    if (/^```/.test(trimmed)) continue;
    return trimmed;
  }
  return null;
}

function extractIdeaSummary(lines: string[]): string {
  const summaryHeaderIndex = lines.findIndex(line => /^##\s+idea summary\b/i.test(line.trim()));
  if (summaryHeaderIndex >= 0) {
    const summaryLines: string[] = [];
    for (let i = summaryHeaderIndex + 1; i < lines.length; i += 1) {
      const current = lines[i].trim();
      if (/^##\s+/.test(current)) break;
      summaryLines.push(lines[i]);
    }
    const sectionSummary = firstMeaningfulNonHeadingLine(summaryLines);
    if (sectionSummary) return sectionSummary;
  }
  return firstMeaningfulNonHeadingLine(lines) ?? '';
}

function parseLocalIdeaFile(path: string, markdown: string): Idea | null {
  const filename = path.split('/').pop();
  if (!filename) return null;
  const stem = filename.replace(/\.md$/i, '');
  if (!/^idea\d+/i.test(stem)) return null;

  const ideaId = stem.toLowerCase();
  const rankMatch = stem.match(/idea(\d+)/i);
  const rank = rankMatch ? Number.parseInt(rankMatch[1], 10) : null;
  const lines = markdown.split(/\r?\n/);
  const headingLine = lines.find(line => /^#\s+/.test(line.trim()));
  const title = headingLine ? headingLine.replace(/^#\s+/, '').trim() : buildSlugTitle(stem);
  const summary = extractIdeaSummary(lines);

  const mappedProjectIds = Array.from(
    new Set(
      lines
        .filter(line => /planned project mapping\s*:/i.test(line))
        .flatMap(line => line.match(/prj\d{8}/gi) ?? [])
        .map(value => value.toLowerCase()),
    ),
  );

  return {
    idea_id: ideaId,
    rank,
    title,
    summary,
    source_path: `docs/project/ideas/${filename}`,
    mapped_project_ids: mappedProjectIds,
  };
}

function getLocalIdeasSnapshot(): Idea[] {
  return Object.entries(importedIdeaMarkdownFiles)
    .map(([path, markdown]) => parseLocalIdeaFile(path, markdown))
    .filter((idea): idea is Idea => idea !== null)
    .sort((a, b) => {
      const aRank = a.rank;
      const bRank = b.rank;
      if (aRank === null && bRank === null) return 0;
      if (aRank === null) return 1;
      if (bRank === null) return -1;
      return aRank - bRank;
    });
}

function normalizeSearchText(value: string): string {
  return value.toLowerCase().trim();
}

function isIdeasBackendUnavailable(message: string): boolean {
  const normalized = message.toLowerCase();
  return (
    normalized.includes('failed to fetch')
    || normalized.includes('networkerror')
    || normalized.includes('http 502')
    || normalized.includes('http 503')
    || normalized.includes('http 504')
  );
}

function matchesIdeaContext(text: string, idea: Idea): boolean {
  const haystack = normalizeSearchText(text);
  const ideaId = normalizeSearchText(idea.idea_id);
  const ideaTitle = normalizeSearchText(idea.title);
  return haystack.includes(ideaId) || (ideaTitle.length > 0 && haystack.includes(ideaTitle));
}

function getIdeaSwotContext(idea: Idea, swot: SwotData): SwotData {
  const pickBucket = (items: string[]): string[] => {
    const matched = items.filter(item => matchesIdeaContext(item, idea));
    if (matched.length > 0) return matched.slice(0, 2);
    return [];
  };

  return {
    strengths: pickBucket(swot.strengths),
    weaknesses: pickBucket(swot.weaknesses),
    opportunities: pickBucket(swot.opportunities),
    threats: pickBucket(swot.threats),
  };
}

function getIdeaRiskContext(idea: Idea, risks: RiskEntry[]): RiskEntry[] {
  const direct = risks.filter(entry => matchesIdeaContext(entry.risk, idea));
  return direct.slice(0, 2);
}

async function getLatestKanbanRegistersSource(): Promise<KanbanEnvelope> {
  const candidatePaths = [
    '/docs/project/kanban.json',
    '/api/docs/project/kanban.json',
  ];

  for (const path of candidatePaths) {
    try {
      const response = await fetchApi(path, {
        headers: { Accept: 'application/json' },
      });
      if (!response.ok) continue;
      const content = await response.json();
      if (content && typeof content === 'object') {
        return content as KanbanEnvelope;
      }
    } catch {
      // Ignore and continue trying additional sources.
    }
  }

  return importedKanbanJson;
}

function formatSwotContextMarkdown(swot: SwotData): string {
  const toLine = (items: string[]) => (items.length > 0 ? items.map(item => `- ${item}`).join('\n') : '- (none found)');
  return [
    'Strengths:',
    toLine(swot.strengths),
    'Weaknesses:',
    toLine(swot.weaknesses),
    'Opportunities:',
    toLine(swot.opportunities),
    'Threats:',
    toLine(swot.threats),
  ].join('\n');
}

function formatRiskContextMarkdown(risks: RiskEntry[]): string {
  if (risks.length === 0) return '- (none found)';
  return risks
    .map(risk => `- ${risk.id} | status=${risk.status} | L=${risk.likelihood} I=${risk.impact} | ${risk.risk} | mitigation: ${risk.mitigation}`)
    .join('\n');
}

function buildProjectDefinitionChecklistMarkdown(): string {
  return [
    '- [ ] Vision',
    '- [ ] Goals',
    '- [ ] Scope',
    '- [ ] Requirements',
    '- [ ] Resources',
    '- [ ] Timeline and milestones',
    '- [ ] Work breakdown structure (WBS)',
    '- [ ] Methodology and process',
    '- [ ] Execution plan',
    '- [ ] Risk management',
    '- [ ] Communication plan',
    '- [ ] Quality plan',
    '- [ ] Documentation plan',
    '- [ ] Delivery and deployment plan',
    '- [ ] Evaluation and closure',
    '- [ ] Failure, rollback, and lessons learned',
  ].join('\n');
}

async function copyTextToClipboard(text: string): Promise<void> {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }
  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.style.position = 'fixed';
  textArea.style.opacity = '0';
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand('copy');
  document.body.removeChild(textArea);
}

interface InsightsModalProps {
  mode: 'swot' | 'risk';
  ideas: Idea[];
  initialIdeaId?: string | null;
  onClose: () => void;
}

const InsightsModal: React.FC<InsightsModalProps> = ({ mode, ideas, initialIdeaId, onClose }) => {
  const risks = parseRiskRegister(importedKanbanJson.risk_register);
  const swot = parseSwot(importedKanbanJson.swot);
  const [selectedIdeaId, setSelectedIdeaId] = useState<string>(initialIdeaId ?? ideas[0]?.idea_id ?? '');
  const [copyNotice, setCopyNotice] = useState<string | null>(null);

  useEffect(() => {
    if (initialIdeaId) setSelectedIdeaId(initialIdeaId);
  }, [initialIdeaId]);

  const selectedIdea = ideas.find(i => i.idea_id === selectedIdeaId) ?? null;

  const setNotice = (message: string) => {
    setCopyNotice(message);
    window.setTimeout(() => setCopyNotice(null), 2200);
  };

  const copyWithNotice = async (text: string, message: string) => {
    await copyTextToClipboard(text);
    setNotice(message);
  };

  const likelihoodStyle = (value: string) => {
    if (value === 'H') return 'bg-red-500/20 text-red-200 border-red-400/50';
    if (value === 'M') return 'bg-amber-500/20 text-amber-200 border-amber-400/50';
    return 'bg-emerald-500/20 text-emerald-200 border-emerald-400/50';
  };

  const statusStyle = (value: string) => {
    if (value.toLowerCase() === 'open') return 'bg-red-500/20 text-red-200 border-red-400/50';
    return 'bg-emerald-500/20 text-emerald-200 border-emerald-400/50';
  };

  const swotQuadrants = [
    { key: 'strengths', title: 'Strengths', color: '#22c55e', items: swot.strengths },
    { key: 'weaknesses', title: 'Weaknesses', color: '#ef4444', items: swot.weaknesses },
    { key: 'opportunities', title: 'Opportunities', color: '#3b82f6', items: swot.opportunities },
    { key: 'threats', title: 'Threats', color: '#f59e0b', items: swot.threats },
  ] as const;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/65" onClick={onClose}>
      <div
        className="bg-gray-950 border border-gray-700 rounded-xl shadow-2xl max-w-6xl w-[96vw] max-h-[86vh] flex flex-col"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-4 py-3 border-b border-gray-700">
          <div>
            <h2 className="text-sm font-semibold text-white">
              {mode === 'swot' ? 'SWOT Workspace' : 'Risk Workspace'}
            </h2>
            <p className="text-[11px] text-gray-400">Visual view with quick copy templates from active ideas.</p>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-xs">Close</button>
        </div>

        <div className="px-4 py-3 border-b border-gray-800 grid grid-cols-1 md:grid-cols-4 gap-2">
          <div className="md:col-span-2">
            <label className="text-[10px] uppercase tracking-wide text-gray-400">Idea quick pick</label>
            <select
              className="mt-1 w-full bg-gray-900 border border-gray-700 rounded px-2 py-1.5 text-xs text-gray-100"
              value={selectedIdeaId}
              onChange={e => setSelectedIdeaId(e.target.value)}
            >
              <option value="">Select active idea...</option>
              {ideas.map(idea => (
                <option key={idea.idea_id} value={idea.idea_id}>{idea.idea_id} - {idea.title}</option>
              ))}
            </select>
          </div>
          <div className="md:col-span-2 flex items-end gap-2 flex-wrap">
            <button
              disabled={!selectedIdea}
              onClick={() => selectedIdea && copyWithNotice(
                `| | ${selectedIdea.title} (${selectedIdea.idea_id}) | |`,
                'Copied SWOT helpful-side row',
              )}
              className="text-[11px] px-2.5 py-1.5 rounded border border-blue-400/60 text-blue-200 hover:bg-blue-500/15 disabled:opacity-40 flex items-center gap-1"
            >
              <Copy size={12} /> Copy SWOT (Helpful)
            </button>
            <button
              disabled={!selectedIdea}
              onClick={() => selectedIdea && copyWithNotice(
                `| | | ${selectedIdea.title} (${selectedIdea.idea_id}) |`,
                'Copied SWOT harmful-side row',
              )}
              className="text-[11px] px-2.5 py-1.5 rounded border border-amber-400/60 text-amber-200 hover:bg-amber-500/15 disabled:opacity-40 flex items-center gap-1"
            >
              <Copy size={12} /> Copy SWOT (Harmful)
            </button>
            <button
              disabled={!selectedIdea}
              onClick={() => selectedIdea && copyWithNotice(
                `| RSK-NEW | ${selectedIdea.title} (${selectedIdea.idea_id}) | M | M | Open | Define mitigation and owner |`,
                'Copied risk row template',
              )}
              className="text-[11px] px-2.5 py-1.5 rounded border border-red-400/60 text-red-200 hover:bg-red-500/15 disabled:opacity-40 flex items-center gap-1"
            >
              <Copy size={12} /> Copy Risk Row
            </button>
          </div>
        </div>

        {copyNotice && (
          <div className="mx-4 mt-2 text-[11px] rounded border border-emerald-400/50 bg-emerald-500/10 text-emerald-200 px-2 py-1">
            {copyNotice}
          </div>
        )}

        <div className="flex-1 overflow-auto p-4">
          {mode === 'swot' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {swotQuadrants.map(quadrant => (
                <div key={quadrant.key} className="border border-gray-700 rounded-lg bg-gray-900/60">
                  <div className="px-3 py-2 border-b border-gray-700 flex items-center justify-between">
                    <span className="text-xs font-semibold" style={{ color: quadrant.color }}>{quadrant.title}</span>
                    <span className="text-[10px] font-mono text-gray-400">{quadrant.items.length}</span>
                  </div>
                  <div className="p-3 space-y-2">
                    {quadrant.items.length === 0 && <div className="text-[11px] text-gray-500 italic">No entries</div>}
                    {quadrant.items.map((item, idx) => (
                      <div key={`${quadrant.key}-${idx}`} className="text-xs text-gray-200 border border-gray-700 rounded px-2 py-1.5 bg-gray-950/70">
                        {item}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
              {risks.map(risk => (
                <div key={risk.id} className="border border-gray-700 rounded-lg bg-gray-900/60 p-3">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs font-mono text-gray-300">{risk.id}</span>
                    <span className={cn('text-[10px] px-2 py-0.5 rounded border', statusStyle(risk.status))}>{risk.status}</span>
                  </div>
                  <div className="text-xs text-gray-100 mb-2 leading-relaxed">{risk.risk}</div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className={cn('text-[10px] px-2 py-0.5 rounded border', likelihoodStyle(risk.likelihood))}>
                      Likelihood {risk.likelihood}
                    </span>
                    <span className={cn('text-[10px] px-2 py-0.5 rounded border', likelihoodStyle(risk.impact))}>
                      Impact {risk.impact}
                    </span>
                  </div>
                  <div className="text-[11px] text-gray-300 mb-2">{risk.mitigation}</div>
                  <button
                    onClick={() => copyWithNotice(
                      `| ${risk.id} | ${risk.risk} | ${risk.likelihood} | ${risk.impact} | ${risk.status} | ${risk.mitigation} |`,
                      `Copied ${risk.id}`,
                    )}
                    className="text-[11px] px-2 py-1 rounded border border-gray-600 text-gray-200 hover:bg-gray-800 inline-flex items-center gap-1"
                  >
                    <Copy size={11} /> Copy row
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ── FilterBar ────────────────────────────────────────────────────────────────

interface FilterBarProps {
  selectedLane: Lane | null;
  onLaneChange: (lane: Lane | null) => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  onNew: () => void;
  onSwot: () => void;
  onRisk: () => void;
}

const FilterBar: React.FC<FilterBarProps> = ({
  selectedLane, onLaneChange, searchQuery, onSearchChange, onNew, onSwot, onRisk,
}) => (
  <div className="flex items-center gap-3 px-3 py-2 bg-os-window border-b border-os-border flex-wrap">
    <div className="flex items-center gap-1 flex-wrap">
      <button
        onClick={() => onLaneChange(null)}
        className={cn(
          'text-[10px] px-2 py-1 rounded border transition-opacity',
          selectedLane === null ? 'opacity-100 bg-os-accent/20 border-os-accent' : 'opacity-40 hover:opacity-70 border-os-border'
        )}
      >
        All
      </button>
      {LANES.map(lane => (
        <button
          key={lane}
          onClick={() => onLaneChange(lane)}
          className={cn(
            'text-[10px] px-2 py-1 rounded border text-black transition-opacity',
            selectedLane === lane ? 'opacity-100' : 'opacity-40 hover:opacity-70'
          )}
          style={{ backgroundColor: LANE_COLORS[lane], borderColor: LANE_COLORS[lane] }}
        >
          {lane}
        </button>
      ))}
    </div>
    <div className="flex items-center gap-1.5 bg-os-bg border border-os-border rounded px-2 py-1 ml-auto">
      <Search size={12} className="text-os-text/40 shrink-0" />
      <input
        type="text"
        placeholder="Search name or ID…"
        value={searchQuery}
        onChange={e => onSearchChange(e.target.value)}
        className="bg-transparent text-xs text-os-text outline-none w-44 placeholder:text-os-text/30"
      />
    </div>
    <button
      onClick={onSwot}
      className="px-2 py-1 text-xs rounded border border-blue-400 text-blue-300 hover:bg-blue-900 flex items-center gap-1"
      title="View SWOT Analysis"
    >
      <BarChart2 size={12} /> SWOT
    </button>
    <button
      onClick={onRisk}
      className="px-2 py-1 text-xs rounded border border-yellow-400 text-yellow-300 hover:bg-yellow-900 flex items-center gap-1"
      title="View Risk Register"
    >
      <AlertTriangle size={12} /> Risk
    </button>
    <button
      onClick={onNew}
      className="flex items-center gap-1 text-[10px] px-2 py-1.5 bg-os-accent text-black rounded font-semibold hover:opacity-90"
    >
      <Plus size={11} /> New
    </button>
  </div>
);

// ── ProjectManager ───────────────────────────────────────────────────────────

export const ProjectManager: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [ideasLoading, setIdeasLoading] = useState(true);
  const [ideasError, setIdeasError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLane, setSelectedLane] = useState<Lane | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [editTarget, setEditTarget] = useState<Project | 'new' | null>(null);
  const [editIdeaTarget, setEditIdeaTarget] = useState<Idea | null>(null);
  const [sectionModal, setSectionModal] = useState<null | 'swot' | 'risk'>(null);
  const [insightIdeaId, setInsightIdeaId] = useState<string | null>(null);
  const [promotingIdeaId, setPromotingIdeaId] = useState<string | null>(null);
  const dragProjectId = useRef<string | null>(null);
  const dragIdeaId = useRef<string | null>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setSectionModal(null);
        setEditIdeaTarget(null);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  const reload = () => {
    setLoading(true);
    setError(null);
    fetchApi('/api/projects')
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then((data: Project[]) => {
        setProjects(data);
        setLoading(false);
      })
      .catch(err => {
        const localProjects = getLocalProjectSnapshot();
        if (localProjects.length > 0) {
          // Keep the board usable in read mode when backend API is temporarily unavailable.
          setProjects(localProjects);
          setLoading(false);
          setError(null);
          return;
        }
        setError(String(err.message));
        setLoading(false);
      });
  };

  const reloadIdeas = () => {
    setIdeasLoading(true);
    setIdeasError(null);
    const ideasParams = new URLSearchParams({
      implemented: 'exclude',
      implemented_mode: 'active_or_released',
      sort: 'rank',
      order: 'asc',
    });
    fetchApi(`/api/ideas?${ideasParams.toString()}`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then((data: Idea[]) => {
        setIdeas(data);
        setIdeasLoading(false);
      })
      .catch(err => {
        const message = String((err as Error).message ?? err);
        if (isIdeasBackendUnavailable(message)) {
          // Keep Ideas usable when API/proxy/backend is transiently offline.
          const localIdeas = getLocalIdeasSnapshot();
          setIdeasError(null);
          setIdeas(localIdeas);
          setIdeasLoading(false);
          return;
        }
        setIdeasError(message);
        setIdeas([]);
        setIdeasLoading(false);
      });
  };

  useEffect(() => {
    reload();
    reloadIdeas();
    const interval = window.setInterval(() => {
      reload();
      reloadIdeas();
    }, 30000);

    return () => window.clearInterval(interval);
  }, []);

  // Apply a saved project back into local state without a full reload
  const applyUpdate = (saved: Project) => {
    setProjects(ps => {
      const idx = ps.findIndex(p => p.id === saved.id);
      if (idx === -1) return [...ps, saved];
      const next = [...ps];
      next[idx] = saved;
      return next;
    });
    reloadIdeas();
    setEditTarget(null);
  };

  const applyIdeaUpdate = (saved: Idea) => {
    setIdeas(prev => prev.map(idea => (idea.idea_id === saved.idea_id ? saved : idea)));
    setEditIdeaTarget(null);
  };

  const openInsightFromIdea = (mode: InsightMode, ideaId: string) => {
    setInsightIdeaId(ideaId);
    setSectionModal(mode);
  };

  const triggerAgentflowForIdea = async (idea: Idea, projectId: string): Promise<void> => {
    const registerSource = await getLatestKanbanRegistersSource();
    const swot = parseSwot(registerSource.swot);
    const risks = parseRiskRegister(registerSource.risk_register);
    const ideaSwot = getIdeaSwotContext(idea, swot);
    const ideaRisks = getIdeaRiskContext(idea, risks);

    const prompt = [
      `Start project workflow for ${projectId} from idea reference ${idea.idea_id}.`,
      '',
      'Idea context',
      `- idea_id: ${idea.idea_id}`,
      `- title: ${idea.title}`,
      `- summary: ${idea.summary}`,
      `- source: ${idea.source_path}`,
      '',
      'SWOT context',
      formatSwotContextMarkdown(ideaSwot),
      '',
      'Risk context',
      formatRiskContextMarkdown(ideaRisks),
      '',
      '@0master responsibilities',
      '- Validate the promotion intent for the specific idea_id and project_id.',
      '- Open and coordinate the full agentflow in strict sequence, then monitor handoffs.',
      '- Ensure governance checks and unblock or escalate blockers quickly.',
      '',
      '@10idea responsibilities',
      '- Monitor docs/project/ideas for duplicate or highly similar idea scopes.',
      '- Merge overlapping ideas into a single, more complete idea artifact with explicit acceptance criteria.',
      '- Archive superseded idea files into docs/project/ideas/archive with traceability notes.',
      '',
      '@1project responsibilities',
      '- Convert the idea context into a concrete project definition artifact for the project folder.',
      '- Fill all checklist elements and map them to actionable work items.',
      '- Include explicit failure handling, rollback criteria, and lessons-learned capture points.',
      '',
      'Project definition template',
      buildProjectDefinitionChecklistMarkdown(),
      '',
      `Required flow: @0master -> @10idea -> @1project -> @2think -> @3design -> @4plan -> @5test -> @6code -> @7exec -> @8ql -> @9git.`,
    ].join('\n');

    enqueueAgentflowInbox({
      agentId: '0master',
      text: prompt,
      createdAt: new Date().toISOString(),
    });

    const pipeline = await apiRunPipeline(prompt);
    await appendAgentLog('0master', [
      `[${new Date().toLocaleTimeString()}] User: ${prompt}`,
      `[${new Date().toLocaleTimeString()}] Agentflow run started: ${pipeline.pipeline_id}`,
      `[${new Date().toLocaleTimeString()}] @0master (via FLM (default)): Received — processing your request…`,
    ]);
  };

  const promoteIdeaToDiscovery = async (idea: Idea) => {
    setPromotingIdeaId(idea.idea_id);
    try {
      let targetProjectId = idea.mapped_project_ids[0] ?? null;

      // Ensure baseline SWOT/Risk data exists whenever an idea is promoted via PM actions.
      await apiPatchIdea(idea.idea_id, { ensure_swot_risk_data: true });

      if (targetProjectId) {
        await apiPatch(targetProjectId, { lane: 'Discovery' });
      } else {
        const createdProject = await apiCreate({
          id: NEXT_PROJECT_ID,
          name: idea.title,
          lane: 'Discovery',
          summary: idea.summary,
          branch: null,
          pr: null,
          priority: 'P3',
          budget_tier: 'S',
          tags: ['idea', idea.idea_id],
          created: TODAY,
          updated: TODAY,
        });
        targetProjectId = createdProject.id;
        const updatedIdea = await apiPatchIdea(idea.idea_id, {
          mapped_project_ids: [createdProject.id],
        });
        setIdeas(prev => prev.map(current => (current.idea_id === updatedIdea.idea_id ? updatedIdea : current)));
      }

      if (targetProjectId) {
        await triggerAgentflowForIdea(idea, targetProjectId);
      }
      reload();
      reloadIdeas();
    } catch (e) {
      const message = String((e as Error).message);
      setIdeasError(message);
    } finally {
      setPromotingIdeaId(null);
    }
  };

  // Drag-and-drop: drop onto a lane column
  const handleDrop = async (targetLane: Lane) => {
    const ideaId = dragIdeaId.current;
    if (ideaId) {
      dragIdeaId.current = null;
      if (targetLane === 'Discovery') {
        const idea = ideas.find(item => item.idea_id === ideaId);
        if (idea) {
          await promoteIdeaToDiscovery(idea);
        }
      }
      return;
    }

    const id = dragProjectId.current;
    if (!id) return;
    dragProjectId.current = null;
    const project = projects.find(p => p.id === id);
    if (!project || project.lane === targetLane) return;
    // Optimistic update
    setProjects(ps => ps.map(p => p.id === id ? { ...p, lane: targetLane, updated: TODAY } : p));
    try {
      await apiPatch(id, { lane: targetLane });
      reloadIdeas();
    } catch {
      // Rollback on failure
      setProjects(ps => ps.map(p => p.id === id ? { ...p, lane: project.lane } : p));
    }
  };

  const filtered = projects.filter(p => {
    const matchLane = selectedLane === null || p.lane === selectedLane;
    const q = searchQuery.toLowerCase();
    const matchSearch = !q || p.name.toLowerCase().includes(q) || p.id.includes(q) ||
      p.summary.toLowerCase().includes(q) || p.tags.some(t => t.includes(q));
    return matchLane && matchSearch;
  });

  const byLane = Object.fromEntries(LANES.map(l => [l, [] as Project[]])) as Record<Lane, Project[]>;
  for (const p of filtered) byLane[p.lane]?.push(p);

  if (loading) return (
    <div className="flex items-center justify-center h-full bg-os-bg text-os-text">
      <Loader2 size={24} className="animate-spin text-os-accent" />
      <span className="ml-2 text-sm">Loading projects…</span>
    </div>
  );

  if (error) return (
    <div className="flex flex-col items-center justify-center h-full bg-os-bg text-os-text gap-3">
      <AlertTriangle size={28} className="text-amber-400" />
      <span className="text-sm text-os-text/70">Failed to load projects</span>
      <span className="text-xs font-mono text-os-text/40">{error}</span>
      <button onClick={reload} className="text-xs px-3 py-1.5 border border-os-border rounded hover:border-os-accent text-os-text/60">
        Retry
      </button>
    </div>
  );

  return (
    <div className="flex flex-col h-full bg-os-bg text-os-text">
      <div className="flex items-center justify-between px-3 py-2 bg-os-window border-b border-os-border text-sm">
        <span className="font-semibold">Project Manager</span>
        <span className="text-xs text-os-text/50 font-mono">{projects.length} projects · drag cards to move lanes · hover to edit</span>
      </div>
      <FilterBar
        selectedLane={selectedLane}
        onLaneChange={setSelectedLane}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        onNew={() => setEditTarget('new')}
        onSwot={() => setSectionModal('swot')}
        onRisk={() => setSectionModal('risk')}
      />
      <div className="flex-1 p-3 min-h-0">
        <div className="flex-1 overflow-x-auto overflow-y-hidden">
          <div className="flex gap-3 h-full">
            <IdeasColumn
              ideas={ideas}
              ideasLoading={ideasLoading}
              ideasError={ideasError}
              promotingIdeaId={promotingIdeaId}
              onDragStartIdea={ideaId => {
                dragIdeaId.current = ideaId;
                dragProjectId.current = null;
              }}
              onEditIdea={setEditIdeaTarget}
              onOpenInsightForIdea={openInsightFromIdea}
              onPromoteIdea={promoteIdeaToDiscovery}
            />
            <FlowColumn
              projectsByLane={byLane}
              onEdit={p => setEditTarget(p)}
              onDragStart={id => {
                dragProjectId.current = id;
                dragIdeaId.current = null;
              }}
              onDrop={handleDrop}
            />
            {BOARD_LANES.map(lane => (
              <LaneColumn
                key={lane}
                lane={lane}
                projects={byLane[lane]}
                onEdit={p => setEditTarget(p)}
                onDragStart={id => {
                  dragProjectId.current = id;
                  dragIdeaId.current = null;
                }}
                onDrop={handleDrop}
              />
            ))}
          </div>
        </div>
      </div>

      {editTarget !== null && (
        <EditModal
          project={editTarget === 'new' ? null : editTarget}
          onSave={applyUpdate}
          onClose={() => setEditTarget(null)}
        />
      )}

      {editIdeaTarget !== null && (
        <IdeaEditModal
          idea={editIdeaTarget}
          onSave={applyIdeaUpdate}
          onClose={() => setEditIdeaTarget(null)}
        />
      )}

      {sectionModal && (
        <InsightsModal
          mode={sectionModal}
          ideas={ideas}
          initialIdeaId={insightIdeaId}
          onClose={() => {
            setSectionModal(null);
            setInsightIdeaId(null);
          }}
        />
      )}
    </div>
  );
};
