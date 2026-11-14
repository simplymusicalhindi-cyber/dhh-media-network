import React, { useState, useEffect } from 'react';
import { ExternalLink, Heart, MessageCircle, Share2, Bookmark, Eye, Film, Image as ImageIcon } from 'lucide-react';

export default function PublishedContentView() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('ALL');

  useEffect(() => {
    fetch('/api/published')
      .then(res => res.json())
      .then(data => setPosts(data || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filtered = posts.filter(p => filter === 'ALL' || p.post_type === filter);

  return (
    <div className="space-y-6">
      <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Published Content & Real Metrics</h1>
          <p className="text-slate-400 text-sm mt-1">
            Historical archive of all published DHH memes, reels, and stories with live reach, shares, and saves.
          </p>
        </div>

        <div className="flex gap-2">
          {['ALL', 'IMAGE', 'REEL', 'STORY'].map((t) => (
            <button
              key={t}
              onClick={() => setFilter(t)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition ${
                filter === t ? 'bg-purple-600 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
            >
              {t === 'ALL' ? 'All Content' : t}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="p-8 text-center text-slate-500 text-sm">Loading published library...</div>
      ) : filtered.length === 0 ? (
        <div className="bg-[#121723] border border-[#1F293D] rounded-2xl p-12 text-center text-slate-500 text-sm">
          No published content found for this filter.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map((p) => {
            const dt = new Date(p.published_at);
            const mediaFileName = p.media_path ? p.media_path.split('\\').pop() : '';
            const isReel = p.post_type === 'REEL';
            const isStory = p.post_type === 'STORY';

            return (
              <div key={p.id} className="bg-[#121723] border border-[#1F293D] rounded-2xl overflow-hidden flex flex-col justify-between">
                <div>
                  {/* Thumbnail / Media Container */}
                  <div className="aspect-square bg-black relative overflow-hidden group">
                    {mediaFileName ? (
                      isReel ? (
                        <video
                          src={`/media/reels/${mediaFileName}`}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <img
                          src={`/media/${isStory ? 'stories' : 'memes'}/${mediaFileName}`}
                          alt="Post Media"
                          className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
                        />
                      )
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-slate-600">
                        <ImageIcon size={48} />
                      </div>
                    )}

                    <span className="absolute top-3 left-3 px-2.5 py-1 rounded-md bg-black/80 backdrop-blur text-[11px] font-bold text-white border border-white/10 uppercase">
                      {p.post_type}
                    </span>

                    <a
                      href={p.permalink}
                      target="_blank"
                      rel="noreferrer"
                      className="absolute top-3 right-3 p-2 rounded-full bg-black/80 hover:bg-purple-600 text-white transition"
                    >
                      <ExternalLink size={14} />
                    </a>
                  </div>

                  {/* Caption & Metadata */}
                  <div className="p-4 space-y-2">
                    <p className="text-xs text-slate-300 line-clamp-3 leading-relaxed">
                      {p.caption}
                    </p>
                    <div className="text-[11px] text-slate-500 font-mono">
                      Published: {dt.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                    </div>
                  </div>
                </div>

                {/* Metrics Footer */}
                <div className="px-4 py-3 bg-slate-900/60 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                  <span className="flex items-center gap-1 text-slate-300 font-semibold" title="Reach">
                    <Eye size={13} className="text-blue-400" /> {p.reach.toLocaleString()}
                  </span>
                  <span className="flex items-center gap-1 font-semibold text-rose-300" title="Likes">
                    <Heart size={13} className="text-rose-400" /> {p.likes.toLocaleString()}
                  </span>
                  <span className="flex items-center gap-1 font-semibold text-emerald-300" title="Comments">
                    <MessageCircle size={13} className="text-emerald-400" /> {p.comments.toLocaleString()}
                  </span>
                  <span className="flex items-center gap-1 font-semibold text-amber-300" title="Shares">
                    <Share2 size={13} className="text-amber-400" /> {p.shares.toLocaleString()}
                  </span>
                  <span className="flex items-center gap-1 font-semibold text-purple-300" title="Saves">
                    <Bookmark size={13} className="text-purple-400" /> {p.saves.toLocaleString()}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
