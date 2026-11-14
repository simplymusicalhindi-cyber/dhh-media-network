import React, { useState } from 'react';
import { Sparkles, Image as ImageIcon, Film, BookOpen, Send, Clock, Check, AlertCircle } from 'lucide-react';

export default function ContentGeneratorView({ setActiveTab }) {
  const [activeType, setActiveType] = useState('MEME');
  const [category, setCategory] = useState('PRODUCER_MEME');
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [generatedResult, setGeneratedResult] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  const categories = [
    { id: 'PRODUCER_MEME', name: 'Producer Struggles (FL Studio, 808s, Shoutouts)' },
    { id: 'RELATABLE_MEME', name: 'Relatable DHH Fan Moments (Metro commute, Spotify)' },
    { id: 'RAPPER_MEME', name: 'Rapper Stereotypes & Starter Packs' },
    { id: 'STUDIO_LIFE', name: 'Studio Life & 4 AM Vocal Mixes' },
    { id: 'FAN_WARS', name: 'Fan Wars & Lyrical Rhyme Debates (KR$NA, SM)' },
    { id: 'POV_MEMES', name: 'POV DHH Comedy' },
    { id: 'YOUTH_HUMOUR', name: 'Indian Parents vs Trap Music' },
    { id: 'INDEPENDENT_STRUGGLE', name: 'Zero-Budget Independent Grind' }
  ];

  const handleGenerate = async (autoEnqueue = true) => {
    setLoading(true);
    setSuccessMessage('');
    setGeneratedResult(null);

    try {
      let endpoint = '/api/content/generate-meme';
      let body = { category, topic: topic.trim() || undefined, auto_enqueue: autoEnqueue };

      if (activeType === 'REEL') {
        endpoint = '/api/content/generate-reel';
        body = { topic: topic.trim() || undefined, auto_enqueue: autoEnqueue };
      } else if (activeType === 'STORY') {
        endpoint = '/api/content/generate-story';
        body = { auto_enqueue: autoEnqueue };
      }

      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      if (res.ok) {
        const json = await res.json();
        setGeneratedResult(json);
        setSuccessMessage(autoEnqueue ? 'Content generated and added to Publishing Queue!' : 'Content generated successfully!');
      } else {
        alert('Generation failed');
      }
    } catch (e) {
      alert('Error: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h1 className="text-2xl font-bold text-white">AI Content Generation Studio</h1>
        <p className="text-slate-400 text-sm mt-1">
          Generate authentic Desi Hip-Hop memes, vertical 9:16 Reels, and interactive Stories with culture-rich captions & SEO.
        </p>

        {/* Format Selector */}
        <div className="flex items-center gap-3 mt-6">
          <button
            onClick={() => setActiveType('MEME')}
            className={`px-5 py-2.5 rounded-xl font-bold text-sm flex items-center gap-2 transition ${
              activeType === 'MEME'
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/30'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <ImageIcon size={18} /> 1:1 Meme Post
          </button>

          <button
            onClick={() => setActiveType('REEL')}
            className={`px-5 py-2.5 rounded-xl font-bold text-sm flex items-center gap-2 transition ${
              activeType === 'REEL'
                ? 'bg-amber-600 text-white shadow-lg shadow-amber-600/30'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <Film size={18} /> 9:16 Video Reel
          </button>

          <button
            onClick={() => setActiveType('STORY')}
            className={`px-5 py-2.5 rounded-xl font-bold text-sm flex items-center gap-2 transition ${
              activeType === 'STORY'
                ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            <BookOpen size={18} /> 9:16 Interactive Story
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Parameters */}
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-5">
          <h2 className="text-lg font-bold text-white">Generation Parameters</h2>

          {activeType === 'MEME' && (
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-2">CONTENT CATEGORY</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-purple-500"
              >
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-2">
              OPTIONAL TOPIC SEED / ARTIST / SCENE (Leave empty for autonomous research discovery)
            </label>
            <input
              type="text"
              placeholder="e.g. KR$NA vs Seedhe Maut rhyme schemes, or 808 distortion in Delhi"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-purple-500"
            />
          </div>

          <div className="pt-4 border-t border-slate-800 flex items-center gap-3">
            <button
              onClick={() => handleGenerate(true)}
              disabled={loading}
              className="flex-1 bg-purple-600 hover:bg-purple-500 text-white font-bold p-3.5 rounded-xl shadow-lg shadow-purple-600/25 flex items-center justify-center gap-2 transition"
            >
              <Sparkles size={18} />
              {loading ? 'Synthesizing Culture...' : 'Generate & Enqueue Post'}
            </button>

            <button
              onClick={() => handleGenerate(false)}
              disabled={loading}
              className="px-4 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-semibold transition"
            >
              Draft Only
            </button>
          </div>

          {successMessage && (
            <div className="p-3 bg-emerald-950/60 border border-emerald-700/60 rounded-xl text-emerald-400 text-sm flex items-center gap-2">
              <Check size={16} /> {successMessage}
            </div>
          )}
        </div>

        {/* Live Preview Panel */}
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
          <h2 className="text-lg font-bold text-white mb-4">Preview & Quality Output</h2>

          {generatedResult ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span>Title: <strong className="text-white">{generatedResult.title}</strong></span>
                <span className="px-2.5 py-1 rounded-full bg-purple-900/60 text-purple-300 font-bold">
                  Quality Score: {generatedResult.quality_score}/10
                </span>
              </div>

              {/* Media Preview */}
              {activeType === 'REEL' ? (
                <div className="aspect-[9/16] max-h-96 mx-auto bg-black rounded-xl overflow-hidden border border-slate-800">
                  <video
                    src={`/media/reels/${generatedResult.media_path.split('\\').pop()}`}
                    controls
                    className="w-full h-full object-contain"
                  />
                </div>
              ) : (
                <div className="max-h-80 mx-auto rounded-xl overflow-hidden border border-slate-800">
                  <img
                    src={`/media/${activeType === 'MEME' ? 'memes' : 'stories'}/${generatedResult.media_path.split('\\').pop()}`}
                    alt="Generated Preview"
                    className="w-full h-full object-contain"
                  />
                </div>
              )}

              {/* Caption Preview */}
              {generatedResult.caption && (
                <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 whitespace-pre-wrap max-h-36 overflow-y-auto">
                  {generatedResult.caption}
                </div>
              )}

              <div className="flex items-center gap-2 pt-2">
                <button
                  onClick={() => setActiveTab('queue')}
                  className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold py-2.5 rounded-xl transition text-center"
                >
                  View in Publishing Queue →
                </button>
              </div>
            </div>
          ) : (
            <div className="h-72 border-2 border-dashed border-slate-800 rounded-xl flex flex-col items-center justify-center text-slate-500 text-sm">
              <Sparkles size={32} className="mb-2 text-slate-600" />
              <span>Select parameters and click Generate to preview here.</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
