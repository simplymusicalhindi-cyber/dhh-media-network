import React, { useState, useEffect } from 'react';
import { Activity, CheckCircle2, AlertTriangle, RefreshCw, HardDrive, Cpu, Database, Film } from 'lucide-react';

export default function SystemHealthView() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchHealth = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const json = await res.json();
        setHealth(json);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  const subsystems = health?.subsystems || {};

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">System Health & Watchdog Monitor</h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time diagnostics covering SQLite integrity, FFmpeg video rendering, media storage, AI engine, and API connectivity.
          </p>
        </div>

        <button
          onClick={fetchHealth}
          disabled={loading}
          className="px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-purple-600/30 transition"
        >
          <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
          Run Subsystems Sweep
        </button>
      </div>

      {/* Overall Health Card */}
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex items-center justify-between">
        <div>
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Overall Platform Status</div>
          <div className="text-2xl font-black text-white mt-1 flex items-center gap-2">
            <span className={`w-3.5 h-3.5 rounded-full ${health?.overall_status === 'HEALTHY' ? 'bg-emerald-400' : 'bg-amber-400'} animate-pulse`}></span>
            {health?.overall_status || 'CHECKING...'}
          </div>
        </div>

        <div className="text-right text-xs text-slate-400 font-mono">
          Last Diagnostic Sweep: {health?.timestamp ? new Date(health.timestamp).toLocaleTimeString() : 'N/A'}
        </div>
      </div>

      {/* Subsystem Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {Object.entries(subsystems).map(([key, info]) => {
          const isHealthy = info.status === 'HEALTHY';

          return (
            <div key={key} className="bg-[#121723] border border-[#1F293D] rounded-2xl p-5 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider font-mono">
                  {key.replace('_', ' ')}
                </span>
                <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                  isHealthy ? 'bg-emerald-950 text-emerald-400 border-emerald-800' : 'bg-amber-950 text-amber-400 border-amber-800'
                }`}>
                  {info.status}
                </span>
              </div>

              <div className="text-sm font-semibold text-white">
                {info.detail}
              </div>

              <div className="flex items-center gap-1.5 text-xs text-slate-500 pt-2 border-t border-slate-800/80">
                <CheckCircle2 size={14} className={isHealthy ? 'text-emerald-400' : 'text-amber-400'} />
                <span>Automated watchdog monitoring active</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
