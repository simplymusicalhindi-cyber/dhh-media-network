import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, Sparkles, Palette, Film, BookOpen, Calendar, 
  ListOrdered, CheckSquare, MessageSquare, Search, TrendingUp, 
  BarChart3, Cpu, Instagram, AlertOctagon, Activity, Database, 
  Settings as SettingsIcon, ShieldCheck, Flame, Radio
} from 'lucide-react';

import OverviewView from './views/OverviewView';
import ContentGeneratorView from './views/ContentGeneratorView';
import MemeStudioView from './views/MemeStudioView';
import ReelsStudioView from './views/ReelsStudioView';
import StoryStudioView from './views/StoryStudioView';
import CalendarView from './views/CalendarView';
import PendingQueueView from './views/PendingQueueView';
import PublishedContentView from './views/PublishedContentView';
import CommentManagerView from './views/CommentManagerView';
import SEOManagerView from './views/SEOManagerView';
import AudienceGrowthView from './views/AudienceGrowthView';
import AnalyticsView from './views/AnalyticsView';
import AISettingsView from './views/AISettingsView';
import InstagramConnectionView from './views/InstagramConnectionView';
import ErrorLogsView from './views/ErrorLogsView';
import SystemHealthView from './views/SystemHealthView';
import BackupRestoreView from './views/BackupRestoreView';
import GeneralSettingsView from './views/GeneralSettingsView';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [currentTime, setCurrentTime] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(now.toLocaleTimeString('en-IN', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', second: '2-digit' }) + ' IST');
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const navGroups = [
    {
      label: 'COMMAND',
      items: [
        { id: 'overview', name: 'Overview', icon: LayoutDashboard }
      ]
    },
    {
      label: 'CREATION SUITE',
      items: [
        { id: 'content_gen', name: 'Content Generator', icon: Sparkles },
        { id: 'meme_studio', name: 'Meme Studio', icon: Palette },
        { id: 'reels_studio', name: 'Reels Studio', icon: Film },
        { id: 'story_studio', name: 'Story Studio', icon: BookOpen }
      ]
    },
    {
      label: 'PUBLISHING PIPELINE',
      items: [
        { id: 'calendar', name: 'Publishing Calendar', icon: Calendar },
        { id: 'queue', name: 'Pending Queue', icon: ListOrdered },
        { id: 'published', name: 'Published Content', icon: CheckSquare }
      ]
    },
    {
      label: 'GROWTH & COMMUNITY',
      items: [
        { id: 'comments', name: 'Comment Manager', icon: MessageSquare },
        { id: 'seo', name: 'SEO & Captions', icon: Search },
        { id: 'growth', name: 'Audience Growth', icon: TrendingUp },
        { id: 'analytics', name: 'Analytics & Learning', icon: BarChart3 }
      ]
    },
    {
      label: 'SYSTEM & INTEGRATIONS',
      items: [
        { id: 'ai_settings', name: 'AI & Ollama Settings', icon: Cpu },
        { id: 'instagram', name: 'Instagram Connection', icon: Instagram },
        { id: 'errors', name: 'Error Diagnostics', icon: AlertOctagon },
        { id: 'health', name: 'System Health', icon: Activity },
        { id: 'backups', name: 'Backup & Restore', icon: Database },
        { id: 'settings', name: 'General Settings', icon: SettingsIcon }
      ]
    }
  ];

  const renderActiveView = () => {
    switch (activeTab) {
      case 'overview': return <OverviewView setActiveTab={setActiveTab} />;
      case 'content_gen': return <ContentGeneratorView setActiveTab={setActiveTab} />;
      case 'meme_studio': return <MemeStudioView />;
      case 'reels_studio': return <ReelsStudioView />;
      case 'story_studio': return <StoryStudioView />;
      case 'calendar': return <CalendarView />;
      case 'queue': return <PendingQueueView />;
      case 'published': return <PublishedContentView />;
      case 'comments': return <CommentManagerView />;
      case 'seo': return <SEOManagerView />;
      case 'growth': return <AudienceGrowthView />;
      case 'analytics': return <AnalyticsView />;
      case 'ai_settings': return <AISettingsView />;
      case 'instagram': return <InstagramConnectionView />;
      case 'errors': return <ErrorLogsView />;
      case 'health': return <SystemHealthView />;
      case 'backups': return <BackupRestoreView />;
      case 'settings': return <GeneralSettingsView />;
      default: return <OverviewView setActiveTab={setActiveTab} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-[#090B11] text-slate-100">
      {/* Sidebar Navigation */}
      <aside className="w-72 bg-[#0D111A] border-r border-[#1F293D] flex flex-col justify-between shrink-0">
        <div>
          {/* Brand Header */}
          <div className="p-5 border-b border-[#1F293D] flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-500 flex items-center justify-center text-white font-extrabold shadow-lg shadow-purple-600/30">
              <Flame size={22} />
            </div>
            <div>
              <div className="font-extrabold text-sm text-white tracking-wider flex items-center gap-1.5">
                DHH NETWORK <span className="text-[10px] bg-purple-950 text-purple-300 px-1.5 py-0.5 rounded border border-purple-800">24/7</span>
              </div>
              <div className="text-[11px] text-slate-400">Autonomous Media Platform</div>
            </div>
          </div>

          {/* Nav Items List */}
          <nav className="p-3 space-y-5 overflow-y-auto max-h-[calc(100vh-140px)]">
            {navGroups.map((group, gi) => (
              <div key={gi} className="space-y-1">
                <div className="text-[10px] font-bold tracking-widest text-slate-500 px-3 uppercase mb-1.5">
                  {group.label}
                </div>
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = activeTab === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => setActiveTab(item.id)}
                      className={`w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-semibold transition ${
                        isActive
                          ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/25'
                          : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                      }`}
                    >
                      <Icon size={16} className={isActive ? 'text-white' : 'text-slate-400'} />
                      <span>{item.name}</span>
                    </button>
                  );
                })}
              </div>
            ))}
          </nav>
        </div>

        {/* Sidebar Footer */}
        <div className="p-4 border-t border-[#1F293D] bg-[#090B11]/80 text-[11px] text-slate-400 flex items-center justify-between font-mono">
          <div className="flex items-center gap-1.5 text-emerald-400 font-bold">
            <Radio size={14} className="animate-pulse" />
            <span>LIVE 8787</span>
          </div>
          <div>{currentTime}</div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        {/* Top Header Bar */}
        <header className="h-16 bg-[#0D111A]/80 backdrop-blur border-b border-[#1F293D] px-8 flex items-center justify-between shrink-0 sticky top-0 z-30">
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-purple-400 uppercase tracking-widest font-bold">
              {navGroups.flatMap(g => g.items).find(i => i.id === activeTab)?.name || 'Dashboard'}
            </span>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="font-semibold text-white">@desihiphop_vibes</span>
            </div>

            <div className="text-xs text-slate-400 font-mono hidden sm:block">
              Target: 10 Posts • 5 Reels • 1 Story
            </div>
          </div>
        </header>

        {/* View Content */}
        <div className="p-8 max-w-7xl mx-auto w-full">
          {renderActiveView()}
        </div>
      </main>
    </div>
  );
}
