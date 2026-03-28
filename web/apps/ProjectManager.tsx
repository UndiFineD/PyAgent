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
  ChevronDown, ChevronUp, Tag, Pencil, FolderOpen, Plus, X, Check, BarChart2,
} from 'lucide-react';
import { cn } from '../utils';
import kanbanRaw from '../../docs/project/kanban.md?raw';
import nextProjectRaw from '../../data/nextproject.md?raw';
import type { AppMeta } from '../types';

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
  source_path: string;
  mapped_project_ids: string[];
}

// ── Constants ────────────────────────────────────────────────────────────────

const LANES: Lane[] = ['Ideas', 'Discovery', 'Design', 'In Sprint', 'Review', 'Released', 'Archived'];
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

// ── API helpers ───────────────────────────────────────────────────────────────

async function apiPatch(id: string, patch: Partial<Project>): Promise<Project> {
  const r = await fetch(`/api/projects/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...patch, updated: TODAY }),
  });
  if (!r.ok) throw new Error(`PATCH ${id}: HTTP ${r.status}`);
  return r.json();
}

async function apiCreate(project: Project): Promise<Project> {
  const r = await fetch('/api/projects', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(project),
  });
  if (!r.ok) throw new Error(`POST: HTTP ${r.status}`);
  return r.json();
}

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

// ── Helpers ──────────────────────────────────────────────────────────────────

function extractSection(raw: string, heading: string): string {
  const start = raw.indexOf(`## ${heading}`);
  if (start === -1) return `Section "${heading}" not found.`;
  const after = raw.indexOf('\n## ', start + 1);
  return after === -1 ? raw.slice(start) : raw.slice(start, after);
}

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
  const [sectionModal, setSectionModal] = useState<null | 'swot' | 'risk'>(null);
  const dragId = useRef<string | null>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') setSectionModal(null); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  const reload = () => {
    setLoading(true);
    fetch('/api/projects')
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then((data: Project[]) => { setProjects(data); setLoading(false); })
      .catch(err => { setError(String(err.message)); setLoading(false); });
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
    fetch(`/api/ideas?${ideasParams.toString()}`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then((data: Idea[]) => {
        setIdeas(data);
        setIdeasLoading(false);
      })
      .catch(err => {
        setIdeasError(String(err.message));
        setIdeas([]);
        setIdeasLoading(false);
      });
  };

  useEffect(() => {
    reload();
    reloadIdeas();
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
    setEditTarget(null);
  };

  // Drag-and-drop: drop onto a lane column
  const handleDrop = async (targetLane: Lane) => {
    const id = dragId.current;
    if (!id) return;
    dragId.current = null;
    const project = projects.find(p => p.id === id);
    if (!project || project.lane === targetLane) return;
    // Optimistic update
    setProjects(ps => ps.map(p => p.id === id ? { ...p, lane: targetLane, updated: TODAY } : p));
    try {
      await apiPatch(id, { lane: targetLane });
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
        <div className="flex gap-3 h-full min-h-0">
          <div className="flex-1 overflow-x-auto overflow-y-hidden">
            <div className="flex gap-3 h-full">
              {LANES.map(lane => (
                <LaneColumn
                  key={lane}
                  lane={lane}
                  projects={byLane[lane]}
                  onEdit={p => setEditTarget(p)}
                  onDragStart={id => { dragId.current = id; }}
                  onDrop={handleDrop}
                />
              ))}
            </div>
          </div>
          <aside className="w-80 shrink-0 bg-os-window border border-os-border rounded-lg flex flex-col min-h-0">
            <div className="px-3 py-2 border-b border-os-border flex items-center justify-between">
              <span className="text-xs font-semibold">Active Ideas Queue</span>
              <span className="text-[10px] text-os-text/50 font-mono">{ideas.length} ideas</span>
            </div>
            <div className="flex-1 overflow-y-auto p-2 space-y-2">
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
                <div className="text-[10px] text-os-text/40 italic px-1 py-2">No active ideas in queue.</div>
              )}
              {!ideasLoading && !ideasError && ideas.map(idea => (
                <div key={idea.idea_id} className="border border-os-border rounded-md px-2 py-1.5 bg-os-bg/40">
                  <div className="flex items-center gap-1.5 mb-1">
                    <span className="text-[10px] font-mono text-os-text/50 bg-os-window border border-os-border rounded px-1">
                      #{idea.rank ?? '-'}
                    </span>
                    <span className="text-xs font-semibold leading-tight text-os-text truncate" title={idea.title}>
                      {idea.title}
                    </span>
                  </div>
                  <div className="text-[10px] font-mono text-os-text/45 mb-1.5">{idea.idea_id}</div>
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
                </div>
              ))}
            </div>
          </aside>
        </div>
      </div>

      {editTarget !== null && (
        <EditModal
          project={editTarget === 'new' ? null : editTarget}
          onSave={applyUpdate}
          onClose={() => setEditTarget(null)}
        />
      )}

      {sectionModal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
          onClick={() => setSectionModal(null)}
        >
          <div
            className="bg-gray-900 border border-gray-700 rounded-lg shadow-xl max-w-3xl w-full max-h-[80vh] flex flex-col"
            onClick={e => e.stopPropagation()}
          >
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-700">
              <h2 className="text-sm font-semibold text-white">
                {sectionModal === 'swot' ? 'SWOT Analysis' : 'Risk Register'}
              </h2>
              <button
                onClick={() => setSectionModal(null)}
                className="text-gray-400 hover:text-white text-xs"
              >
                ✕ Close
              </button>
            </div>
            <pre className="flex-1 overflow-auto p-4 text-xs text-gray-300 whitespace-pre-wrap font-mono">
              {sectionModal === 'swot'
                ? extractSection(kanbanRaw, 'SWOT Analysis')
                : extractSection(kanbanRaw, 'Risk Register')}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
