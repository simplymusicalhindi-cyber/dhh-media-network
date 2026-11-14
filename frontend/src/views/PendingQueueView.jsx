import React, { useState, useEffect } from 'react';
import { Clock, Send, Trash2, RefreshCw, AlertCircle } from 'lucide-react';

export default function PendingQueueView() {
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionId, setActionId] = useState(null);

  const fetchQueue = async () => {
    try {
      const res = await fetch('/api/queue?status=QUEUED');
      if (res.ok) {
        const json = await res.json();
        setQueue(json || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQueue();
    const interval = setInterval(fetchQueue, 10000);
    return () => clearInterval(interval);
  }, []);

  const handlePublishNow = async (jobId) => {
    setActionId(jobId);
    try {
      const res = await fetch(`/api/queue/${jobId}/publish-now`, { method: 'POST' });
      if (res.ok) {
        alert("Published successfully!");
        fetchQueue();
      } else {
        alert("Publish failed");
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setActionId(null);
    }
  };

  const handleCancel = async (jobId) => {
    if (!confirm("Are you sure you want to cancel this queued item?")) return;
    try {
      await fetch(`/api/queue/${jobId}`, { method: 'DELETE' });
      fetchQueue();
    } catch (e) {
      alert("Error: " + e.message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Pending Publishing Queue</h1>
          <p className="text-slate-400 text-sm mt-1">
            Persistent content pipeline ready for autonomous execution. Guarded by idempotency tokens to prevent accidental duplicates.
          </p>
        </div>
        <button
          onClick={fetchQueue}
          className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
        >
          <RefreshCw size={16} />
        </button>
      </div>

      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-slate-500 text-sm">Loading queue...</div>
        ) : queue.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            The publishing queue is currently empty. Generated content will appear here ahead of scheduled times.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-900/80 text-xs text-slate-400 uppercase font-semibold border-b border-slate-800">
                <tr>
                  <th className="p-4">Type</th>
                  <th className="p-4">Title & Context</th>
                  <th className="p-4">Scheduled For</th>
                  <th className="p-4">Priority</th>
                  <th className="p-4">Retries</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {queue.map((item) => {
                  const dt = new Date(item.scheduled_for);
                  const content = item.content || {};

                  return (
                    <tr key={item.id} className="hover:bg-slate-900/40 transition">
                      <td className="p-4">
                        <span className="px-2.5 py-1 rounded-md bg-purple-950 text-purple-300 font-mono text-xs font-bold border border-purple-800">
                          {content.content_type || 'POST'}
                        </span>
                      </td>
                      <td className="p-4 max-w-xs">
                        <div className="font-semibold text-white truncate">{content.title || 'Untitled'}</div>
                        <div className="text-xs text-slate-400 truncate mt-0.5">{content.caption?.slice(0, 50)}...</div>
                      </td>
                      <td className="p-4 text-xs font-mono text-slate-300 whitespace-nowrap">
                        {dt.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })} IST
                      </td>
                      <td className="p-4 text-xs font-semibold text-slate-400">P{item.priority}</td>
                      <td className="p-4 text-xs font-semibold text-slate-400">{item.retry_count} / 3</td>
                      <td className="p-4 text-right space-x-2 whitespace-nowrap">
                        <button
                          onClick={() => handlePublishNow(item.id)}
                          disabled={actionId === item.id}
                          className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold inline-flex items-center gap-1 shadow transition"
                        >
                          <Send size={12} /> {actionId === item.id ? 'Publishing...' : 'Publish Now'}
                        </button>
                        <button
                          onClick={() => handleCancel(item.id)}
                          className="px-2.5 py-1.5 rounded-lg bg-red-950/60 hover:bg-red-900/80 text-red-400 text-xs font-bold inline-flex items-center transition"
                        >
                          <Trash2 size={13} />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
