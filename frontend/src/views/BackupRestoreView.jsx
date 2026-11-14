import React, { useState, useEffect } from 'react';
import { Database, Download, RotateCcw, Plus, CheckCircle2, HardDrive } from 'lucide-react';

export default function BackupRestoreView() {
  const [backups, setBackups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [restoringId, setRestoringId] = useState(null);

  const fetchBackups = async () => {
    try {
      const res = await fetch('/api/backups');
      if (res.ok) {
        const json = await res.json();
        setBackups(json || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBackups();
  }, []);

  const handleCreateBackup = async () => {
    setCreating(true);
    try {
      const res = await fetch('/api/backups/create', { method: 'POST' });
      if (res.ok) {
        alert("Database snapshot created successfully!");
        fetchBackups();
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setCreating(false);
    }
  };

  const handleRestore = async (backupId) => {
    if (!confirm("Are you sure you want to restore this database snapshot? Current state will be replaced.")) return;
    setRestoringId(backupId);
    try {
      const res = await fetch(`/api/backups/${backupId}/restore`, { method: 'POST' });
      if (res.ok) {
        alert("Database restored successfully!");
        window.location.reload();
      } else {
        alert("Restore failed");
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setRestoringId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Database Backup & Recovery</h1>
          <p className="text-slate-400 text-sm mt-1">
            Create atomic SQLite snapshots, safeguard publishing history & analytics, and restore states with one click.
          </p>
        </div>

        <button
          onClick={handleCreateBackup}
          disabled={creating}
          className="px-4 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs flex items-center gap-2 shadow-lg shadow-purple-600/30 transition"
        >
          <Plus size={16} />
          {creating ? 'Taking Snapshot...' : 'Create Snapshot Now'}
        </button>
      </div>

      {/* Backups List */}
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4">Available Snapshots</h2>

        {loading ? (
          <div className="p-8 text-center text-slate-500 text-sm">Loading backup archive...</div>
        ) : backups.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-sm">No backup snapshots found. Click Create Snapshot Now to take one.</div>
        ) : (
          <div className="space-y-3">
            {backups.map((b) => {
              const dt = new Date(b.created_at);
              const fileName = b.backup_path.split('\\').pop();

              return (
                <div key={b.id} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-xl bg-purple-900/40 text-purple-300">
                      <Database size={20} />
                    </div>
                    <div>
                      <div className="text-sm font-bold text-white font-mono">{fileName}</div>
                      <div className="text-xs text-slate-400 mt-0.5">
                        Created: {dt.toLocaleString()} • Size: {Math.round(b.file_size_bytes / 1024)} KB • Type: {b.backup_type}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleRestore(b.id)}
                      disabled={restoringId === b.id}
                      className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-bold border border-slate-700 flex items-center gap-1.5 transition"
                    >
                      <RotateCcw size={14} />
                      {restoringId === b.id ? 'Restoring...' : 'Restore'}
                    </button>
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
