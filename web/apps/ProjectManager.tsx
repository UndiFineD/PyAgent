/**
 * ProjectManager — NebulaOS app showing all PyAgent projects as a Kanban board.
 *
 * Data source: GET /api/projects (backend/app.py)
 * Lane transitions are git-only (this panel is read-only).
 */
import React, { useState, useEffect } from 'react';
import {
  GitBranch, ExternalLink, Search, Loader2, AlertTriangle, ChevronDown, ChevronUp, Tag
} from 'lucide-react';
import { cn } from '../utils';

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

// ── Constants ────────────────────────────────────────────────────────────────

const LANES: Lane[] = ['Ideas', 'Discovery', 'Design', 'In Sprint', 'Review', 'Released', 'Archived'];

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

// ── ProjectCard ──────────────────────────────────────────────────────────────

const ProjectCard: React.FC<{ project: Project }> = ({ project }) => {
  const [expanded, setExpanded] = useState(false);
  const laneColor = LANE_COLORS[project.lane];
  const priorityColor = PRIORITY_COLORS[project.priority];

  return (
    <div
      className="bg-os-window border border-os-border rounded-lg p-3 mb-2 cursor-pointer hover:border-os-accent/50 transition-colors"
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
      </div>

      <div className="font-semibold text-sm text-os-text mb-1 leading-tight">
        {project.name}
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

const LaneColumn: React.FC<{ lane: Lane; projects: Project[] }> = ({ lane, projects }) => {
  const color = LANE_COLORS[lane];
  return (
    <div className="min-w-[240px] w-64 flex flex-col shrink-0">
      <div
        className="flex items-center justify-between px-3 py-2 rounded-t-lg mb-2 text-black"
        style={{ backgroundColor: color }}
      >
        <span className="text-xs font-bold uppercase tracking-wide">{lane}</span>
        <span className="text-xs font-mono bg-black/20 rounded-full px-2 py-0.5">{projects.length}</span>
      </div>
      <div className="flex-1 overflow-y-auto min-h-0 max-h-[calc(100vh-240px)]">
        {projects.length === 0
          ? <div className="text-[10px] text-os-text/30 text-center py-4 italic">empty</div>
          : projects.map(p => <ProjectCard key={p.id} project={p} />)
        }
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
}

const FilterBar: React.FC<FilterBarProps> = ({ selectedLane, onLaneChange, searchQuery, onSearchChange }) => (
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
  </div>
);

// ── ProjectManager ───────────────────────────────────────────────────────────

export const ProjectManager: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLane, setSelectedLane] = useState<Lane | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetch('/api/projects')
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then((data: Project[]) => { setProjects(data); setLoading(false); })
      .catch(err => { setError(String(err.message)); setLoading(false); });
  }, []);

  const filtered = projects.filter(p => {
    const matchLane = selectedLane === null || p.lane === selectedLane;
    const q = searchQuery.toLowerCase();
    const matchSearch = !q || p.name.toLowerCase().includes(q) || p.id.includes(q);
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
    </div>
  );

  return (
    <div className="flex flex-col h-full bg-os-bg text-os-text">
      <div className="flex items-center justify-between px-3 py-2 bg-os-window border-b border-os-border text-sm">
        <span className="font-semibold">Project Manager</span>
        <span className="text-xs text-os-text/50 font-mono">{projects.length} projects</span>
      </div>
      <FilterBar
        selectedLane={selectedLane}
        onLaneChange={setSelectedLane}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
      />
      <div className="flex-1 overflow-x-auto overflow-y-hidden p-3">
        <div className="flex gap-3 h-full">
          {LANES.map(lane => (
            <LaneColumn key={lane} lane={lane} projects={byLane[lane]} />
          ))}
        </div>
      </div>
    </div>
  );
};
