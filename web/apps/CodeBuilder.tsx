import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  Bot, BrainCircuit, TestTube, Code2, Terminal, GitBranch,
  Play, Square, RotateCcw, Cpu, Activity,
  Lightbulb, Pencil, ShieldCheck, FolderOpen,
  Mic, MicOff, Send, FileCode2, ChevronRight, Eye, ScrollText,
} from 'lucide-react';
import { cn } from '../utils';

// ── Types ───────────────────────────────────────────────────────────────────
type AgentId = '0master' | '1project' | '2think' | '3design' | '4plan' | '5test' | '6code' | '7exec' | '8ql' | '9git';
type TabId = 'chat' | 'logs' | 'doc';
type LlmId = 'flm' | 'gpt41' | 'gpt5mini' | 'grok' | 'raptor';

interface ChatMessage {
  role: 'user' | 'agent';
  text: string;
  ts: string;
}

// ── LLM Providers ─────────────────────────────────────────────────────────────
const LLM_PROVIDERS: { id: LlmId; label: string }[] = [
  { id: 'flm',      label: 'FLM (default)' },
  { id: 'gpt41',    label: 'GPT-4.1' },
  { id: 'gpt5mini', label: 'GPT-5 Mini' },
  { id: 'grok',     label: 'Grok Code Fast 1' },
  { id: 'raptor',   label: 'Raptor Mini (preview)' },
];

// ── Agent Definitions ─────────────────────────────────────────────────────────
const AGENTS: {
  id: AgentId; name: string; icon: React.ElementType;
  color: string; bgColor: string; desc: string; docFile: string;
}[] = [
  { id: '0master',  name: '@0master',  icon: Cpu,          color: 'text-purple-400', bgColor: 'bg-purple-900/30',  desc: 'Orchestrator',      docFile: '0master.agent.md' },
  { id: '1project', name: '@1project', icon: FolderOpen,   color: 'text-blue-400',   bgColor: 'bg-blue-900/30',    desc: 'Project Manager',   docFile: '1project.agent.md' },
  { id: '2think',   name: '@2think',   icon: Lightbulb,    color: 'text-cyan-400',   bgColor: 'bg-cyan-900/30',    desc: 'Options Explorer',  docFile: '2think.agent.md' },
  { id: '3design',  name: '@3design',  icon: Pencil,       color: 'text-indigo-400', bgColor: 'bg-indigo-900/30',  desc: 'Architect',         docFile: '3design.agent.md' },
  { id: '4plan',    name: '@4plan',    icon: BrainCircuit, color: 'text-sky-400',    bgColor: 'bg-sky-900/30',     desc: 'Planner (TDD)',     docFile: '4plan.agent.md' },
  { id: '5test',    name: '@5test',    icon: TestTube,     color: 'text-yellow-400', bgColor: 'bg-yellow-900/30',  desc: 'QA / Red Phase',    docFile: '5test.agent.md' },
  { id: '6code',    name: '@6code',    icon: Code2,        color: 'text-green-400',  bgColor: 'bg-green-900/30',   desc: 'Developer',         docFile: '6code.agent.md' },
  { id: '7exec',    name: '@7exec',    icon: Terminal,     color: 'text-orange-400', bgColor: 'bg-orange-900/30',  desc: 'Runtime Validator', docFile: '7exec.agent.md' },
  { id: '8ql',      name: '@8ql',      icon: ShieldCheck,  color: 'text-red-400',    bgColor: 'bg-red-900/30',     desc: 'Security Scanner',  docFile: '8ql.agent.md' },
  { id: '9git',     name: '@9git',     icon: GitBranch,    color: 'text-slate-300',  bgColor: 'bg-slate-800/50',   desc: 'Git / GitHub',      docFile: '9git.agent.md' },
];


// ── Helpers ───────────────────────────────────────────────────────────────────────
const now = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

const INITIAL_MESSAGES: Record<AgentId, ChatMessage[]> = Object.fromEntries(
  AGENTS.map(a => [a.id, [{ role: 'agent' as const, text: `${a.name} ready. How can I help?`, ts: now() }]])
) as Record<AgentId, ChatMessage[]>;

