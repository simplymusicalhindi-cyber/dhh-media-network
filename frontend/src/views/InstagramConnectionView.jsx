import React, { useState, useEffect } from 'react';
import { ShieldCheck, CheckCircle2, AlertTriangle, Key, ExternalLink, RefreshCw } from 'lucide-react';

export default function InstagramConnectionView() {
  const [data, setData] = useState(null);
  const [accessToken, setAccessToken] = useState('');
  const [accountId, setAccountId] = useState('');
  const [appId, setAppId] = useState('');
  const [appSecret, setAppSecret] = useState('');
  const [mockMode, setMockMode] = useState(true);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const fetchStatus = async () => {
    try {
      const res = await fetch('/api/instagram/status');
      if (res.ok) {
        const json = await res.json();
        setData(json);
        setMockMode(json.account?.mock_mode ?? true);
        setAccountId(json.account?.ig_user_id || '');
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const handleConnect = async () => {
    setSaving(true);
    try {
      const res = await fetch('/api/instagram/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          access_token: accessToken,
          ig_account_id: accountId,
          meta_app_id: appId,
          meta_app_secret: appSecret,
          mock_mode: mockMode
        })
      });
      if (res.ok) {
        alert("Instagram configuration saved successfully!");
        fetchStatus();
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setSaving(false);
    }
  };

  const handleToggleMock = async (enabled) => {
    setMockMode(enabled);
    try {
      await fetch(`/api/instagram/toggle-mock-mode?enabled=${enabled}`, { method: 'POST' });
      fetchStatus();
    } catch (e) {
      console.error(e);
    }
  };

  const live = data?.live_test || {};
  const wizard = data?.wizard_steps || [];

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h1 className="text-2xl font-bold text-white">Official Meta Instagram Integration</h1>
        <p className="text-slate-400 text-sm mt-1">
          Supports Instagram Professional & Business accounts via official Meta Graph API v21.0. Zero unofficial scrapers, zero bot logins.
        </p>
      </div>

      {/* Mode Indicator & Switch */}
      <div className={`p-5 rounded-2xl border flex flex-wrap items-center justify-between gap-4 ${
        mockMode ? 'bg-amber-950/30 border-amber-800 text-amber-300' : 'bg-emerald-950/30 border-emerald-800 text-emerald-300'
      }`}>
        <div className="flex items-center gap-3">
          <ShieldCheck size={28} />
          <div>
            <div className="text-base font-bold">
              {mockMode ? 'Simulation & Dry-Run Mode Active' : 'Live Meta Graph API Active'}
            </div>
            <div className="text-xs opacity-90">
              {mockMode
                ? 'All publishing endpoints, containers, insights & comment replies are faithfully emulated for 100% offline testing without risking real Instagram accounts.'
                : 'Publishing operations will execute on your connected Meta Instagram Business account.'}
            </div>
          </div>
        </div>

        <button
          onClick={() => handleToggleMock(!mockMode)}
          className="px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs font-bold text-white hover:bg-slate-800 transition"
        >
          Switch to {mockMode ? 'Live Mode' : 'Mock Simulation'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Credentials Form */}
        <div className="lg:col-span-7 bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Key size={18} className="text-purple-400" /> Meta Credentials & Token
          </h2>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">INSTAGRAM BUSINESS ACCOUNT ID</label>
            <input
              type="text"
              value={accountId}
              onChange={(e) => setAccountId(e.target.value)}
              placeholder="e.g. 17841400012345678"
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5">USER ACCESS TOKEN (LONG-LIVED / 60-DAY)</label>
            <input
              type="password"
              value={accessToken}
              onChange={(e) => setAccessToken(e.target.value)}
              placeholder="EAAG..."
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white font-mono"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1.5">META APP ID (OPTIONAL)</label>
              <input
                type="text"
                value={appId}
                onChange={(e) => setAppId(e.target.value)}
                placeholder="App ID"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white font-mono"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1.5">APP SECRET (OPTIONAL)</label>
              <input
                type="password"
                value={appSecret}
                onChange={(e) => setAppSecret(e.target.value)}
                placeholder="App Secret"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white font-mono"
              />
            </div>
          </div>

          <button
            onClick={handleConnect}
            disabled={saving}
            className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-purple-600/30 text-xs transition"
          >
            {saving ? 'Saving...' : 'Save Instagram Credentials'}
          </button>
        </div>

        {/* Setup Checklist Wizard */}
        <div className="lg:col-span-5 bg-[#121723] border border-[#1F293D] rounded-2xl p-6 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center justify-between">
            <span>Meta Setup Checklist</span>
            <span className="text-xs text-purple-400 font-mono">v21.0 Compliant</span>
          </h2>

          <div className="space-y-3">
            {wizard.map((step) => (
              <div key={step.step} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
                <div className="flex items-center gap-2">
                  <CheckCircle2 size={16} className={step.done ? 'text-emerald-400' : 'text-slate-600'} />
                  <span className="text-xs font-bold text-white">Step {step.step}: {step.title}</span>
                </div>
                <p className="text-[11px] text-slate-400 pl-6 leading-relaxed">{step.detail}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
