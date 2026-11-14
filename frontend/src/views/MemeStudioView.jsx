import React, { useState, useEffect } from 'react';
import { Palette, Sparkles, Download, Layers, RefreshCw } from 'lucide-react';

export default function MemeStudioView() {
  const [template, setTemplate] = useState('TWEET_CARD_STYLE');
  const [hook, setHook] = useState('Producer life in DHH hits different 💀');
  const [bodyText, setBodyText] = useState("Rapper: 'Bhai beat fire hai, mix-master bhi karke de de na.'\n\nMe: 'Budget kitna hai?'\nRapper: 'Bhai pure DHH mein shoutout milega.'");
  const [punchline, setPunchline] = useState('Shoutout se FL Studio ka subscription nahi renew hota bhai.');
  const [category, setCategory] = useState('PRODUCER_MEME');
  const [presets, setPresets] = useState([]);
  const [renderedMeme, setRenderedMeme] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch('/api/memes/presets')
      .then(res => res.json())
      .then(data => setPresets(data || []))
      .catch(console.error);
  }, []);

  const handleRender = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/memes/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          template,
          hook,
          body_text: bodyText,
          punchline,
          category
        })
      });
      if (res.ok) {
        const json = await res.json();
        setRenderedMeme(json.result);
      }
    } catch (e) {
      alert("Render failed: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (p) => {
    setHook(p.hook);
    setBodyText(`${p.top_text}\n\n${p.bottom_text}`);
    setPunchline(p.punchline || '');
    setCategory(p.category || 'DHH_MEME');
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h1 className="text-2xl font-bold text-white">Meme Studio & Canvas</h1>
        <p className="text-slate-400 text-sm mt-1">
          Precision meme layout engine with Twitter/X dark aesthetic, high-contrast typography, and split comparison templates.
        </p>

        {/* Template Selector */}
        <div className="flex gap-3 mt-5">
          <button
            onClick={() => setTemplate('TWEET_CARD_STYLE')}
            className={`px-4 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 transition ${
              template === 'TWEET_CARD_STYLE'
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/30'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <Layers size={16} /> Twitter / X Dark Card (1:1)
          </button>

          <button
            onClick={() => setTemplate('SPLIT_COMPARISON')}
            className={`px-4 py-2.5 rounded-xl text-sm font-bold flex items-center gap-2 transition ${
              template === 'SPLIT_COMPARISON'
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/30'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <Palette size={16} /> Split Comparison (Plan vs Reality)
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Editor Form */}
        <div className="lg:col-span-7 bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white">Custom Typography & Layout</h2>
            {presets.length > 0 && (
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">Load Preset:</span>
                <select
                  onChange={(e) => {
                    const found = presets.find(p => p.hook === e.target.value);
                    if (found) loadPreset(found);
                  }}
                  className="bg-slate-900 border border-slate-700 text-xs text-purple-300 rounded-lg p-1.5 focus:outline-none"
                >
                  <option value="">Choose preset...</option>
                  {presets.map((p, i) => (
                    <option key={i} value={p.hook}>{p.category} - {p.hook.slice(0, 30)}...</option>
                  ))}
                </select>
              </div>
            )}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">CATEGORY BADGE</label>
            <input
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">HOOK (TITLE / FIRST LINE)</label>
            <input
              type="text"
              value={hook}
              onChange={(e) => setHook(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">
              BODY CONTENT {template === 'SPLIT_COMPARISON' && '(Separate top and bottom with ---)'}
            </label>
            <textarea
              rows={4}
              value={bodyText}
              onChange={(e) => setBodyText(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">PUNCHLINE FOOTER (HIGHLIGHTED)</label>
            <input
              type="text"
              value={punchline}
              onChange={(e) => setPunchline(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div className="pt-3">
            <button
              onClick={handleRender}
              disabled={loading}
              className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-purple-600/30 flex items-center justify-center gap-2 transition"
            >
              <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
              {loading ? 'Rendering 1080x1080...' : 'Render High-Res Meme'}
            </button>
          </div>
        </div>

        {/* Live Preview Canvas */}
        <div className="lg:col-span-5 bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-col items-center justify-center">
          <h2 className="text-lg font-bold text-white mb-4 self-start">Visual Output (1080x1080)</h2>
          {renderedMeme ? (
            <div className="space-y-4 w-full">
              <div className="rounded-xl overflow-hidden border border-slate-700 shadow-2xl bg-black">
                <img
                  src={`/media/memes/${renderedMeme.file_name}`}
                  alt="Rendered Meme"
                  className="w-full h-auto object-contain"
                />
              </div>
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span>Format: {renderedMeme.format} • {renderedMeme.width}x{renderedMeme.height}</span>
                <a
                  href={`/media/memes/${renderedMeme.file_name}`}
                  download={renderedMeme.file_name}
                  className="text-purple-400 font-bold hover:underline flex items-center gap-1"
                >
                  <Download size={14} /> Download PNG
                </a>
              </div>
            </div>
          ) : (
            <div className="w-full h-80 border-2 border-dashed border-slate-800 rounded-xl flex flex-col items-center justify-center text-slate-500 text-sm">
              <Palette size={32} className="mb-2 text-slate-600" />
              <span>Click "Render High-Res Meme" to generate preview</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
