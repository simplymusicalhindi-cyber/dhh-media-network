import React, { useState, useEffect } from 'react';
import { Cpu, CheckCircle2, AlertTriangle, RefreshCw, Send } from 'lucide-react';

export default function AISettingsView() {
  const [status, setStatus] = useState(null);
  const [baseUrl, setBaseUrl] = useState('http://127.0.0.1:11434');
  const [model, setModel] = useState('llama3:latest');
  const [minQuality, setMinQuality] = useState(7.5);
  const [testPrompt, setTestPrompt] = useState('Seedhe Maut TBSM vibe meme');
  const [testResult, setTestResult] = useState(null);
  const [testing, setTesting] = useState(false);
  const [saving, setSaving] = useState(false);

  const fetchStatus = async () => {
    try {
      const res = await fetch('/api/ai/status');
      if (res.ok) {
        const json = await res.json();
        setStatus(json);
        if (json.config) {
          setBaseUrl(json.config.base_url);
          setModel(json.config.model);
          setMinQuality(json.config.min_quality_score);
        }
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const handleSaveConfig = async () => {
    setSaving(true);
    try {
      const res = await fetch('/api/ai/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ollama_base_url: baseUrl,
          ollama_model: model,
          min_quality_score: parseFloat(minQuality)
        })
      });
      if (res.ok) {
        alert("AI Settings updated successfully!");
        fetchStatus();
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setSaving(false);
    }
  };

  const handleTestInference = async () => {
    setTesting(true);
    setTestResult(null);
    try {
      const res = await fetch('/api/ai/test-inference', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: testPrompt })
      });
      if (res.ok) {
        const json = await res.json();
        setTestResult(json.result);
      }
    } catch (e) {
      alert("Test failed: " + e.message);
    } finally {
      setTesting(false);
    }
  };

  const isOllamaOnline = status?.ollama?.available;

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h1 className="text-2xl font-bold text-white">Local AI & Ollama Configuration</h1>
        <p className="text-slate-400 text-sm mt-1">
          Local-first architecture. Uses local Ollama LLMs when installed, or seamlessly falls back to the autonomous DHH cultural knowledge template engine.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Connection & Configuration */}
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Cpu size={18} className="text-purple-400" /> Local Daemon Status
            </h2>
            <button onClick={fetchStatus} className="p-1.5 rounded-lg bg-slate-800 text-slate-400 hover:text-white">
              <RefreshCw size={14} />
            </button>
          </div>

          <div className={`p-4 rounded-xl border flex items-center gap-3 ${
            isOllamaOnline ? 'bg-emerald-950/40 border-emerald-800 text-emerald-400' : 'bg-amber-950/40 border-amber-800 text-amber-300'
          }`}>
            {isOllamaOnline ? <CheckCircle2 size={24} /> : <AlertTriangle size={24} />}
            <div className="text-xs">
              <div className="font-bold">{isOllamaOnline ? 'Ollama Daemon Connected Locally' : 'Ollama Daemon Offline'}</div>
              <div className="mt-0.5 opacity-90">{status?.ollama?.message || 'Checking status...'}</div>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1.5">OLLAMA BASE URL</label>
              <input
                type="text"
                value={baseUrl}
                onChange={(e) => setBaseUrl(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1.5">MODEL NAME</label>
              <input
                type="text"
                value={model}
                onChange={(e) => setModel(e.target.value)}
                placeholder="e.g. llama3:latest, mistral, qwen2.5"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1.5">MINIMUM QUALITY THRESHOLD (1-10)</label>
              <input
                type="number"
                step="0.1"
                min="5"
                max="10"
                value={minQuality}
                onChange={(e) => setMinQuality(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
              />
            </div>

            <button
              onClick={handleSaveConfig}
              disabled={saving}
              className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 rounded-xl shadow-lg shadow-purple-600/30 text-xs transition"
            >
              {saving ? 'Saving...' : 'Save AI Configuration'}
            </button>
          </div>
        </div>

        {/* Prompt Test Bench */}
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Send size={18} className="text-purple-400" /> Prompt & Generation Test Bench
          </h2>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">TEST SEED TOPIC</label>
            <div className="flex gap-2">
              <input
                type="text"
                value={testPrompt}
                onChange={(e) => setTestPrompt(e.target.value)}
                className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white"
              />
              <button
                onClick={handleTestInference}
                disabled={testing}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-xl text-xs transition whitespace-nowrap"
              >
                {testing ? 'Inference...' : 'Test Run'}
              </button>
            </div>
          </div>

          {testResult ? (
            <div className="p-4 bg-slate-900/90 border border-slate-800 rounded-xl space-y-2 text-xs">
              <div className="flex justify-between items-center text-slate-400">
                <span>Source: <strong className="text-purple-300">{testResult.source}</strong></span>
                <span className="font-bold text-emerald-400">Score: {testResult.quality_score}/10</span>
              </div>
              <div className="font-bold text-white text-sm">💡 {testResult.hook}</div>
              <p className="text-slate-300 whitespace-pre-wrap">{testResult.top_text}</p>
              <p className="text-amber-300 font-semibold">{testResult.bottom_text}</p>
              {testResult.punchline && <p className="text-slate-400 italic">Punchline: {testResult.punchline}</p>}
            </div>
          ) : (
            <div className="h-64 border-2 border-dashed border-slate-800 rounded-xl flex items-center justify-center text-slate-500 text-xs">
              Run test inference to inspect JSON output structure
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
