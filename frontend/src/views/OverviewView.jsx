import React, { useState, useEffect } from 'react';
import { 
  Play, Pause, OctagonAlert, Sparkles, TrendingUp, Users, 
  MessageSquare, Film, Image as ImageIcon, BookOpen, AlertTriangle, CheckCircle2, Clock
} from 'lucide-react';

export default function OverviewView({ setActiveTab }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  const fetchOverview = async () => {
    try {
      const res = await fetch('/api/overview');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
    const interval = setInterval(fetchOverview, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleAction = async (endpoint) => {
    setActionLoading(true);
    try {
      await fetch(endpoint, { method: 'POST' });
      await fetchOverview();
    } catch (e) {
      alert("Action failed: " + e.message);
    } finally {
      setActionLoading(false);
    }
  };

  if (loading && !data) {
    return <div className="p-8 text-slate-400">Loading autonomous network overview...</div>;
  }

  const s = data || {};
  const today = s.today_stats || {};
  const totals = s.totals || {};
  const sys = s.system_status || {};

  return (
    <div className="space-y-6">
      {/* Top Banner & Emergency Controls */}
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 shadow-xl flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-white tracking-wide">Desi Hip-Hop Mission Control</h1>
            {sys.emergency_stopped ? (
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-red-950 text-red-400 border border-red-700">EMERGENCY STOPPED</span>
            ) : sys.automation_active ? (
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-950 text-emerald-400 border border-emerald-700 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                AUTONOMOUS MODE ACTIVE
              </span>
            ) : (
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-950 text-amber-400 border border-amber-700">PAUSED</span>
            )}
          </div>
          <p className="text-slate-400 text-sm mt-1">Autonomous content creation, scheduling, comment management & self-learning for Indian Hip-Hop.</p>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          {sys.automation_active ? (
            <button 
              onClick={() => handleAction('/api/overview/pause')} 
              disabled={actionLoading}
              className="px-4 py-2.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30 text-sm font-semibold flex items-center gap-2 transition"
            >
              <Pause size={16} /> Pause Auto
            </button>
          ) : (
            <button 
              onClick={() => handleAction('/api/overview/start')} 
              disabled={actionLoading}
              className="px-4 py-2.5 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-sm font-semibold flex items-center gap-2 transition"
            >
              <Play size={16} /> Resume Auto
            </button>
          )}

          <button 
            onClick={() => handleAction('/api/overview/generate-now')}
            disabled={actionLoading}
            className="px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-sm font-bold flex items-center gap-2 shadow-lg shadow-purple-600/20 transition"
          >
            <Sparkles size={16} /> Generate Now
          </button>

          <button 
            onClick={() => handleAction('/api/overview/emergency-stop')}
            disabled={actionLoading}
            className="px-4 py-2.5 rounded-xl bg-red-600 hover:bg-red-500 text-white text-sm font-bold flex items-center gap-2 shadow-lg shadow-red-600/20 transition"
          >
            <OctagonAlert size={16} /> Emergency Stop
          </button>
        </div>
      </div>

      {/* Daily Target Progress Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 text-sm">
            <span>Today's Image Posts</span>
            <ImageIcon size={18} className="text-purple-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{today.posts_published || 0}</span>
            <span className="text-slate-500 text-sm font-medium">/ {today.posts_target || 10} Target</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
            <div 
              className="bg-purple-500 h-full rounded-full transition-all" 
              style={{ width: `${Math.min(100, ((today.posts_published || 0) / (today.posts_target || 10)) * 100)}%` }}
            ></div>
          </div>
        </div>

        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 text-sm">
            <span>Today's Reels</span>
            <Film size={18} className="text-amber-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{today.reels_published || 0}</span>
            <span className="text-slate-500 text-sm font-medium">/ {today.reels_target || 5} Target</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
            <div 
              className="bg-amber-500 h-full rounded-full transition-all" 
              style={{ width: `${Math.min(100, ((today.reels_published || 0) / (today.reels_target || 5)) * 100)}%` }}
            ></div>
          </div>
        </div>

        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-5 relative overflow-hidden">
          <div className="flex items-center justify-between text-slate-400 text-sm">
            <span>Today's Stories</span>
            <BookOpen size={18} className="text-emerald-400" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{today.stories_published || 0}</span>
            <span className="text-slate-500 text-sm font-medium">/ {today.stories_target || 1} Target</span>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
            <div 
              className="bg-emerald-500 h-full rounded-full transition-all" 
              style={{ width: `${Math.min(100, ((today.stories_published || 0) / (today.stories_target || 1)) * 100)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Cumulative Metrics & Reach Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="bg-[#121723] border border-[#1F293D] rounded-xl p-4">
          <div className="text-xs text-slate-400">Total Reach</div>
          <div className="text-xl font-bold text-white mt-1">{(totals.total_reach || 0).toLocaleString()}</div>
        </div>
        <div className="bg-[#121723] border border-[#1F293D] rounded-xl p-4">
          <div className="text-xs text-slate-400">Total Likes</div>
          <div className="text-xl font-bold text-purple-400 mt-1">{(totals.total_likes || 0).toLocaleString()}</div>
        </div>
        <div className="bg-[#121723] border border-[#1F293D] rounded-xl p-4">
          <div className="text-xs text-slate-400">Comments Handled</div>
          <div className="text-xl font-bold text-emerald-400 mt-1">{(totals.total_comments || 0).toLocaleString()}</div>
        </div>
        <div className="bg-[#121723] border border-[#1F293D] rounded-xl p-4">
          <div className="text-xs text-slate-400">Total Shares</div>
          <div className="text-xl font-bold text-amber-400 mt-1">{(totals.total_shares || 0).toLocaleString()}</div>
        </div>
        <div className="bg-[#121723] border border-[#1F293D] rounded-xl p-4">
          <div className="text-xs text-slate-400">Queue Buffer</div>
          <div className="text-xl font-bold text-blue-400 mt-1">{totals.pending_queue || 0} Ready</div>
        </div>
        <div className="bg-[#121723] border border-[#1F293D] rounded-xl p-4">
          <div className="text-xs text-slate-400">Failed / Retried</div>
          <div className="text-xl font-bold text-rose-400 mt-1">{totals.failed_jobs || 0}</div>
        </div>
      </div>

      {/* Live System Diagnostics & Feeds */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Subsystem Health Cards */}
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 className="text-lg font-bold text-white">Subsystem Status</h2>
            <button onClick={() => setActiveTab('health')} className="text-xs text-purple-400 hover:underline">Full Diagnostics →</button>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div className="flex items-center gap-3">
                <CheckCircle2 size={18} className="text-emerald-400" />
                <div>
                  <div className="text-sm font-semibold text-white">Meta Instagram Graph API</div>
                  <div className="text-xs text-slate-400">{sys.instagram_api?.mode || 'MOCK'} • {sys.instagram_api?.username || 'desihiphop_vibes'}</div>
                </div>
              </div>
              <span className="px-2.5 py-1 text-xs rounded-full bg-emerald-950 text-emerald-400 font-bold">CONNECTED</span>
            </div>

            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div className="flex items-center gap-3">
                <CheckCircle2 size={18} className="text-emerald-400" />
                <div>
                  <div className="text-sm font-semibold text-white">AI Content Engine</div>
                  <div className="text-xs text-slate-400">{sys.ai_engine?.status === 'ONLINE' ? 'Ollama Daemon Active' : 'Autonomous DHH Cultural Template Engine Active'}</div>
                </div>
              </div>
              <span className="px-2.5 py-1 text-xs rounded-full bg-purple-950 text-purple-300 font-bold">
                {sys.ai_engine?.status === 'ONLINE' ? 'LOCAL OLLAMA' : 'TEMPLATE FALLBACK'}
              </span>
            </div>

            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div className="flex items-center gap-3">
                <CheckCircle2 size={18} className="text-emerald-400" />
                <div>
                  <div className="text-sm font-semibold text-white">Video Rendering Subsystem</div>
                  <div className="text-xs text-slate-400">FFmpeg 9:16 Vertical Video + 808 Audio Synthesizer</div>
                </div>
              </div>
              <span className="px-2.5 py-1 text-xs rounded-full bg-emerald-950 text-emerald-400 font-bold">READY</span>
            </div>
          </div>
        </div>

        {/* Recent Community Comments & AI Responses */}
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-5 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h2 className="text-lg font-bold text-white">Recent Fan Interactions</h2>
            <button onClick={() => setActiveTab('comments')} className="text-xs text-purple-400 hover:underline">Manage All ({s.recent_comments?.length || 0}) →</button>
          </div>

          <div className="space-y-3">
            {(s.recent_comments || []).slice(0, 3).map((c) => (
              <div key={c.id} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-purple-300">@{c.username}</span>
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono text-[10px]">{c.classification}</span>
                </div>
                <p className="text-sm text-slate-200">"{c.text}"</p>
                {c.is_replied && (
                  <div className="text-xs text-emerald-400 flex items-center gap-1 mt-1 pt-1 border-t border-slate-800/80">
                    <span>↳ Auto-replied in authentic Hinglish voice</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
