import React, { useState, useEffect } from 'react';
import { Film, Play, Sparkles, RefreshCw, Volume2, ShieldCheck, Download } from 'lucide-react';

export default function ReelsStudioView() {
  const [title, setTitle] = useState('Types of Rappers in DHH Studio Sessions');
  const [hook, setHook] = useState('Every DHH studio session has these 3 characters 💀');
  const [scenes, setScenes] = useState([
    { duration: 3, text: "Character 1: The 'Bhai AutoTune thoda aur badha de' guy" },
    { duration: 3, text: "Character 2: The lyricist writing 4-syllable rhymes while ignoring the beat tempo" },
    { duration: 3, text: "Character 3: The friend who came for free AC and eating samosas" }
  ]);
  const [punchline, setPunchline] = useState('Tag your friend who is 100% Character 3 😂👇');
  const [presets, setPresets] = useState([]);
  const [renderedReel, setRenderedReel] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch('/api/reels/presets')
      .then(res => res.json())
      .then(data => setPresets(data || []))
      .catch(console.error);
  }, []);

  const handleRender = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/reels/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          hook,
          scenes,
          punchline
        })
      });
      if (res.ok) {
        const json = await res.json();
        setRenderedReel(json.result);
      }
    } catch (e) {
      alert("Reel render failed: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (p) => {
    setTitle(p.title);
    setHook(p.hook);
    setScenes(p.scenes || []);
    setPunchline(p.punchline || '');
  };

  const updateSceneText = (idx, text) => {
    const updated = [...scenes];
    updated[idx].text = text;
    setScenes(updated);
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h1 className="text-2xl font-bold text-white">Reels Production Studio (9:16 Vertical)</h1>
        <p className="text-slate-400 text-sm mt-1">
          Automated vertical video pipeline powered by FFmpeg. Combines scene pacing, safe margins, high-CTR covers, and royalty-free 808 audio beats.
        </p>

        {presets.length > 0 && (
          <div className="flex items-center gap-3 mt-4">
            <span className="text-xs text-slate-400 font-semibold">LOAD REEL PRESET:</span>
            <div className="flex flex-wrap gap-2">
              {presets.map((p, i) => (
                <button
                  key={i}
                  onClick={() => loadPreset(p)}
                  className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-amber-300 border border-slate-700 transition"
                >
                  {p.title}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Script & Scenes Editor */}
        <div className="lg:col-span-7 bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white">Script & Scene Progression</h2>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">REEL TITLE (TOP BADGE)</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">OPENING HOOK (FIRST 3 SECONDS)</label>
            <input
              type="text"
              value={hook}
              onChange={(e) => setHook(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div className="space-y-3 pt-2">
            <label className="block text-xs font-semibold text-slate-400">SCENE-BY-SCENE SLIDES</label>
            {scenes.map((s, idx) => (
              <div key={idx} className="p-3.5 bg-slate-900/80 border border-slate-800 rounded-xl space-y-1.5">
                <div className="flex items-center justify-between text-xs text-amber-400 font-bold">
                  <span>Part {idx + 1} ({s.duration}s)</span>
                  <span className="text-slate-500 font-mono text-[11px]">Safe Area Compliant</span>
                </div>
                <input
                  type="text"
                  value={s.text}
                  onChange={(e) => updateSceneText(idx, e.target.value)}
                  className="w-full bg-slate-800/80 border border-slate-700 rounded-lg p-2.5 text-xs text-white"
                />
              </div>
            ))}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">FINAL VERDICT / PUNCHLINE</label>
            <input
              type="text"
              value={punchline}
              onChange={(e) => setPunchline(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-amber-300 font-bold"
            />
          </div>

          <div className="pt-3">
            <button
              onClick={handleRender}
              disabled={loading}
              className="w-full bg-amber-600 hover:bg-amber-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-amber-600/30 flex items-center justify-center gap-2 transition"
            >
              <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
              {loading ? 'Compiling Video via FFmpeg...' : 'Render 9:16 Video Reel (MP4)'}
            </button>
          </div>
        </div>

        {/* Video Player & Cover Preview */}
        <div className="lg:col-span-5 bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-col items-center justify-center">
          <h2 className="text-lg font-bold text-white mb-4 self-start">9:16 Video Player Preview</h2>

          {renderedReel ? (
            <div className="space-y-4 w-full flex flex-col items-center">
              <div className="w-64 aspect-[9/16] rounded-2xl overflow-hidden border-2 border-slate-700 shadow-2xl bg-black relative">
                <video
                  src={`/media/reels/${renderedReel.video_path.split('\\').pop()}`}
                  controls
                  autoPlay
                  loop
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="text-center text-xs text-slate-400 space-y-1">
                <div>Duration: {renderedReel.duration}s • {renderedReel.width}x{renderedReel.height}</div>
                <div>Audio: AAC 192k 808 Trap Synthesizer • File Size: {Math.round(renderedReel.file_size / 1024)} KB</div>
                <a
                  href={`/media/reels/${renderedReel.video_path.split('\\').pop()}`}
                  download="dhh_reel.mp4"
                  className="inline-flex items-center gap-1 text-amber-400 font-bold hover:underline mt-2"
                >
                  <Download size={14} /> Download MP4
                </a>
              </div>
            </div>
          ) : (
            <div className="w-64 aspect-[9/16] border-2 border-dashed border-slate-800 rounded-2xl flex flex-col items-center justify-center text-slate-500 text-xs p-4 text-center">
              <Film size={36} className="mb-2 text-slate-600" />
              <span>Click "Render 9:16 Video Reel" to assemble with FFmpeg and preview playback</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
