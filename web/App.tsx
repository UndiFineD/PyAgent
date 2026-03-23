import React, { useState, useEffect, useRef } from 'react';
import { Login } from './components/Login';
import { Window } from './components/Window';
import { Calculator } from './apps/Calculator';
import { Editor } from './apps/Editor';
import { Paint } from './apps/Paint';
import { Conky } from './apps/Conky';
import { CodeBuilder } from './apps/CodeBuilder';
import { WindowState, AppId, Theme, OsConfig, DEFAULT_OS_CONFIG } from './types';
import { generateId, cn } from './utils';
import {
  Menu, Monitor, Terminal, Palette, Calculator as CalcIcon,
  LogOut, Moon, Sun, MonitorPlay, Bot, Settings, X
} from 'lucide-react';

const INITIAL_WINDOWS: WindowState[] = [
  {
    id: 'welcome-note',
    appId: 'editor',
    title: 'Welcome.md',
    component: <Editor />,
    x: 100,
    y: 100,
    width: 600,
    height: 400,
    zIndex: 1,
    isMinimized: false,
    isMaximized: false,
    hasMenu: true,
  }
];

function loadOsConfig(): OsConfig {
  try {
    const raw = localStorage.getItem('nebula-os-config');
    if (!raw) return DEFAULT_OS_CONFIG;
    const parsed: unknown = JSON.parse(raw);
    if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
      return DEFAULT_OS_CONFIG;
    }
    const data = parsed as Record<string, unknown>;
    return {
      taskbarAlwaysVisible: typeof data.taskbarAlwaysVisible === 'boolean'
        ? data.taskbarAlwaysVisible
        : DEFAULT_OS_CONFIG.taskbarAlwaysVisible,
    };
  } catch {
    return DEFAULT_OS_CONFIG;
  }
}

