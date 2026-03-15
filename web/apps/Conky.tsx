import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { Cpu, HardDrive, Wifi, Activity } from 'lucide-react';

const generateData = (length: number) => {
  return Array.from({ length }, (_, i) => ({
    time: i,
    cpu: Math.floor(Math.random() * 40) + 20,
    mem: Math.floor(Math.random() * 30) + 40,
    net: Math.floor(Math.random() * 100),
  }));
};

export const Conky: React.FC = () => {
  const [data, setData] = useState(generateData(20));
  const [stats, setStats] = useState({
    cpu: 0,
    mem: 0,
    netUp: 0,
    netDown: 0,
    diskRead: 0,
    diskWrite: 0,
    tokens: 12450
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setData(prev => {
        const next = [...prev.slice(1), {
          time: prev[prev.length - 1].time + 1,
          cpu: Math.floor(Math.random() * 60) + 10,
          mem: Math.floor(Math.random() * 20) + 50,
          net: Math.floor(Math.random() * 80)
        }];
        
        setStats({
          cpu: next[next.length - 1].cpu,
          mem: next[next.length - 1].mem,
          netUp: Math.floor(Math.random() * 500),
          netDown: Math.floor(Math.random() * 2000),
          diskRead: Math.floor(Math.random() * 10),
          diskWrite: Math.floor(Math.random() * 5),
          tokens: 12450 + Math.floor(Date.now() / 10000) // Fake increment
        });
        
        return next;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-full bg-black/80 text-green-400 font-mono p-4 text-xs flex flex-col gap-4 overflow-hidden">
      <div className="flex items-center justify-between border-b border-green-900/50 pb-2">
        <span className="font-bold text-lg">SYSTEM_MONITOR</span>
        <Activity size={16} className="animate-pulse" />
      </div>

      {/* CPU Section */}
      <div className="space-y-1">
        <div className="flex justify-between">
          <span className="flex items-center gap-2"><Cpu size={12} /> CPU_LOAD</span>
          <span>{stats.cpu}%</span>
        </div>
        <div className="h-1 bg-green-900/30 w-full rounded-full overflow-hidden">
          <div className="h-full bg-green-500 transition-all duration-500" style={{ width: `${stats.cpu}%` }} />
        </div>
        <div className="h-24 w-full mt-2">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="colorCpu" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#4ade80" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#4ade80" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <Area type="monotone" dataKey="cpu" stroke="#4ade80" fillOpacity={1} fill="url(#colorCpu)" strokeWidth={1} isAnimationActive={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Memory Section */}
      <div className="space-y-1">
        <div className="flex justify-between">
          <span className="flex items-center gap-2"><HardDrive size={12} /> MEM_USAGE</span>
          <span>{stats.mem}%</span>
        </div>
        <div className="h-1 bg-green-900/30 w-full rounded-full overflow-hidden">
          <div className="h-full bg-yellow-500 transition-all duration-500" style={{ width: `${stats.mem}%` }} />
        </div>
      </div>

      {/* Network Section */}
      <div className="space-y-1">
        <div className="flex items-center gap-2 mb-1"><Wifi size={12} /> NETWORK_IO</div>
        <div className="grid grid-cols-2 gap-2 text-[10px] text-green-300/80">
          <div>UP: {stats.netUp} KB/s</div>
          <div>DOWN: {stats.netDown} KB/s</div>
        </div>
        <div className="h-16 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <Line type="step" dataKey="net" stroke="#60a5fa" strokeWidth={1} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Token Usage */}
      <div className="mt-auto border-t border-green-900/50 pt-2">
        <div className="text-xs text-green-500 mb-1">TOKEN_USAGE_TODAY</div>
        <div className="text-xl font-bold text-white">{stats.tokens.toLocaleString()}</div>
        <div className="text-[10px] text-green-600">Cost est: ${(stats.tokens * 0.00001).toFixed(4)}</div>
      </div>
    </div>
  );
};
