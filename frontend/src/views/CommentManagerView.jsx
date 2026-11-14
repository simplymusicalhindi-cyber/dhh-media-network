import React, { useState, useEffect } from 'react';
import { MessageSquare, Send, ShieldAlert, Sparkles, RefreshCw, CheckCircle2, User } from 'lucide-react';

export default function CommentManagerView() {
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [autoReplyEnabled, setAutoReplyEnabled] = useState(true);
  const [replyInput, setReplyInput] = useState({});
  const [simText, setSimText] = useState('Bhai KR$NA aur Seedhe Maut ka collab kab aayega?');
  const [simLoading, setSimLoading] = useState(false);

  const fetchComments = async () => {
    try {
      const res = await fetch('/api/comments');
      if (res.ok) {
        const json = await res.json();
        setComments(json || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComments();
  }, []);

  const handleManualReply = async (commentId) => {
    const text = replyInput[commentId];
    if (!text || !text.trim()) return;

    try {
      const res = await fetch(`/api/comments/${commentId}/reply`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reply_text: text })
      });
      if (res.ok) {
        setReplyInput({ ...replyInput, [commentId]: '' });
        fetchComments();
      } else {
        alert("Failed to send reply");
      }
    } catch (e) {
      alert("Error: " + e.message);
    }
  };

  const handleSimulate = async () => {
    setSimLoading(true);
    try {
      const res = await fetch('/api/comments/simulate-incoming', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: 'dhh_listener_live',
          comment_text: simText
        })
      });
      if (res.ok) {
        fetchComments();
      }
    } catch (e) {
      alert("Error: " + e.message);
    } finally {
      setSimLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Autonomous Comment Manager</h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time comment classification, spam/abuse filters, and culturally nuanced Hinglish auto-replies.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 cursor-pointer bg-slate-900 border border-slate-700 px-4 py-2 rounded-xl text-xs font-bold text-slate-300">
            <input
              type="checkbox"
              checked={autoReplyEnabled}
              onChange={(e) => {
                setAutoReplyEnabled(e.target.checked);
                fetch(`/api/comments/toggle-auto-reply?enabled=${e.target.checked}`, { method: 'POST' });
              }}
              className="accent-purple-600 rounded"
            />
            Auto-Reply Active
          </label>

          <button
            onClick={fetchComments}
            className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          >
            <RefreshCw size={16} />
          </button>
        </div>
      </div>

      {/* Simulator Bench */}
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-5">
        <h2 className="text-sm font-bold text-white mb-2 flex items-center gap-2">
          <Sparkles size={16} className="text-purple-400" />
          Test NLP Classification & Reply Engine
        </h2>
        <div className="flex gap-3">
          <input
            type="text"
            value={simText}
            onChange={(e) => setSimText(e.target.value)}
            placeholder="Type a sample comment..."
            className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-purple-500"
          />
          <button
            onClick={handleSimulate}
            disabled={simLoading}
            className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs shadow-lg shadow-purple-600/20 transition whitespace-nowrap"
          >
            {simLoading ? 'Classifying...' : 'Simulate Comment'}
          </button>
        </div>
      </div>

      {/* Comments List */}
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4">Community Conversation Feed</h2>

        {loading ? (
          <div className="p-8 text-center text-slate-500 text-sm">Loading comments...</div>
        ) : comments.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-sm">No comments ingested yet.</div>
        ) : (
          <div className="space-y-4">
            {comments.map((c) => {
              const dt = new Date(c.created_at);
              const isAbuse = c.classification === 'ABUSE';
              const isSpam = c.classification === 'SPAM';

              return (
                <div key={c.id} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-full bg-purple-900/50 flex items-center justify-center text-purple-300 font-bold text-xs">
                        <User size={14} />
                      </div>
                      <span className="font-bold text-white">@{c.username}</span>
                      <span className="text-slate-500">• {dt.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                        isAbuse ? 'bg-red-950 text-red-400 border border-red-800' : isSpam ? 'bg-amber-950 text-amber-400 border border-amber-800' : 'bg-slate-800 text-slate-300'
                      }`}>
                        {c.classification}
                      </span>
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px] font-semibold">
                        {c.sentiment}
                      </span>
                    </div>
                  </div>

                  <p className="text-sm text-slate-200 pl-9">"{c.text}"</p>

                  {/* Replies Thread */}
                  {c.replies && c.replies.length > 0 && (
                    <div className="ml-9 pl-4 border-l-2 border-purple-500/40 space-y-2">
                      {c.replies.map((r, ri) => (
                        <div key={ri} className="text-xs text-purple-300 bg-purple-950/30 p-2.5 rounded-lg border border-purple-900/30">
                          <span className="font-bold text-purple-200">@desihiphop_vibes (Auto-Reply):</span> {r.text}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Manual Reply Box */}
                  <div className="ml-9 flex gap-2 pt-1">
                    <input
                      type="text"
                      placeholder="Write a custom Hinglish reply..."
                      value={replyInput[c.id] || ''}
                      onChange={(e) => setReplyInput({ ...replyInput, [c.id]: e.target.value })}
                      className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-purple-500"
                    />
                    <button
                      onClick={() => handleManualReply(c.id)}
                      className="px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-white text-xs font-semibold flex items-center gap-1 transition"
                    >
                      <Send size={12} /> Reply
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
