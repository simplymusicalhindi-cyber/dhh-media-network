import React, { useState, useEffect } from 'react';
import { Search, Hash, Sparkles, UserCheck, Copy, Check } from 'lucide-react';

export default function SEOManagerView() {
  const [hook, setHook] = useState('Why Delhi underground rap hits harder than corporate labels');
  const [body, setBody] = useState('Raw production, hunger in the booth, and zero filter on the lyrics.');
  const [cta, setCta] = useState('Which underground track is on repeat for you right now? Drop names below! 👇');
  const [category, setCategory] = useState('UNDERGROUND');
  const [optimized, setOptimized] = useState(null);
  const [keywords, setKeywords] = useState({ primary: [], clusters: {} });
  const [bios, setBios] = useState([]);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetch('/api/seo/keywords')
      .then(res => res.json())
      .then(data => setKeywords(data || { primary: [], clusters: {} }))
      .catch(console.error);

    fetch('/api/seo/bios')
      .then(res => res.json())
      .then(data => setBios(data || []))
      .catch(console.error);
  }, []);

  const handleOptimize = async () => {
    try {
      const res = await fetch('/api/seo/optimize-caption', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hook, body, cta, category })
      });
      if (res.ok) {
        const json = await res.json();
        setOptimized(json);
      }
    } catch (e) {
      alert("Error: " + e.message);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h1 className="text-2xl font-bold text-white">SEO & Discoverability Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Optimize captions for the Instagram explore algorithm, avoid hashtag stuffing (strict 3-5 high-intent tags), and polish profile discovery.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Caption Optimizer */}
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles size={18} className="text-purple-400" /> Caption & Hook Optimizer
          </h2>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">OPENING HOOK (FIRST 125 CHARACTERS)</label>
            <input
              type="text"
              value={hook}
              onChange={(e) => setHook(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">BODY STORY & RELATABLE CONTEXT</label>
            <textarea
              rows={3}
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">CALL TO ACTION (COMMENT DRIVER)</label>
            <input
              type="text"
              value={cta}
              onChange={(e) => setCta(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">KEYWORD CLUSTER CATEGORY</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            >
              <option value="PRODUCER">Producer & Beatmaker Cluster</option>
              <option value="UNDERGROUND">Underground Hip-Hop Cluster</option>
              <option value="MAINSTREAM_DHH">Mainstream DHH & Artist Tropes</option>
              <option value="MEMES_HUMOR">Viral Memes & Relatable Jokes</option>
              <option value="STUDIO_LIFE">Studio Engineering & Vocal Mix</option>
            </select>
          </div>

          <button
            onClick={handleOptimize}
            className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 rounded-xl shadow-lg shadow-purple-600/30 transition text-sm"
          >
            Run SEO Optimization
          </button>

          {optimized && (
            <div className="p-4 bg-slate-900/80 border border-slate-700 rounded-xl space-y-3 mt-4">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-emerald-400">SEO Score: {optimized.seo_score}/10</span>
                <button
                  onClick={() => copyToClipboard(optimized.caption)}
                  className="text-purple-400 hover:underline flex items-center gap-1 font-semibold"
                >
                  {copied ? <Check size={14} /> : <Copy size={14} />} {copied ? 'Copied' : 'Copy Full Caption'}
                </button>
              </div>
              <p className="text-xs text-slate-200 whitespace-pre-wrap font-mono leading-relaxed bg-black/40 p-3 rounded-lg border border-slate-800">
                {optimized.caption}
              </p>
            </div>
          )}
        </div>

        {/* Profile Bios & Keywords */}
        <div className="space-y-6">
          <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <UserCheck size={18} className="text-purple-400" /> High-Discovery Instagram Bios
            </h2>
            <div className="space-y-3">
              {bios.map((b) => (
                <div key={b.id} className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white text-sm">@{b.username_suggestion}</span>
                    <span className="text-[11px] font-mono text-purple-400 bg-purple-950/60 px-2 py-0.5 rounded border border-purple-800">
                      {b.category_tag}
                    </span>
                  </div>
                  <div className="text-xs font-semibold text-slate-300">{b.display_name}</div>
                  <p className="text-xs text-slate-300 whitespace-pre-wrap bg-black/30 p-2.5 rounded-lg border border-slate-800/80">
                    {b.bio_text}
                  </p>
                  <div className="text-[11px] text-slate-500 italic">Strategy: {b.strategy_notes}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
            <h2 className="text-lg font-bold text-white flex items-center gap-2 mb-3">
              <Hash size={18} className="text-purple-400" /> Tracked DHH Keywords
            </h2>
            <div className="flex flex-wrap gap-2">
              {keywords.primary.map((kw, i) => (
                <span key={i} className="px-3 py-1 rounded-lg bg-slate-800 text-xs font-semibold text-slate-300 border border-slate-700">
                  {kw}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
