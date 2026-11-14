import React, { useState, useEffect } from 'react';
import { Sliders, Save, Clock, ShieldAlert, Folder, Database } from 'lucide-react';

export default function GeneralSettingsView() {
  const [imageTarget, setImageTarget] = useState(10);
  const [reelsTarget, setReelsTarget] = useState(5);
  const [storiesTarget, setStoriesTarget] = useState(1);
  const [timezone, setTimezone] = useState('Asia/Kolkata');
  const [settingsData, setSettingsData] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetch('/api/settings')
      .then(res => res.json())
      .then(data => {
        setSettingsData(data);
        setImageTarget(data.daily_image_target || 10);
        setReelsTarget(data.daily_reels_target || 5);
        setStoriesTarget(data.daily_stories_target || 1);
        setTimezone(data.timezone || 'Asia/Kolkata');
      })
      .catch(console.error);
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      const res = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          daily_image_target: parseInt(imageTarget),
          daily_reels_target: parseInt(reelsTarget),
          daily_stories_target: parseInt(storiesTarget),
          timezone
        })
      });
      if (res.ok) {
        alert("Platform settings saved successfully!");
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h1 className="text-2xl font-bold text-white">General & Publishing Settings</h1>
        <p className="text-slate-400 text-sm mt-1">
          Configure daily publishing quotas, scheduler timezones, and system storage directories.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily Publishing Targets */}
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Sliders size={18} className="text-purple-400" /> Daily Autonomous Publishing Targets
          </h2>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">
              IMAGE & CAROUSEL POSTS PER DAY (INITIAL TARGET: 10)
            </label>
            <input
              type="number"
              min="1"
              max="30"
              value={imageTarget}
              onChange={(e) => setImageTarget(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">
              INSTAGRAM REELS PER DAY (INITIAL TARGET: 5)
            </label>
            <input
              type="number"
              min="1"
              max="20"
              value={reelsTarget}
              onChange={(e) => setReelsTarget(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">
              INSTAGRAM STORIES PER DAY (MINIMUM TARGET: 1)
            </label>
            <input
              type="number"
              min="1"
              max="15"
              value={storiesTarget}
              onChange={(e) => setStoriesTarget(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">
              SCHEDULER TIMEZONE
            </label>
            <input
              type="text"
              value={timezone}
              onChange={(e) => setTimezone(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white font-mono"
            />
          </div>

          <button
            onClick={handleSave}
            disabled={saving}
            className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-purple-600/30 text-xs transition flex items-center justify-center gap-2"
          >
            <Save size={16} />
            {saving ? 'Saving Settings...' : 'Save Publishing Quotas'}
          </button>
        </div>

        {/* Storage Paths & Host Information */}
        <div className="space-y-6">
          <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Folder size={18} className="text-purple-400" /> Storage & Host Environment
            </h2>

            <div className="space-y-3 text-xs">
              <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                <div className="font-bold text-slate-400">Media Storage Partition:</div>
                <div className="font-mono text-purple-300 break-all">{settingsData?.media_storage_path || 'backend/data/media'}</div>
              </div>

              <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                <div className="font-bold text-slate-400">Database Connection URL:</div>
                <div className="font-mono text-purple-300 break-all">{settingsData?.database_url || 'sqlite:///backend/data/dhh_media.db'}</div>
              </div>

              <div className="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1">
                <div className="font-bold text-slate-400">Host Server Access:</div>
                <div className="font-mono text-emerald-400">http://127.0.0.1:8787 (Localhost Restricted)</div>
              </div>
            </div>
          </div>

          <div className="bg-purple-950/20 border border-purple-800/40 rounded-2xl p-5 text-xs text-purple-300 space-y-2">
            <div className="font-bold text-white flex items-center gap-2">
              <span>⚡ Autonomous Reliability Policy</span>
            </div>
            <p className="leading-relaxed text-slate-300">
              The scheduler continuously runs in the background. If content quality or API permissions are insufficient, the engine will never force low-quality or duplicate publications to meet numerical targets.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