const INITIAL_INPUT: Record<AgentId, string> = Object.fromEntries(
  AGENTS.map(a => [a.id, ''])
) as Record<AgentId, string>;

// ── Minimal Markdown Renderer ──────────────────────────────────────────────────
function MarkdownView({ content }: { content: string }) {
  if (!content) return <p className="text-xs text-slate-600 italic">No content.</p>;

  function renderInline(text: string, base = 0): React.ReactNode {
    return text.split(/(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)/).map((seg, i) => {
      const k = base * 1000 + i;
      if (seg.startsWith('`') && seg.endsWith('`') && seg.length > 2)
        return <code key={k} className="px-1 py-0.5 bg-slate-800 rounded text-purple-300 text-[11px] font-mono">{seg.slice(1, -1)}</code>;
      if (seg.startsWith('**') && seg.endsWith('**') && seg.length > 4)
        return <strong key={k} className="text-slate-200 font-semibold">{seg.slice(2, -2)}</strong>;
      if (seg.startsWith('*') && seg.endsWith('*') && seg.length > 2)
        return <em key={k} className="text-slate-300 italic">{seg.slice(1, -1)}</em>;
      return seg;
    });
  }

  const lines = content.split('\n');
  const nodes: React.ReactNode[] = [];
  let i = 0;

  // YAML frontmatter
  if (lines[0]?.trim() === '---') {
    const end = lines.findIndex((l, idx) => idx > 0 && l.trim() === '---');
    if (end > 0) {
      nodes.push(
        <div key="fm" className="mb-4 rounded border border-slate-700 bg-[#161b22] px-3 py-2 text-[11px] font-mono text-slate-500 space-y-0.5">
          {lines.slice(1, end).map((m, idx) => <div key={idx}>{m}</div>)}
        </div>
      );
      i = end + 1;
    }
  }

  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }

    const hm = line.match(/^(#{1,3})\s+(.+)/);
    if (hm) {
      const cls = hm[1].length === 1
        ? 'text-slate-100 text-sm font-bold mt-5 mb-2 border-b border-slate-800 pb-1'
        : hm[1].length === 2
        ? 'text-purple-400 text-xs font-semibold mt-4 mb-1.5 uppercase tracking-wide'
        : 'text-slate-300 text-xs font-semibold mt-3 mb-1';
      nodes.push(<div key={i} className={cls}>{renderInline(hm[2], i)}</div>);
      i++; continue;
    }

    if (/^---+$/.test(line.trim())) {
      nodes.push(<hr key={i} className="border-slate-700 my-3" />);
      i++; continue;
    }

    if (line.trim().startsWith('```')) {
      const lang = line.trim().slice(3).trim();
      const code: string[] = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith('```')) { code.push(lines[i]); i++; }
      i++;
      nodes.push(
        <pre key={i} className="my-2 rounded bg-slate-900 border border-slate-700 px-3 py-2 text-[11px] font-mono text-green-300 overflow-x-auto">
          {lang && <div className="text-slate-600 text-[10px] mb-1">{lang}</div>}
          {code.join('\n')}
        </pre>
      );
      continue;
    }

    if (/^[-*]\s/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^[-*]\s/.test(lines[i])) { items.push(lines[i].slice(2)); i++; }
      nodes.push(
        <ul key={i} className="my-1.5 ml-3 space-y-1">
          {items.map((item, idx) => (
            <li key={idx} className="flex gap-1.5 text-xs text-slate-400">
              <span className="text-slate-600 flex-shrink-0 mt-px">•</span>
              <span>{renderInline(item, idx)}</span>
            </li>
          ))}
        </ul>
      );
      continue;
    }

    nodes.push(<p key={i} className="text-xs text-slate-400 leading-relaxed my-0.5">{renderInline(line, i)}</p>);
    i++;
  }

  return <>{nodes}</>;
}

// ── Augmented Window type for SpeechRecognition ───────────────────────────────
interface SpeechRecognitionResult { transcript: string; }
interface SpeechRecognitionEvent  { results: { 0: SpeechRecognitionResult }[]; }
interface SpeechRecognitionHandle {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onresult: ((e: SpeechRecognitionEvent) => void) | null;
  onerror: (() => void) | null;
  onend:   (() => void) | null;
  start: () => void;
  stop:  () => void;
}
declare global {
  interface Window {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    SpeechRecognition: new () => SpeechRecognitionHandle;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    webkitSpeechRecognition: new () => SpeechRecognitionHandle;
  }
}

