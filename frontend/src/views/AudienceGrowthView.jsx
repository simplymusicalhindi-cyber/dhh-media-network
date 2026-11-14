import React, { useState, useEffect } from 'react';
import { Compass, Flame, Clock, Users, Send, Check } from 'lucide-react';

export default function AudienceGrowthView() {
  const [topics, setTopics] = useState([]);
  const [artists, setArtists] = useState([]);
  const [windows, setWindows] = useState([]);
  const [drafts, setDrafts] = useState([]);
  const [selectedArtist, setSelectedArtist] = useState('');
  const [artistHandle, setArtistHandle] = useState('');
  const [loadingDraft, setLoadingDraft] = useState(false);

  useEffect(() => {
    fetch('/api/growth/topics')
      .then(res => res.json())
      .then(data => setTopics(data || []))
      .catch(console.error);

    fetch('/api/growth/artists')
      .then(res => res.json())
      .then(data => setArtists(data || []))
      .catch(console.error);

    fetch('/api/growth/posting-windows')
      .then(res => res.json())
      .then(data => setWindows(data || []))
      .catch(console.error);

    fetch('/api/growth/outreach-drafts')
      .then(res => res.json())
      .then(data => setDrafts(data || []))
      .catch(console.error);
  }, []);

  const handleCreateOutreach = async () => {
    if (!selectedArtist) return;
    setLoadingDraft(true);
    try {
      const res = await fetch('/api/growth/outreach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          artist_name: selectedArtist,
          artist_handle: artistHandle || `@${selectedArtist.toLowerCase().replace(/[^a-z0-9]/g, '')}`
        })
      });
      if (res.ok) {
        fetch('/api/growth/outreach-drafts')
          .then(r => r.json())
          .then(d => setDrafts(d || []));
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setLoadingDraft(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h1 className="text-2xl font-bold text-white">Organic Audience Growth Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Trend discovery radar, optimal posting windows for Indian hip-hop audiences, and personalized creator outreach drafts.
        </p>
      </div>

      {/* Optimal Posting Windows */}
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Clock size={18} className="text-amber-400" /> Optimal Publishing Windows (India Standard Time)
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {windows.map((w, i) => (
            <div key={i} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
              <div className="text-xs font-bold text-amber-300 font-mono">{w.window}</div>
              <p className="text-xs text-slate-300">{w.reason}</p>
              <div className="flex flex-wrap gap-1 mt-2">
                {w.target_formats.map((f, fi) => (
                  <span key={fi} className="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400 font-semibold">
                    {f}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Topic Radar */}
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Flame size={18} className="text-rose-400" /> DHH Topic & Trend Radar
          </h2>
          <div className="space-y-3">
            {topics.map((t) => (
              <div key={t.id} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-white">{t.topic_name}</span>
                  <span className="px-2 py-0.5 rounded bg-purple-950 text-purple-300 font-mono text-[10px] font-bold">
                    Relevance: {t.relevance_score}/10
                  </span>
                </div>
                <p className="text-xs text-slate-400">{t.summary}</p>
                <div className="text-[10px] text-slate-500 font-mono">Source: {t.source} • Category: {t.category}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Collab Outreach */}
        <div className="space-y-6">
          <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Users size={18} className="text-purple-400" /> Creator & Artist Collab Pitch Generator
            </h2>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">SELECT ARTIST / PRODUCER</label>
                <select
                  value={selectedArtist}
                  onChange={(e) => {
                    setSelectedArtist(e.target.value);
                    const a = artists.find(ar => ar.name === e.target.value);
                    if (a) setArtistHandle(`@${a.name.toLowerCase().replace(/[^a-z0-9]/g, '')}`);
                  }}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-xs text-white"
                >
                  <option value="">Choose an artist...</option>
                  {artists.map((a) => (
                    <option key={a.id} value={a.name}>{a.name} ({a.scene} Scene)</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">INSTAGRAM HANDLE</label>
                <input
                  type="text"
                  value={artistHandle}
                  onChange={(e) => setArtistHandle(e.target.value)}
                  placeholder="@artist_handle"
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-xs text-white"
                />
              </div>

              <button
                onClick={handleCreateOutreach}
                disabled={loadingDraft || !selectedArtist}
                className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-2.5 rounded-xl text-xs transition shadow-lg shadow-purple-600/20"
              >
                {loadingDraft ? 'Generating Draft...' : 'Generate Collaboration Pitch'}
              </button>
            </div>

            {/* Generated Drafts */}
            <div className="space-y-3 pt-3">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Prepared Outreach Drafts (Manual Review)</h3>
              {drafts.slice(0, 3).map((d) => (
                <div key={d.id} className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between text-xs font-bold text-purple-300">
                    <span>{d.artist_name} ({d.artist_handle})</span>
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">{d.status}</span>
                  </div>
                  <p className="text-xs text-slate-200 bg-black/30 p-2.5 rounded-lg border border-slate-800/80 leading-relaxed">
                    {d.outreach_pitch}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