function saveOsConfig(cfg: OsConfig): void {
  try {
    localStorage.setItem('nebula-os-config', JSON.stringify(cfg));
  } catch {
    // QuotaExceededError or SecurityError — best-effort persistence
  }
}

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [windows, setWindows] = useState<WindowState[]>([]);
  const [activeWindowId, setActiveWindowId] = useState<string | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const [theme, setTheme] = useState<Theme['id']>('dark');
  const [currentTime, setCurrentTime] = useState(new Date());
  
  // Taskbar Auto-hide State
  const [isTaskbarVisible, setIsTaskbarVisible] = useState(true);
  const hideTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [osConfig, setOsConfig] = useState<OsConfig>(loadOsConfig);
  const [settingsOpen, setSettingsOpen] = useState(false);

  // Clock
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Theme Application
  useEffect(() => {
    document.body.className = `theme-${theme} overflow-hidden`;
  }, [theme]);

  // Taskbar Logic
  const showTaskbar = () => {
    if (hideTimeoutRef.current) clearTimeout(hideTimeoutRef.current);
    setIsTaskbarVisible(true);
  };

  const hideTaskbar = () => {
    if (osConfig.taskbarAlwaysVisible) return; // Don't hide if pinned
    if (menuOpen) return; // Don't hide if menu is open
    hideTimeoutRef.current = setTimeout(() => {
      setIsTaskbarVisible(false);
    }, 2000);
  };

  // Keep taskbar visible if menu is open
  useEffect(() => {
    if (menuOpen) {
      showTaskbar();
    } else {
      hideTaskbar();
    }
  }, [menuOpen]);

  // Persist OS config to localStorage on every change
  useEffect(() => {
    saveOsConfig(osConfig);
  }, [osConfig]);

  // Escape key closes settings modal
  useEffect(() => {
    if (!settingsOpen) return;
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') setSettingsOpen(false); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [settingsOpen]);

  const openApp = (appId: AppId) => {
    const id = generateId();
    let component;
    let title = 'Application';
    let width = 600;
    let height = 400;

    switch (appId) {
      case 'calculator':
        component = <Calculator />;
        title = 'Calculator';
        width = 320;
        height = 450;
        break;
      case 'editor':
        component = <Editor />;
        title = 'Text Editor';
        break;
      case 'paint':
        component = <Paint />;
        title = 'Paint Studio';
        width = 800;
        height = 600;
        break;
      case 'conky':
        component = <Conky />;
        title = 'System Monitor';
        width = 300;
        height = 500;
        break;
      case 'codebuilder':
        component = <CodeBuilder />;
        title = 'AgentFlow Builder';
        width = 900;
        height = 600;
        break;
    }

    const newWindow: WindowState = {
      id,
      appId,
      title,
      component,
      x: 50 + (windows.length * 30),
      y: 50 + (windows.length * 30),
      width,
      height,
      zIndex: windows.length + 1,
      isMinimized: false,
      isMaximized: false,
      hasMenu: ['editor', 'paint', 'codebuilder'].includes(appId),
    };

    setWindows([...windows, newWindow]);
    setActiveWindowId(id);
    setMenuOpen(false);
  };

  const closeWindow = (id: string) => {
    setWindows(windows.filter(w => w.id !== id));
    if (activeWindowId === id) setActiveWindowId(null);
  };

  const focusWindow = (id: string) => {
    setActiveWindowId(id);
    setWindows(prev => prev.map(w => ({
      ...w,
      zIndex: w.id === id ? Math.max(...prev.map(p => p.zIndex)) + 1 : w.zIndex
    })));
  };

  const updateWindow = (id: string, updates: Partial<WindowState>) => {
    setWindows(prev => prev.map(w => w.id === id ? { ...w, ...updates } : w));
  };

  const toggleMaximize = (id: string) => {
    setWindows(windows.map(w => w.id === id ? { ...w, isMaximized: !w.isMaximized } : w));
  };

  const toggleMinimize = (id: string) => {
    setWindows(windows.map(w => w.id === id ? { ...w, isMinimized: !w.isMinimized } : w));
  };

  if (!isLoggedIn) {
    return <Login onLogin={() => {
      setIsLoggedIn(true);
      setWindows(INITIAL_WINDOWS);
    }} />;
  }

  return (
    <div className="h-screen w-screen bg-os-bg text-os-text overflow-hidden relative transition-colors duration-300">
      
      {/* Trigger Zone for Taskbar */}
      <div 
        className="fixed top-0 left-0 right-0 h-2 z-[1001]" 
        onMouseEnter={showTaskbar}
      />

      {/* Top Bar (Taskbar) */}
      <div 
        className={cn(
          "fixed top-0 left-0 right-0 h-12 bg-os-header/90 backdrop-blur-md border-b border-os-border flex items-center justify-between px-4 z-[1000] shadow-sm transition-transform duration-500 ease-in-out",
          !isTaskbarVisible && !menuOpen ? "-translate-y-full" : "translate-y-0"
        )}
        onMouseEnter={showTaskbar}
        onMouseLeave={hideTaskbar}
      >
        <div className="flex items-center gap-4">
          <span className="font-bold text-lg tracking-tight">NebulaOS</span>
          <div className="h-4 w-px bg-os-border mx-2" />
          {/* Taskbar Items */}
          <div className="flex items-center gap-2">
            {windows.map(w => (
              <button
                key={w.id}
                onClick={() => {
                  if (w.isMinimized) toggleMinimize(w.id);
                  focusWindow(w.id);
                }}
                className={cn(
                  "px-3 py-1 rounded text-xs max-w-[120px] truncate transition-all",
                  activeWindowId === w.id && !w.isMinimized
                    ? "bg-os-accent text-white shadow-sm"
                    : "bg-os-window hover:bg-os-border text-os-text/80"
                )}
              >
                {w.title}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-sm font-mono opacity-80 hidden sm:block">
            {currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
          
          {/* The "3 Carrot" Menu Trigger */}
          <div className="relative">
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className={cn(
                "p-2 rounded-lg transition-all duration-200 hover:bg-os-border active:scale-95",
                menuOpen && "bg-os-accent text-white rotate-90"
              )}
            >
              <Menu size={20} />
            </button>

            {/* Dropdown Menu */}
            {menuOpen && (
              <>
                <div className="fixed inset-0 z-40" onClick={() => setMenuOpen(false)} />
                <div className="absolute right-0 top-full mt-2 w-64 bg-os-window border border-os-border rounded-xl shadow-2xl z-50 overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
                  <div className="p-2 space-y-1">
                    <div className="px-3 py-2 text-xs font-semibold text-os-text/50 uppercase tracking-wider">Applications</div>
                    <button onClick={() => openApp('codebuilder')} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors">
                      <Bot size={16} className="text-purple-400" /> AgentFlow Builder
                    </button>
                    <button onClick={() => openApp('editor')} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors">
                      <Terminal size={16} className="text-blue-400" /> Text Editor
                    </button>
                    <button onClick={() => openApp('calculator')} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors">
                      <CalcIcon size={16} className="text-orange-400" /> Calculator
                    </button>
                    <button onClick={() => openApp('paint')} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors">
                      <Palette size={16} className="text-pink-400" /> Paint Studio
                    </button>
                    <button onClick={() => openApp('conky')} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors">
                      <Monitor size={16} className="text-green-400" /> System Monitor
                    </button>

                    <div className="h-px bg-os-border my-2" />
                    
                    <div className="px-3 py-2 text-xs font-semibold text-os-text/50 uppercase tracking-wider">Appearance</div>
                    <div className="grid grid-cols-3 gap-2 px-2">
                      <button onClick={() => setTheme('dark')} className={cn("flex flex-col items-center gap-1 p-2 rounded border transition-all", theme === 'dark' ? "bg-slate-800 border-blue-500 text-white" : "border-transparent hover:bg-os-bg")}>
                        <Moon size={14} /> <span className="text-[10px]">Dark</span>
                      </button>
                      <button onClick={() => setTheme('light')} className={cn("flex flex-col items-center gap-1 p-2 rounded border transition-all", theme === 'light' ? "bg-slate-100 border-blue-500 text-black" : "border-transparent hover:bg-os-bg")}>
                        <Sun size={14} /> <span className="text-[10px]">Light</span>
                      </button>
                      <button onClick={() => setTheme('retro')} className={cn("flex flex-col items-center gap-1 p-2 rounded border transition-all", theme === 'retro' ? "bg-teal-700 border-blue-900 text-white" : "border-transparent hover:bg-os-bg")}>
                        <MonitorPlay size={14} /> <span className="text-[10px]">Retro</span>
                      </button>
                    </div>

                    <div className="h-px bg-os-border my-2" />

                    <button
                      onClick={() => { setMenuOpen(false); setSettingsOpen(true); }}
                      className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-os-bg text-left text-sm transition-colors"
                    >
                      <Settings size={16} className="text-os-text/70" /> Settings
                    </button>

                    <div className="h-px bg-os-border my-2" />
                    
                    <button onClick={() => setIsLoggedIn(false)} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-red-500/10 hover:text-red-500 text-left text-sm transition-colors">
                      <LogOut size={16} /> Logout
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Settings Modal */}
      {settingsOpen && (
        <div
          className="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm"
          onClick={() => setSettingsOpen(false)}
        >
          <div
            className="rounded-xl shadow-2xl bg-gray-900/95 border border-white/10 p-6 w-80 min-w-[280px]"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-semibold text-white">Settings</h2>
              <button
                onClick={() => setSettingsOpen(false)}
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="Close settings"
              >
                <X size={16} />
              </button>
            </div>

            {/* Taskbar */}
            <div className="mb-4">
              <h3 className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-3">Taskbar</h3>
              <label className="flex items-center justify-between cursor-pointer">
                <span className="text-sm text-gray-200">Always show taskbar</span>
                <button
                  role="switch"
                  aria-checked={osConfig.taskbarAlwaysVisible}
                  onClick={() => setOsConfig(prev => ({ ...prev, taskbarAlwaysVisible: !prev.taskbarAlwaysVisible }))}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ${
                    osConfig.taskbarAlwaysVisible ? 'bg-blue-500' : 'bg-gray-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      osConfig.taskbarAlwaysVisible ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </label>
            </div>
          </div>
        </div>
      )}

      {/* Desktop Area */}
      <div className="absolute inset-0 z-0 overflow-hidden" onClick={() => setActiveWindowId(null)}>
        {/* Desktop Background Image/Pattern */}
        <div className="absolute inset-0 opacity-5 pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')]" />
        
        {windows.map(window => (
          <Window
            key={window.id}
            window={window}
            isActive={activeWindowId === window.id}
            onClose={closeWindow}
            onMinimize={toggleMinimize}
            onMaximize={toggleMaximize}
            onFocus={focusWindow}
            onUpdate={updateWindow}
          />
        ))}
      </div>
    </div>
  );
}