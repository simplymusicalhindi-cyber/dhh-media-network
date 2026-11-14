import React, { useState, useEffect } from 'react';
import { BookOpen, RefreshCw, Download, CheckCircle } from 'lucide-react';

export default function StoryStudioView() {
  const [storyType, setStoryType] = useState('GUESS_THE_RAPPER');
  const [title, setTitle] = useState('GUESS THE DHH RAPPER 🔍');
  const [clue, setClue] = useState("Bars: 'Kaanch ke ghar mein baith ke, ye phek rahe patthar'\nKnown for: Multi-syllabic schemes & lyrical dominance.");
  const [options, setOptions] = useState(['A) KR$NA', 'B) Karma', 'C) Seedhe Maut', 'D) Brodha V']);
  const [callToAction, setCallToAction] = useState('Reply with your answer to test your DHH IQ! 🧠');
  const [presets, setPresets] = useState([]);
  const [renderedStory, setRenderedStory] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch('/api/stories/presets')
      .then(res => res.json())
      .then(data => setPresets(data || []))
      .catch(console.error);
  }, []);

  const handleRender = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/stories/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          story_type: storyType,
          title,
          clue,
          options,
          call_to_action: callToAction
        })
      });
      if (res.ok) {
        const json = await res.json();
        setRenderedStory(json.result);
      }
    } catch (e) {
      alert("Story render failed: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (p) => {
    setStoryType(p.type);
    setTitle(p.title);
    setClue(p.clue);
    setOptions(p.options || []);
    setCallToAction(p.call_to_action || '');
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h1 className="text-2xl font-bold text-white">Interactive Story Studio (9:16)</h1>
        <p className="text-slate-400 text-sm mt-1">
          Generate daily 1080x1920 interactive Story cards designed to stimulate fan DMs, quiz answers, and high profile retention.
        </p>

        {presets.length > 0 && (
          <div className="flex items-center gap-3 mt-4">
            <span className="text-xs text-slate-400 font-semibold">PRESET TEMPLATES:</span>
            <div className="flex flex-wrap gap-2">
              {presets.map((p, i) => (
                <button
                  key={i}
                  onClick={() => loadPreset(p)}
                  className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-medium text-emerald-300 border border-slate-700 transition"
                >
                  {p.title}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Editor */}
        <div className="lg:col-span-7 bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white">Story Card Elements</h2>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">STORY TITLE</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">CLUE / BARS / TRIVIA PROMPT</label>
            <textarea
              rows={3}
              value={clue}
              onChange={(e) => setClue(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
            />
          </div>

          <div className="space-y-2">
            <label className="block text-xs font-semibold text-slate-400">CHOICE OPTIONS / INTERACTIVE BADGES</label>
            {options.map((opt, i) => (
              <input
                key={i}
                type="text"
                value={opt}
                onChange={(e) => {
                  const copy = [...options];
                  copy[i] = e.target.value;
                  setOptions(copy);
                }}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs text-white"
              />
            ))}
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">CALL TO ACTION (BOTTOM PROMPT)</label>
            <input
              type="text"
              value={callToAction}
              onChange={(e) => setCallToAction(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-emerald-300 font-bold"
            />
          </div>

          <div className="pt-3">
            <button
              onClick={handleRender}
              disabled={loading}
              className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-emerald-600/30 flex items-center justify-center gap-2 transition"
            >
              <RefreshCw size={18} className={loading ? 'animate-spin' : ''} />
              {loading ? 'Rendering 1080x1920 Story...' : 'Render High-Res Story (PNG)'}
            </button>
          </div>
        </div>

        {/* Preview */}
        <div className="lg:col-span-5 bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-col items-center justify-center">
          <h2 className="text-lg font-bold text-white mb-4 self-start">9:16 Story Preview</h2>

          {renderedStory ? (
            <div className="space-y-4 w-full flex flex-col items-center">
              <div className="w-60 aspect-[9/16] rounded-2xl overflow-hidden border-2 border-slate-700 shadow-2xl bg-black">
                <img
                  src={`/media/stories/${renderedStory.file_name}`}
                  alt="Rendered Story"
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="text-center text-xs text-slate-400 space-y-1">
                <div>Format: 1080x1920 (9:16) • Safe Zones Included</div>
                <a
                  href={`/media/stories/${renderedStory.file_name}`}
                  download={renderedStory.file_name}
                  className="inline-flex items-center gap-1 text-emerald-400 font-bold hover:underline mt-2"
                >
                  <Download size={14} /> Download PNG
                </a>
              </div>
            </div>
          ) : (
            <div className="w-60 aspect-[9/16] border-2 border-dashed border-slate-800 rounded-2xl flex flex-col items-center justify-center text-slate-500 text-xs p-4 text-center">
              <BookOpen size={36} className="mb-2 text-slate-600" />
              <span>Click "Render High-Res Story" to generate 9:16 vertical graphic</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
