import React, { useState, useEffect, useRef } from 'react';
import { 
  Bot, 
  BrainCircuit, 
  TestTube, 
  Code2, 
  Terminal, 
  GitBranch, 
  Play, 
  Square, 
  RotateCcw, 
  FileText,
  Cpu,
  Activity
} from 'lucide-react';
import { cn } from '../utils';

type AgentType = 'master' | 'plan' | 'test' | 'code' | 'exec' | 'gh';

interface MemoryFile {
  name: string;
  content: string;
}

const AGENTS: { id: AgentType; name: string; icon: React.ElementType; color: string; desc: string }[] = [
  { id: 'master', name: '@master', icon: Cpu, color: 'text-purple-400', desc: 'Orchestrator' },
  { id: 'plan', name: '@plan', icon: BrainCircuit, color: 'text-blue-400', desc: 'Architect' },
  { id: 'test', name: '@test', icon: TestTube, color: 'text-yellow-400', desc: 'QA Engineer' },
  { id: 'code', name: '@code', icon: Code2, color: 'text-green-400', desc: 'Developer' },
  { id: 'exec', name: '@exec', icon: Terminal, color: 'text-orange-400', desc: 'Runtime' },
  { id: 'gh', name: '@gh', icon: GitBranch, color: 'text-white', desc: 'Version Control' },
];

const INITIAL_MEMORY: Record<string, string> = {
  'memory.master.md': '# Master Log\n\nInitializing system...\nWaiting for user input...',
  'memory.plan.md': '# Implementation Plan\n\n- [ ] Analyze requirements\n- [ ] Define architecture',
  'memory.test.md': '# Test Suite\n\n// Pending plan approval',
  'memory.code.md': '// Source Code\n\nconst app = require("express")();',
  'memory.exec.md': '> Execution Logs\n\n$ node server.js\nWaiting...',
  'memory.gh.md': '# GitHub Actions\n\nNo active PRs.',
};

