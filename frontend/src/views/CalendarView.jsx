import React, { useState, useEffect } from 'react';
import { Calendar as CalendarIcon, Clock, Send, Trash2, CheckCircle2, AlertTriangle, RefreshCw } from 'lucide-react';

export default function CalendarView() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('ALL');

  const fetchCalendar = async () => {
    try {
      const res = await fetch('/api/queue/calendar');
      if (res.ok) {
        const json = await res.json();
        setEvents(json || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCalendar();
  }, []);

  const filteredEvents = events.filter(e => {
    if (filterType === 'ALL') return true;
    return e.content_type === filterType;
  });

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Publishing Calendar & Timeline</h1>
          <p className="text-slate-400 text-sm mt-1">
            Visual distribution of 10 image posts, 5 reels, and daily stories across peak engagement windows in India (IST).
          </p>
        </div>

        <div className="flex items-center gap-2">
          {['ALL', 'IMAGE', 'REEL', 'STORY'].map((t) => (
            <button
              key={t}
              onClick={() => setFilterType(t)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition ${
                filterType === t
                  ? 'bg-purple-600 text-white'
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
            >
              {t === 'ALL' ? 'All Formats' : t}
            </button>
          ))}
          <button
            onClick={fetchCalendar}
            className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          >
            <RefreshCw size={16} />
          </button>
        </div>
      </div>

      {/* Timeline List / Grid */}
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4">Scheduled & Published Activity</h2>

        {loading ? (
          <div className="text-slate-500 text-sm py-8 text-center">Loading timeline events...</div>
        ) : filteredEvents.length === 0 ? (
          <div className="text-slate-500 text-sm py-12 text-center border-2 border-dashed border-slate-800 rounded-xl">
            No events found for this filter. Use Content Generator to queue items.
          </div>
        ) : (
          <div className="space-y-3">
            {filteredEvents.map((evt) => {
              const dt = new Date(evt.start);
              const isPublished = evt.status === 'PUBLISHED';
              const isFailed = evt.status === 'FAILED';

              return (
                <div
                  key={evt.id}
                  className={`p-4 rounded-xl border flex items-center justify-between gap-4 transition ${
                    isPublished
                      ? 'bg-emerald-950/20 border-emerald-900/40'
                      : isFailed
                      ? 'bg-red-950/20 border-red-900/40'
                      : 'bg-slate-900/60 border-slate-800'
                  }`}
                >
                  <div className="flex items-center gap-3.5">
                    <div className={`p-2.5 rounded-xl ${
                      isPublished ? 'bg-emerald-900/40 text-emerald-400' : isFailed ? 'bg-red-900/40 text-red-400' : 'bg-purple-900/40 text-purple-400'
                    }`}>
                      {isPublished ? <CheckCircle2 size={20} /> : isFailed ? <AlertTriangle size={20} /> : <Clock size={20} />}
                    </div>

                    <div>
                      <div className="text-sm font-bold text-white">{evt.title}</div>
                      <div className="text-xs text-slate-400 flex items-center gap-2 mt-0.5">
                        <span>{dt.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
                        <span>•</span>
                        <span>{dt.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })} IST</span>
                        <span>•</span>
                        <span className="uppercase text-[10px] font-mono tracking-wider font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                          {evt.content_type}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      isPublished
                        ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                        : isFailed
                        ? 'bg-red-950 text-red-400 border border-red-800'
                        : 'bg-blue-950 text-blue-300 border border-blue-800'
                    }`}>
                      {evt.status}
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
