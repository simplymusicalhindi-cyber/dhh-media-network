import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Sparkles, RefreshCw, Layers, Award } from 'lucide-react';

export default function AnalyticsView() {
  const [categories, setCategories] = useState([]);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  const fetchAnalytics = async () => {
    try {
      const [catRes, repRes] = await Promise.all([
        fetch('/api/analytics/categories'),
        fetch('/api/analytics/weekly-report')
      ]);

      if (catRes.ok) setCategories(await catRes.json());
      if (repRes.ok) setReport(await repRes.json());
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const handleGenerateReport = async () => {
    setGenerating(true);
    try {
      const res = await fetch('/api/analytics/generate-report', { method: 'POST' });
      if (res.ok) {
        await fetchAnalytics();
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Analytics & Self-Learning Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Empirical content feedback loop measuring share-to-reach, saves-to-reach, and automatically adjusting publishing weights weekly.
          </p>
        </div>

        <button
          onClick={handleGenerateReport}
          disabled={generating}
          className="px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-purple-600/30 transition"
        >
          <Sparkles size={16} />
          {generating ? 'Synthesizing...' : 'Re-compute Weekly Learning Report'}
        </button>
      </div>

      {/* Weekly Self-Learning Report Card */}
      {report && (
        <div className="bg-gradient-to-r from-purple-950/40 to-slate-900 border border-purple-800/40 rounded-2xl p-6 space-y-4 shadow-xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-bold text-purple-300 uppercase tracking-widest flex items-center gap-1.5">
              <Award size={16} className="text-amber-400" />
              WEEKLY STRATEGY REPORT • WEEK OF {new Date(report.week_start).toLocaleDateString()}
            </span>
            <span className="px-3 py-1 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800 text-xs font-bold">
              STRATEGY APPLIED TO SCHEDULER
            </span>
          </div>

          <p className="text-sm text-slate-200 leading-relaxed font-medium">
            {report.summary}
          </p>

          <div className="pt-2">
            <h3 className="text-xs font-bold text-slate-400 mb-2 uppercase tracking-wider">Recommended Strategy Shifts</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {(report.recommended_strategy_shifts || []).map((shift, i) => (
                <div key={i} className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 flex items-start gap-2">
                  <span className="text-purple-400 font-bold">•</span>
                  <span>{shift}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Category Virality Matrix */}
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <BarChart3 size={18} className="text-purple-400" /> Content Category Virality Matrix
        </h2>

        {loading ? (
          <div className="p-8 text-center text-slate-500 text-sm">Aggregating empirical performance data...</div>
        ) : categories.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-sm">No category performance records found yet.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900 text-xs text-slate-400 uppercase font-semibold border-b border-slate-800">
                <tr>
                  <th className="p-4">Category</th>
                  <th className="p-4">Posts Tracked</th>
                  <th className="p-4">Average Reach</th>
                  <th className="p-4">Avg Shares</th>
                  <th className="p-4">Avg Saves</th>
                  <th className="p-4">Share/Reach Ratio</th>
                  <th className="p-4">Save/Reach Ratio</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {categories.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-900/40 transition">
                    <td className="p-4 font-bold text-white flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-purple-500"></span>
                      {c.category}
                    </td>
                    <td className="p-4 font-mono text-xs">{c.count_published}</td>
                    <td className="p-4 font-mono text-xs text-slate-200">{Math.round(c.avg_reach).toLocaleString()}</td>
                    <td className="p-4 font-mono text-xs text-amber-400">{Math.round(c.avg_shares).toLocaleString()}</td>
                    <td className="p-4 font-mono text-xs text-purple-400">{Math.round(c.avg_saves).toLocaleString()}</td>
                    <td className="p-4">
                      <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-amber-950 text-amber-300 border border-amber-800">
                        {(c.share_to_reach_ratio * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="p-4">
                      <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-purple-950 text-purple-300 border border-purple-800">
                        {(c.saves_to_reach_ratio * 100).toFixed(1)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
