import React, { useState, useEffect } from 'react';
import { AlertOctagon, RefreshCw, CheckCircle2, Terminal, ShieldAlert } from 'lucide-react';

export default function ErrorLogsView() {
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [recovering, setRecovering] = useState(false);
  const [recoveryMsg, setRecoveryMsg] = useState('');

  const fetchErrors = async () => {
    try {
      const res = await fetch('/api/errors');
      if (res.ok) {
        const json = await res.json();
        setErrors(json || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchErrors();
  }, []);

  const handleRecoverNow = async () => {
    setRecovering(true);
    try {
      const res = await fetch('/api/errors/recover-now', { method: 'POST' });
      if (res.ok) {
        const json = await res.json();
        setRecoveryMsg(json.message);
        fetchErrors();
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setRecovering(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Diagnostics & Self-Healing Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Intercepts exceptions, logs full stack traces, and triggers automatic recovery procedures for disk, network, and scheduler interruptions.
          </p>
        </div>

        <button
          onClick={handleRecoverNow}
          disabled={recovering}
          className="px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-purple-600/30 transition"
        >
          <RefreshCw size={16} className={recovering ? 'animate-spin' : ''} />
          {recovering ? 'Recovering Subsystems...' : 'Trigger Auto-Recovery Routine'}
        </button>
      </div>

      {recoveryMsg && (
        <div className="p-4 rounded-xl bg-emerald-950/60 border border-emerald-800 text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 size={16} /> {recoveryMsg}
        </div>
      )}

      {/* Error Logs Table */}
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4">Exception History & Recovery Audit</h2>

        {loading ? (
          <div className="p-8 text-center text-slate-500 text-sm">Loading logs...</div>
        ) : errors.length === 0 ? (
          <div className="p-12 text-center text-emerald-400 text-sm border-2 border-dashed border-emerald-900/30 rounded-xl bg-emerald-950/10">
            <CheckCircle2 size={32} className="mx-auto mb-2 text-emerald-400" />
            Zero unhandled errors recorded. All subsystems running healthy.
          </div>
        ) : (
          <div className="space-y-4">
            {errors.map((err) => {
              const dt = new Date(err.created_at);
              return (
                <div key={err.id} className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-rose-400 font-mono">[{err.module}] {err.exception_type}</span>
                    <span className="text-slate-500 font-mono">{dt.toLocaleString()}</span>
                  </div>
                  <div className="text-xs text-slate-300 font-mono bg-black/60 p-3 rounded-lg border border-slate-800 whitespace-pre-wrap max-h-48 overflow-y-auto">
                    {err.traceback}
                  </div>
                  <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
                    <span>Recovery Action: <strong className="text-purple-300">{err.recovery_action}</strong></span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      err.recovery_successful ? 'bg-emerald-950 text-emerald-400' : 'bg-amber-950 text-amber-400'
                    }`}>
                      {err.recovery_successful ? 'RECOVERED' : 'LOGGED'}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
