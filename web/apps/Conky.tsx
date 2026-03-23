import React, { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, ResponsiveContainer } from 'recharts';
import { Cpu, HardDrive, Wifi, Activity, AlertTriangle } from 'lucide-react';

interface NetworkInterface {
  interface: string;
  tx_kbps: number;
  rx_kbps: number;
}

interface MemoryMetrics {
  used_mb: number;
  total_mb: number;
  percent: number;
}

interface DiskMetrics {
  read_kbps: number;
  write_kbps: number;
}

interface SystemMetrics {
  cpu_percent: number;
  memory: MemoryMetrics;
  network: NetworkInterface[];
  disk: DiskMetrics;
  sampled_at: number;
}

interface ChartPoint {
  time: number;
  cpu: number;
  net: number;
}

const HISTORY_LENGTH = 30;
const TOKENS = 12450;

const emptyHistory = (): ChartPoint[] =>
  Array.from({ length: HISTORY_LENGTH }, (_, i) => ({ time: i, cpu: 0, net: 0 }));

export const Conky: React.FC = () => {
  const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
  const [offline, setOffline] = useState(false);
  const [history, setHistory] = useState<ChartPoint[]>(emptyHistory);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const resp = await fetch('/api/metrics/system');
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const data: SystemMetrics = await resp.json();
        setMetrics(data);
        setOffline(false);
        const totalNet = data.network.reduce((s, n) => s + n.tx_kbps + n.rx_kbps, 0);
        setHistory(prev => {
          const point: ChartPoint = {
            time: (prev[prev.length - 1]?.time ?? 0) + 1,
            cpu: data.cpu_percent,
            net: totalNet,
          };
          return [...prev.slice(1), point];
        });
      } catch {
        setOffline(true);
      }
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 2000);
    return () => clearInterval(interval);
  }, []);

  const cpu = metrics?.cpu_percent ?? 0;
  const mem = metrics?.memory ?? { used_mb: 0, total_mb: 0, percent: 0 };
  const network = metrics?.network ?? [];
  const disk = metrics?.disk ?? { read_kbps: 0, write_kbps: 0 };
  const totalTx = network.reduce((s, n) => s + n.tx_kbps, 0);
  const totalRx = network.reduce((s, n) => s + n.rx_kbps, 0);

  return (
    <div className="h-full bg-black/80 text-green-400 font-mono p-4 text-xs flex flex-col gap-4 overflow-hidden">
      <div className="flex items-center justify-between border-b border-green-900/50 pb-2">
        <span className="font-bold text-lg">SYSTEM_MONITOR</span>
        <div className="flex items-center gap-2">
          {offline && (
            <span className="flex items-center gap-1 text-amber-400 text-[10px]">
              <AlertTriangle size={12} /> OFFLINE
            </span>
          )}
          <Activity size={16} className="animate-pulse" />
        </div>
      </div>

      {/* CPU Section */}
      <div className="space-y-1">
        <div className="flex justify-between">
          <span className="flex items-center gap-2"><Cpu size={12} /> CPU_LOAD</span>
          <span>{cpu.toFixed(1)}%</span>
        </div>
        <div className="h-1 bg-green-900/30 w-full rounded-full overflow-hidden">
          <div className="h-full bg-green-500 transition-all duration-500" style={{ width: `${cpu}%` }} />
        </div>
        <div className="h-24 w-full mt-2">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={history}>
              <defs>
                <linearGradient id="colorCpu" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#4ade80" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#4ade80" stopOpacity={0} />
                </linearGradient>
              </defs>
              <Area
                type="monotone"
                dataKey="cpu"
                stroke="#4ade80"
                fillOpacity={1}
                fill="url(#colorCpu)"
                strokeWidth={1}
                isAnimationActive={false}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Memory Section */}
      <div className="space-y-1">
        <div className="flex justify-between">
          <span className="flex items-center gap-2"><HardDrive size={12} /> MEM_USAGE</span>
          <span>{mem.percent.toFixed(1)}%</span>
        </div>
        <div className="h-1 bg-green-900/30 w-full rounded-full overflow-hidden">
          <div className="h-full bg-yellow-500 transition-all duration-500" style={{ width: `${mem.percent}%` }} />
        </div>
        <div className="text-[10px] text-green-300/80 mt-1">
          {mem.used_mb.toFixed(0)} MB / {mem.total_mb.toFixed(0)} MB
        </div>
      </div>

      {/* Network Section */}
      <div className="space-y-1">
        <div className="flex items-center gap-2 mb-1"><Wifi size={12} /> NETWORK_IO</div>
        {network.length <= 4 ? (
          <div className="space-y-0.5">
            {network.map(iface => (
              <div key={iface.interface} className="grid grid-cols-3 gap-1 text-[10px] text-green-300/80">
                <span className="truncate">{iface.interface}</span>
                <span>TX: {iface.tx_kbps.toFixed(1)}</span>
                <span>RX: {iface.rx_kbps.toFixed(1)}</span>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-2 text-[10px] text-green-300/80">
            <div>UP: {totalTx.toFixed(1)} KB/s</div>
            <div>DOWN: {totalRx.toFixed(1)} KB/s</div>
          </div>
        )}
        <div className="h-16 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={history}>
              <Line type="step" dataKey="net" stroke="#60a5fa" strokeWidth={1} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Disk Section */}
      <div className="space-y-1">
        <div className="text-[10px] text-green-500">DISK_IO</div>
        <div className="grid grid-cols-2 gap-2 text-[10px] text-green-300/80">
          <div>READ: {disk.read_kbps.toFixed(1)} KB/s</div>
          <div>WRITE: {disk.write_kbps.toFixed(1)} KB/s</div>
        </div>
      </div>

      {/* Token Usage */}
      <div className="mt-auto border-t border-green-900/50 pt-2">
        <div className="text-xs text-green-500 mb-1">TOKEN_USAGE_TODAY</div>
        <div className="text-xl font-bold text-white">{TOKENS.toLocaleString()}</div>
        <div className="text-[10px] text-green-600">Cost est: ${(TOKENS * 0.00001).toFixed(4)}</div>
      </div>
    </div>
  );
};