export const CodeBuilder: React.FC = () => {
  const [activeAgent, setActiveAgent] = useState<AgentType>('master');
  const [isRunning, setIsRunning] = useState(false);
  const [memory, setMemory] = useState(INITIAL_MEMORY);
  const [selectedFile, setSelectedFile] = useState<string>('memory.master.md');
  const [logs, setLogs] = useState<string[]>(['System initialized.']);
  const logsEndRef = useRef<HTMLDivElement>(null);

  const addLog = (msg: string) => {
    setLogs(prev => [...prev.slice(-50), `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs]);

  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(() => {
      // Simulation Logic
      switch (activeAgent) {
        case 'master':
          setActiveAgent('plan');
          addLog('@master: Delegating task to @plan agent.');
          setMemory(prev => ({
            ...prev,
            'memory.master.md': prev['memory.master.md'] + '\n- Delegated task to @plan'
          }));
          break;
        case 'plan':
          setActiveAgent('test');
          addLog('@plan: Architecture defined. Requesting tests.');
          setMemory(prev => ({
            ...prev,
            'memory.plan.md': prev['memory.plan.md'] + '\n- [x] Architecture defined\n- [ ] Reviewing constraints'
          }));
          break;
        case 'test':
          setActiveAgent('code');
          addLog('@test: Unit tests generated. Passing to @code.');
          setMemory(prev => ({
            ...prev,
            'memory.test.md': prev['memory.test.md'] + '\n\ndescribe("Auth", () => {\n  it("should login", () => { ... });\n});'
          }));
          break;
        case 'code':
          setActiveAgent('exec');
          addLog('@code: Implementation complete. Starting build.');
          setMemory(prev => ({
            ...prev,
            'memory.code.md': prev['memory.code.md'] + '\n\nfunction login() {\n  return true;\n}'
          }));
          break;
        case 'exec':
          setActiveAgent('gh');
          addLog('@exec: Build successful. Tests passed (3/3).');
          setMemory(prev => ({
            ...prev,
            'memory.exec.md': prev['memory.exec.md'] + '\n> Tests passed.\n> Build successful.'
          }));
          break;
        case 'gh':
          setActiveAgent('plan'); // Loop back
          addLog('@gh: PR created #123. Merged to main.');
          setMemory(prev => ({
            ...prev,
            'memory.gh.md': prev['memory.gh.md'] + '\n- Pushed commit a1b2c3d\n- Created PR #42'
          }));
          break;
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [isRunning, activeAgent]);

  const toggleRun = () => setIsRunning(!isRunning);
  const reset = () => {
    setIsRunning(false);
    setActiveAgent('master');
    setMemory(INITIAL_MEMORY);
    setLogs(['System reset.']);
  };

  return (
    <div className="h-full flex flex-col bg-[#0d1117] text-slate-300 font-mono text-sm">
      {/* Toolbar */}
      <div className="h-12 border-b border-slate-800 flex items-center px-4 justify-between bg-[#161b22]">
        <div className="flex items-center gap-2">
          <Bot className="text-purple-500" />
          <span className="font-bold text-slate-100">AgentFlow Builder</span>
        </div>
        <div className="flex items-center gap-2">
          <button 
            onClick={toggleRun}
            className={cn(
              "flex items-center gap-2 px-3 py-1.5 rounded-md transition-all",
              isRunning 
                ? "bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/50" 
                : "bg-green-500/10 text-green-400 hover:bg-green-500/20 border border-green-500/50"
            )}
          >
            {isRunning ? <Square size={14} fill="currentColor" /> : <Play size={14} fill="currentColor" />}
            {isRunning ? 'Stop Workflow' : 'Start Workflow'}
          </button>
          <button 
            onClick={reset}
            className="p-2 hover:bg-slate-800 rounded-md text-slate-400 transition-colors"
          >
            <RotateCcw size={16} />
          </button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar - Agents */}
        <div className="w-64 border-r border-slate-800 bg-[#0d1117] flex flex-col">
          <div className="p-3 text-xs font-bold text-slate-500 uppercase tracking-wider">Active Agents</div>
          <div className="flex-1 space-y-1 px-2">
            {AGENTS.map(agent => {
              const isActive = activeAgent === agent.id;
              const Icon = agent.icon;
              return (
                <div 
                  key={agent.id}
                  className={cn(
                    "flex items-center gap-3 p-3 rounded-lg border transition-all duration-300",
                    isActive 
                      ? "bg-slate-800 border-slate-600 shadow-lg shadow-purple-900/20" 
                      : "border-transparent opacity-50 grayscale"
                  )}
                >
                  <div className={cn("p-2 rounded-md bg-slate-900", agent.color)}>
                    <Icon size={18} />
                  </div>
                  <div>
                    <div className={cn("font-bold", isActive ? "text-white" : "text-slate-400")}>
                      {agent.name}
                    </div>
                    <div className="text-[10px] text-slate-500">{agent.desc}</div>
                  </div>
                  {isActive && (
                    <Activity size={14} className="ml-auto text-green-400 animate-pulse" />
                  )}
                </div>
              );
            })}
          </div>
          
          {/* Mini Console */}
          <div className="h-1/3 border-t border-slate-800 bg-[#010409] p-2 flex flex-col">
            <div className="text-[10px] text-slate-500 mb-2 flex items-center gap-1">
              <Terminal size={10} /> SYSTEM_LOGS
            </div>
            <div className="flex-1 overflow-y-auto space-y-1 font-mono text-[10px]">
              {logs.map((log, i) => (
                <div key={i} className="text-slate-400 border-l-2 border-slate-800 pl-2 py-0.5">
                  {log}
                </div>
              ))}
              <div ref={logsEndRef} />
            </div>
          </div>
        </div>

        {/* Main Content - Memory Files */}
        <div className="flex-1 flex flex-col bg-[#0d1117]">
          {/* File Tabs */}
          <div className="flex items-center border-b border-slate-800 bg-[#010409] overflow-x-auto">
            {Object.keys(memory).map(filename => (
              <button
                key={filename}
                onClick={() => setSelectedFile(filename)}
                className={cn(
                  "px-4 py-2 text-xs flex items-center gap-2 border-r border-slate-800 transition-colors min-w-fit",
                  selectedFile === filename 
                    ? "bg-[#0d1117] text-white border-t-2 border-t-purple-500" 
                    : "text-slate-500 hover:bg-[#161b22]"
                )}
              >
                <FileText size={12} />
                {filename}
              </button>
            ))}
          </div>

          {/* Editor Area */}
          <div className="flex-1 relative">
            <textarea
              readOnly
              value={memory[selectedFile]}
              className="absolute inset-0 w-full h-full bg-[#0d1117] text-slate-300 p-4 font-mono text-sm resize-none focus:outline-none leading-relaxed"
            />
            
            {/* Floating Status Badge */}
            <div className="absolute bottom-4 right-4 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs text-slate-400 flex items-center gap-2 shadow-xl">
              <div className={cn("w-2 h-2 rounded-full", isRunning ? "bg-green-500 animate-pulse" : "bg-slate-500")} />
              {isRunning ? 'Workflow Active' : 'Workflow Paused'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