// ── Component ─────────────────────────────────────────────────────────────────
export const CodeBuilder: React.FC = () => {
  const [activeAgent, setActiveAgent] = useState<AgentId>('0master');
  const [activeTab, setActiveTab]     = useState<TabId>('chat');
  const [agentLlm, setAgentLlm]       = useState<Record<AgentId, LlmId>>(
    Object.fromEntries(AGENTS.map(a => [a.id, 'flm' as LlmId])) as Record<AgentId, LlmId>
  );
  const [isRunning, setIsRunning]     = useState(false);
  const [messages, setMessages]       = useState<Record<AgentId, ChatMessage[]>>(INITIAL_MESSAGES);
  const [inputText, setInputText]     = useState<Record<AgentId, string>>(INITIAL_INPUT);
  const [agentDocs, setAgentDocs]     = useState<Record<AgentId, string>>(
    Object.fromEntries(AGENTS.map(a => [a.id, ''])) as Record<AgentId, string>
  );
  const [docsLoading, setDocsLoading] = useState<Record<AgentId, boolean>>(
    Object.fromEntries(AGENTS.map(a => [a.id, true])) as Record<AgentId, boolean>
  );
  const [docEditing, setDocEditing]   = useState<Record<AgentId, boolean>>(
    Object.fromEntries(AGENTS.map(a => [a.id, false])) as Record<AgentId, boolean>
  );
  const [logs, setLogs]               = useState<string[]>(['[system] AgentFlow Builder v2 initialized.']);
  const [agentLogs, setAgentLogs]     = useState<Record<AgentId, string[]>>(
    Object.fromEntries(AGENTS.map(a => [a.id, [] as string[]])) as Record<AgentId, string[]>
  );
  const [isListening, setIsListening] = useState(false);

  const chatEndRef        = useRef<HTMLDivElement>(null);
  const logsEndRef        = useRef<HTMLDivElement>(null);
  const agentLogsEndRef   = useRef<HTMLDivElement>(null);
  const recognizerRef = useRef<SpeechRecognitionHandle | null>(null);
  const workflowRef   = useRef<{ step: number; timer: ReturnType<typeof setTimeout> | null }>({ step: 0, timer: null });
  const saveTimerRef    = useRef<ReturnType<typeof setTimeout> | null>(null);
  const docSaveTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // ── Load agent docs from .github/agents/ on mount ───────────────────────────
  useEffect(() => {
    AGENTS.forEach(agent => {
      fetch(`/api/agent-doc/${agent.id}`)
        .then(r => r.ok ? r.json() : null)
        .then((data: { content: string } | null) => {
          setAgentDocs(prev => ({ ...prev, [agent.id]: data?.content ?? '' }));
          setDocsLoading(prev => ({ ...prev, [agent.id]: false }));
        })
        .catch(() => {
          setDocsLoading(prev => ({ ...prev, [agent.id]: false }));
        });
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── Debounced auto-save docs to .github/agents/<id>.agent.md ─────────────────
  useEffect(() => {
    if (Object.values(docsLoading).some(Boolean)) return; // skip while initial load in progress
    if (docSaveTimerRef.current) clearTimeout(docSaveTimerRef.current);
    docSaveTimerRef.current = setTimeout(() => {
      AGENTS.forEach(agent => {
        const content = agentDocs[agent.id];
        if (!content) return;
        fetch(`/api/agent-doc/${agent.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content }),
        }).catch(() => { /* backend not running — silently ignore */ });
      });
    }, 2000);
    return () => { if (docSaveTimerRef.current) clearTimeout(docSaveTimerRef.current); };
  }, [agentDocs, docsLoading]);

  // ── Load persisted logs on mount ─────────────────────────────────────────
  useEffect(() => {
    AGENTS.forEach(agent => {
      fetch(`/api/agent-log/${agent.id}`)
        .then(r => r.ok ? r.json() : null)
        .then((data: { content: string } | null) => {
          if (!data?.content) return;
          const lines = data.content.split('\n').filter(Boolean);
          if (lines.length > 0) {
            setAgentLogs(prev => ({ ...prev, [agent.id]: lines }));
            setLogs(prev => [...prev, ...lines].slice(-99));
          }
        })
        .catch(() => { /* backend not running — silently ignore */ });
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── Debounced auto-save logs to docs/agents/<id>.log.md ──────────────────
  useEffect(() => {
    if (saveTimerRef.current) clearTimeout(saveTimerRef.current);
    saveTimerRef.current = setTimeout(() => {
      AGENTS.forEach(agent => {
        const lines = agentLogs[agent.id];
        if (!lines || lines.length === 0) return;
        fetch(`/api/agent-log/${agent.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: lines.join('\n') }),
        }).catch(() => { /* backend not running — silently ignore */ });
      });
    }, 2000);
    return () => { if (saveTimerRef.current) clearTimeout(saveTimerRef.current); };
  }, [agentLogs]);

  // ── Auto-scroll ───────────────────────────────────────────────────────────
  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, activeAgent]);
  useEffect(() => { logsEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [logs]);
  useEffect(() => { agentLogsEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [agentLogs, activeAgent]);

  // ── Helpers ───────────────────────────────────────────────────────────────
  const addLog = useCallback((msg: string) => {
    setLogs(prev => [...prev.slice(-99), `[${now()}] ${msg}`]);
  }, []);

  const addAgentLog = useCallback((agentId: AgentId, msg: string) => {
    const line = `[${now()}] ${msg}`;
    setLogs(prev => [...prev.slice(-99), line]);
    setAgentLogs(prev => ({ ...prev, [agentId]: [...(prev[agentId] ?? []).slice(-199), line] }));
  }, []);

  const addMessage = useCallback((agentId: AgentId, role: 'user' | 'agent', text: string) => {
    setMessages(prev => ({
      ...prev,
      [agentId]: [...prev[agentId], { role, text, ts: now() }],
    }));
  }, []);

  // ── Send Message ──────────────────────────────────────────────────────────
  const sendMessage = useCallback((agentId: AgentId) => {
    const text = inputText[agentId].trim();
    if (!text) return;
    addMessage(agentId, 'user', text);
    const agentName = AGENTS.find(a => a.id === agentId)?.name ?? agentId;
    const currentLlmId = agentLlm[agentId] ?? 'flm';
    const llmLabel = LLM_PROVIDERS.find(l => l.id === currentLlmId)?.label ?? currentLlmId;
    addAgentLog(agentId, `User: ${text}`);
    setInputText(prev => ({ ...prev, [agentId]: '' }));
    setTimeout(() => {
      addMessage(agentId, 'agent', `${agentName} (via ${llmLabel}): Received — processing your request…`);
      addAgentLog(agentId, `Agent responded via ${llmLabel}.`);
    }, 600);
  }, [inputText, addMessage, addAgentLog, agentLlm]);

  // ── Voice Input ───────────────────────────────────────────────────────────
  const toggleVoice = useCallback(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { addLog('[voice] SpeechRecognition not available in this browser.'); return; }
    if (isListening) {
      recognizerRef.current?.stop();
      setIsListening(false);
      return;
    }
    const rec = new SR();
    rec.continuous = false;
    rec.interimResults = false;
    rec.lang = 'en-US';
    rec.onresult = (e: SpeechRecognitionEvent) => {  // local type above
      const transcript = e.results[0][0].transcript;
      setInputText(prev => ({
        ...prev,
        [activeAgent]: prev[activeAgent] ? `${prev[activeAgent]} ${transcript}` : transcript,
      }));
      addLog(`[voice] Transcript: "${transcript}"`);
    };
    rec.onerror = () => { setIsListening(false); addLog('[voice] Recognition error.'); };
    rec.onend   = () => setIsListening(false);
    recognizerRef.current = rec;
    rec.start();
    setIsListening(true);
    addLog('[voice] Listening…');
  }, [isListening, activeAgent, addLog]);

  // ── Workflow Simulation ───────────────────────────────────────────────────
  const workflowSteps = AGENTS.map(a => a.id);

  const stepWorkflow = useCallback(() => {
    const step = workflowRef.current.step;
    const agentId = workflowSteps[step];
    const agent = AGENTS.find(a => a.id === agentId)!;
    setActiveAgent(agentId);
    addMessage(agentId, 'agent', `${agent.name} is active in the workflow pipeline (step ${step + 1}/10).`);
    addAgentLog(agentId, `[workflow] Step ${step + 1}/10 — ${agent.name} (${agent.desc})`);
    workflowRef.current.step = (step + 1) % workflowSteps.length;
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [addMessage, addAgentLog]);

  useEffect(() => {
    if (!isRunning) {
      if (workflowRef.current.timer) { clearTimeout(workflowRef.current.timer); workflowRef.current.timer = null; }
      return;
    }
    const schedule = () => {
      workflowRef.current.timer = setTimeout(() => { stepWorkflow(); schedule(); }, 2500);
    };
    stepWorkflow();
    schedule();
    return () => { if (workflowRef.current.timer) clearTimeout(workflowRef.current.timer); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isRunning]);

  const reset = () => {
    setIsRunning(false);
    workflowRef.current.step = 0;
    setActiveAgent('0master');
    setMessages(INITIAL_MESSAGES);
    setInputText(INITIAL_INPUT);
    setLogs(['[system] AgentFlow Builder reset.']);
    setAgentLogs(Object.fromEntries(AGENTS.map(a => [a.id, [] as string[]])) as Record<AgentId, string[]>);
  };

  // ── Render ────────────────────────────────────────────────────────────────
  const currentAgent = AGENTS.find(a => a.id === activeAgent)!;
  const AgentIcon = currentAgent.icon;

  return (
    <div className="h-full flex flex-col bg-[#0d1117] text-slate-300 font-mono text-sm select-none">

      {/* ── Pipeline Bar ───────────────────────────────────────────────────── */}
      <div className="flex items-center border-b border-slate-800 bg-[#161b22] px-2 py-1.5 gap-1 overflow-x-auto flex-shrink-0">
        {AGENTS.map((agent, idx) => {
          const Icon = agent.icon;
          const isActive = activeAgent === agent.id;
          return (
            <React.Fragment key={agent.id}>
              <button
                onClick={() => setActiveAgent(agent.id)}
                title={agent.desc}
                className={cn(
                  'flex items-center gap-1.5 px-2 py-1 rounded text-[10px] border whitespace-nowrap transition-all',
                  isActive
                    ? cn('border-current', agent.color, agent.bgColor, 'shadow-sm')
                    : 'border-slate-700 text-slate-500 hover:text-slate-300 hover:border-slate-600'
                )}
              >
                <Icon size={11} />
                <span className="font-semibold">{agent.name}</span>
                {isActive && isRunning && <Activity size={9} className="animate-pulse" />}
              </button>
              {idx < AGENTS.length - 1 && <ChevronRight size={10} className="text-slate-700 flex-shrink-0" />}
            </React.Fragment>
          );
        })}

        {/* Start/Stop + Reset pinned to the right */}
        <div className="flex items-center gap-1.5 ml-auto pl-2 flex-shrink-0">
          <button
            onClick={() => setIsRunning(r => !r)}
            className={cn(
              'flex items-center gap-1.5 px-2.5 py-1 rounded text-[10px] transition-all border whitespace-nowrap',
              isRunning
                ? 'bg-red-500/10 text-red-400 border-red-500/50 hover:bg-red-500/20'
                : 'bg-green-500/10 text-green-400 border-green-500/50 hover:bg-green-500/20'
            )}
          >
            {isRunning ? <Square size={10} fill="currentColor" /> : <Play size={10} fill="currentColor" />}
            {isRunning ? 'Stop' : 'Run'}
          </button>
          <button onClick={reset} className="p-1 hover:bg-slate-700 rounded text-slate-500 hover:text-slate-300 transition-colors" title="Reset">
            <RotateCcw size={12} />
          </button>
        </div>
      </div>

      {/* ── Body ───────────────────────────────────────────────────────────── */}
      <div className="flex-1 flex overflow-hidden">

        {/* ── Sidebar ──────────────────────────────────────────────────────── */}
        <div className="w-48 border-r border-slate-800 bg-[#0d1117] flex flex-col flex-shrink-0">
          <div className="px-3 py-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">Agents</div>
          <div className="flex-1 overflow-y-auto px-2 space-y-0.5">
            {AGENTS.map(agent => {
              const Icon = agent.icon;
              const isActive = activeAgent === agent.id;
              return (
                <button
                  key={agent.id}
                  onClick={() => setActiveAgent(agent.id)}
                  className={cn(
                    'w-full flex items-center gap-2 p-2 rounded-lg border text-left transition-all duration-200',
                    isActive ? cn('border-slate-600', agent.bgColor) : 'border-transparent hover:bg-slate-800/50'
                  )}
                >
                  <div className={cn('p-1.5 rounded flex-shrink-0', isActive ? agent.bgColor : 'bg-slate-900', agent.color)}>
                    <Icon size={13} />
                  </div>
                  <div className="min-w-0">
                    <div className={cn('text-xs font-bold truncate', isActive ? 'text-white' : 'text-slate-400')}>
                      {agent.name}
                    </div>
                    <div className="text-[10px] text-slate-500 truncate">{agent.desc}</div>
                  </div>
                  {isActive && isRunning && <Activity size={11} className="ml-auto flex-shrink-0 text-green-400 animate-pulse" />}
                </button>
              );
            })}
          </div>

          {/* System log strip */}
          <div className="h-36 border-t border-slate-800 bg-[#010409] flex flex-col flex-shrink-0">
            <div className="px-2 py-1 text-[10px] text-slate-600 flex items-center gap-1 border-b border-slate-800">
              <Terminal size={9} /> LOG
            </div>
            <div className="flex-1 overflow-y-auto p-1.5 space-y-0.5">
              {logs.map((log, i) => (
                <div key={i} className="text-[10px] text-slate-500 leading-relaxed break-all">{log}</div>
              ))}
              <div ref={logsEndRef} />
            </div>
          </div>
        </div>

        {/* ── Main Panel ───────────────────────────────────────────────────── */}
        <div className="flex-1 flex flex-col overflow-hidden">

          {/* Panel header + tabs */}
          <div className="flex items-center border-b border-slate-800 bg-[#0d1117] px-3 flex-shrink-0">
            <div className={cn('flex items-center gap-2 py-2', currentAgent.color)}>
              <AgentIcon size={15} />
              <span className="text-xs font-bold">{currentAgent.name}</span>
              <span className="text-[10px] text-slate-500">— {currentAgent.desc}</span>
            </div>

            {/* Per-agent LLM selector */}
            <div className="flex items-center gap-1.5 ml-4">
              <span className="text-[10px] text-slate-600 uppercase tracking-wider">LLM</span>
              <select
                value={agentLlm[activeAgent]}
                onChange={e => setAgentLlm(prev => ({ ...prev, [activeAgent]: e.target.value as LlmId }))}
                className="bg-slate-900 border border-slate-700 text-slate-300 text-[11px] rounded px-2 py-0.5 focus:outline-none focus:border-purple-500 transition-colors"
              >
                {LLM_PROVIDERS.map(p => <option key={p.id} value={p.id}>{p.label}</option>)}
              </select>
            </div>

            <div className="flex ml-auto gap-0">
              <button
                onClick={() => setActiveTab('chat')}
                className={cn(
                  'flex items-center gap-1.5 px-3 py-2 text-xs border-b-2 transition-colors',
                  activeTab === 'chat' ? 'border-purple-500 text-white' : 'border-transparent text-slate-500 hover:text-slate-300'
                )}
              >
                <Bot size={12} /> Chat
              </button>
              <button
                onClick={() => setActiveTab('logs')}
                className={cn(
                  'flex items-center gap-1.5 px-3 py-2 text-xs border-b-2 transition-colors',
                  activeTab === 'logs' ? 'border-purple-500 text-white' : 'border-transparent text-slate-500 hover:text-slate-300'
                )}
              >
                <ScrollText size={12} /> Logs
                {agentLogs[activeAgent].length > 0 && (
                  <span className="ml-1 px-1 py-0 rounded bg-slate-700 text-[10px] text-slate-400">
                    {agentLogs[activeAgent].length}
                  </span>
                )}
              </button>
              <button
                onClick={() => setActiveTab('doc')}
                className={cn(
                  'flex items-center gap-1.5 px-3 py-2 text-xs border-b-2 transition-colors',
                  activeTab === 'doc' ? 'border-purple-500 text-white' : 'border-transparent text-slate-500 hover:text-slate-300'
                )}
              >
                <FileCode2 size={12} /> Agent Doc
              </button>
            </div>
          </div>

          {/* ── Chat Tab ─────────────────────────────────────────────────── */}
          {activeTab === 'chat' && (
            <div className="flex-1 flex flex-col overflow-hidden">
              <div className="flex-1 overflow-y-auto p-3 space-y-2">
                {messages[activeAgent].map((msg, i) => (
                  <div
                    key={i}
                    className={cn('flex gap-2 max-w-[88%]', msg.role === 'user' ? 'ml-auto flex-row-reverse' : '')}
                  >
                    <div className={cn(
                      'p-1.5 rounded flex-shrink-0 self-start',
                      msg.role === 'user' ? 'bg-purple-800/50' : currentAgent.bgColor
                    )}>
                      {msg.role === 'user'
                        ? <Bot size={12} className="text-purple-300" />
                        : <AgentIcon size={12} className={currentAgent.color} />
                      }
                    </div>
                    <div className={cn(
                      'rounded-lg px-3 py-2 text-xs leading-relaxed',
                      msg.role === 'user'
                        ? 'bg-purple-900/40 text-slate-200 border border-purple-800/50'
                        : 'bg-slate-800/60 text-slate-300 border border-slate-700/50'
                    )}>
                      <div>{msg.text}</div>
                      <div className="text-[10px] text-slate-600 mt-1">{msg.ts}</div>
                    </div>
                  </div>
                ))}
                <div ref={chatEndRef} />
              </div>

              {/* Input row */}
              <div className="border-t border-slate-800 p-2 flex items-center gap-2 flex-shrink-0 bg-[#0d1117]">
                <button
                  onClick={toggleVoice}
                  title={isListening ? 'Stop listening' : 'Voice input'}
                  className={cn(
                    'p-2 rounded transition-colors flex-shrink-0',
                    isListening ? 'bg-red-500/20 text-red-400 animate-pulse' : 'hover:bg-slate-700 text-slate-500 hover:text-slate-300'
                  )}
                >
                  {isListening ? <MicOff size={14} /> : <Mic size={14} />}
                </button>
                <input
                  type="text"
                  value={inputText[activeAgent]}
                  onChange={e => setInputText(prev => ({ ...prev, [activeAgent]: e.target.value }))}
                  onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(activeAgent); } }}
                  placeholder={`Message ${currentAgent.name}…`}
                  className="flex-1 bg-slate-900 border border-slate-700 rounded px-3 py-1.5 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-purple-500 transition-colors"
                />
                <button
                  onClick={() => sendMessage(activeAgent)}
                  disabled={!inputText[activeAgent].trim()}
                  className="p-2 rounded bg-purple-700/40 text-purple-300 hover:bg-purple-700/60 disabled:opacity-30 disabled:cursor-not-allowed transition-colors flex-shrink-0"
                >
                  <Send size={14} />
                </button>
              </div>
            </div>
          )}

          {/* ── Logs Tab ─────────────────────────────────────────────────── */}
          {activeTab === 'logs' && (
            <div className="flex-1 flex flex-col overflow-hidden">
              <div className="flex items-center gap-2 px-3 py-1.5 border-b border-slate-800 bg-[#161b22] flex-shrink-0">
                <ScrollText size={11} className={currentAgent.color} />
                <span className="text-[10px] text-slate-400 font-semibold">{currentAgent.name} activity log</span>
                <span className="text-[10px] text-slate-600 ml-1">({agentLogs[activeAgent].length} entries)</span>
                <button
                  onClick={() => {
                    setAgentLogs(prev => ({ ...prev, [activeAgent]: [] }));
                    fetch(`/api/agent-log/${activeAgent}`, {
                      method: 'PUT',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ content: '' }),
                    }).catch(() => {});
                  }}
                  className="ml-auto text-[10px] text-slate-600 hover:text-slate-400 px-2 py-0.5 rounded hover:bg-slate-700 transition-colors"
                >
                  Clear
                </button>
              </div>
              <div className="flex-1 overflow-y-auto p-3 space-y-0.5 bg-[#010409]">
                {agentLogs[activeAgent].length === 0 ? (
                  <div className="text-[11px] text-slate-600 italic mt-4 text-center">No activity yet for {currentAgent.name}.</div>
                ) : (
                  agentLogs[activeAgent].map((line, i) => (
                    <div key={i} className="flex gap-2 text-[11px] leading-relaxed">
                      <span className="text-slate-700 flex-shrink-0 select-none">{String(i + 1).padStart(3, '0')}</span>
                      <span className={cn(
                        'break-all',
                        line.includes('User:') ? 'text-purple-300' :
                        line.includes('workflow') ? currentAgent.color :
                        line.includes('error') || line.includes('Error') ? 'text-red-400' :
                        'text-slate-400'
                      )}>{line}</span>
                    </div>
                  ))
                )}
                <div ref={agentLogsEndRef} />
              </div>
            </div>
          )}

          {/* ── Agent Doc Tab ─────────────────────────────────────────────── */}
          {activeTab === 'doc' && (
            <div className="flex-1 flex flex-col overflow-hidden">
              <div className="flex items-center gap-2 px-3 py-1.5 border-b border-slate-800 bg-[#161b22] flex-shrink-0">
                <span className="text-[10px] text-slate-500">.github/agents/{currentAgent.docFile}</span>
                {docsLoading[activeAgent] && (
                  <span className="text-[10px] text-slate-600 italic">Loading…</span>
                )}
                <button
                  onClick={() => setDocEditing(prev => ({ ...prev, [activeAgent]: !prev[activeAgent] }))}
                  className="ml-auto flex items-center gap-1.5 px-2 py-1 text-[10px] rounded bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 border border-slate-700 transition-colors"
                >
                  {docEditing[activeAgent]
                    ? <><Eye size={11} /> Preview</>
                    : <><Pencil size={11} /> Edit</>}
                </button>
              </div>
              {docEditing[activeAgent] ? (
                <textarea
                  value={agentDocs[activeAgent]}
                  onChange={e => setAgentDocs(prev => ({ ...prev, [activeAgent]: e.target.value }))}
                  spellCheck={false}
                  disabled={docsLoading[activeAgent]}
                  placeholder={docsLoading[activeAgent] ? 'Loading from .github/agents/…' : ''}
                  className="flex-1 bg-[#0d1117] text-slate-300 p-4 font-mono text-xs resize-none focus:outline-none leading-relaxed disabled:opacity-50"
                />
              ) : (
                <div className="flex-1 overflow-y-auto p-4">
                  {docsLoading[activeAgent]
                    ? <p className="text-xs text-slate-600 italic">Loading from .github/agents/…</p>
                    : <MarkdownView content={agentDocs[activeAgent]} />
                  }
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* ── Status Bar ─────────────────────────────────────────────────────── */}
      <div className="h-6 border-t border-slate-800 bg-[#161b22] flex items-center px-3 gap-4 flex-shrink-0">
        <div className="flex items-center gap-1.5 text-[10px] text-slate-500">
          <div className={cn('w-1.5 h-1.5 rounded-full', isRunning ? 'bg-green-500 animate-pulse' : 'bg-slate-600')} />
          {isRunning ? 'Workflow running' : 'Idle'}
        </div>
        <div className="text-[10px] text-slate-600">
          LLM: {LLM_PROVIDERS.find(p => p.id === agentLlm[activeAgent])?.label}
        </div>
        {isListening && (
          <div className="flex items-center gap-1 text-[10px] text-red-400 animate-pulse">
            <Mic size={10} /> Listening…
          </div>
        )}
        <div className="ml-auto text-[10px] text-slate-600">
          {currentAgent.name} · {messages[activeAgent].length} messages
        </div>
      </div>
    </div>
  );
};
