import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import { BookOpen, Search, Compass, Bookmark, LogOut, Sparkles, Sun, Flame, Menu, X, Image } from 'lucide-react';
import DailyVerse from '../components/DailyVerse';
import SearchTab from '../components/SearchTab';
import BrowseTexts from '../components/BrowseTexts';
import BookmarksTab from '../components/BookmarksTab';

const tabs = [
  { id: 'home', label: 'Daily Verse', icon: Sun },
  { id: 'search', label: 'Search', icon: Sparkles },
  { id: 'browse', label: 'Browse', icon: Compass },
  { id: 'bookmarks', label: 'Saved', icon: Bookmark },
];

export default function Dashboard() {
  const { user, loading, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('home');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  if (loading) return null;
  if (!user) return <Navigate to="/login" />;

  return (
    <div className="min-h-screen bg-[#FDFBF7] flex" data-testid="dashboard">
      {/* Sidebar - Desktop */}
      <aside className="hidden lg:flex flex-col w-56 min-h-screen border-r border-[#E8E3D9] bg-white fixed left-0 top-0 z-30">
        <div className="px-5 h-16 flex items-center gap-2.5 border-b border-[#E8E3D9]">
          <Flame className="w-5 h-5 text-[#D97757]" strokeWidth={1.5} />
          <span className="font-heading text-base font-bold text-[#2C2A29]">DharmaSearch</span>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1" data-testid="dashboard-nav">
          {tabs.map(t => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all ${
                activeTab === t.id
                  ? 'bg-[#D97757]/10 text-[#D97757] font-medium'
                  : 'text-[#75716B] hover:bg-[#F5F2EA] hover:text-[#2C2A29]'
              }`}
              data-testid={`nav-${t.id}`}
            >
              <t.icon className="w-[18px] h-[18px]" strokeWidth={activeTab === t.id ? 2 : 1.5} />
              {t.label}
            </button>
          ))}
        </nav>

        <div className="px-3 py-4 border-t border-[#E8E3D9]">
          <div className="px-3 mb-3">
            <p className="text-sm font-medium text-[#2C2A29] truncate">{user.name || 'User'}</p>
            <p className="text-xs text-[#A39E93] truncate">{user.email}</p>
          </div>
          <button
            onClick={logout}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-[#75716B] hover:bg-red-50 hover:text-red-600 transition-all"
            data-testid="logout-btn"
          >
            <LogOut className="w-[18px] h-[18px]" strokeWidth={1.5} />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Mobile overlay sidebar */}
      {sidebarOpen && (
        <div className="lg:hidden fixed inset-0 z-50">
          <div className="absolute inset-0 bg-black/30" onClick={() => setSidebarOpen(false)} />
          <aside className="absolute left-0 top-0 bottom-0 w-64 bg-white animate-slide-down">
            <div className="px-5 h-16 flex items-center justify-between border-b border-[#E8E3D9]">
              <div className="flex items-center gap-2.5">
                <Flame className="w-5 h-5 text-[#D97757]" strokeWidth={1.5} />
                <span className="font-heading text-base font-bold text-[#2C2A29]">DharmaSearch</span>
              </div>
              <button onClick={() => setSidebarOpen(false)} className="p-1 text-[#A39E93]">
                <X className="w-5 h-5" />
              </button>
            </div>
            <nav className="px-3 py-4 space-y-1" data-testid="mobile-nav">
              {tabs.map(t => (
                <button
                  key={t.id}
                  onClick={() => { setActiveTab(t.id); setSidebarOpen(false); }}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all ${
                    activeTab === t.id
                      ? 'bg-[#D97757]/10 text-[#D97757] font-medium'
                      : 'text-[#75716B] hover:bg-[#F5F2EA]'
                  }`}
                  data-testid={`mobile-nav-${t.id}`}
                >
                  <t.icon className="w-[18px] h-[18px]" />
                  {t.label}
                </button>
              ))}
            </nav>
            <div className="px-3 py-4 border-t border-[#E8E3D9]">
              <button onClick={logout} className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-[#75716B] hover:bg-red-50 hover:text-red-600 transition-all">
                <LogOut className="w-[18px] h-[18px]" strokeWidth={1.5} />
                Sign Out
              </button>
            </div>
          </aside>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 lg:ml-56">
        {/* Top bar - mobile */}
        <header className="lg:hidden sticky top-0 z-20 bg-[#FDFBF7]/80 backdrop-blur-xl border-b border-[#E8E3D9] h-14 flex items-center justify-between px-4">
          <button onClick={() => setSidebarOpen(true)} className="p-1.5 text-[#75716B]" data-testid="mobile-menu-btn">
            <Menu className="w-5 h-5" />
          </button>
          <span className="font-heading text-sm font-bold text-[#2C2A29]">
            {tabs.find(t => t.id === activeTab)?.label}
          </span>
          <div className="w-8" /> {/* spacer */}
        </header>

        {/* Top bar - desktop */}
        <header className="hidden lg:flex sticky top-0 z-20 bg-[#FDFBF7]/80 backdrop-blur-xl border-b border-[#E8E3D9] h-14 items-center justify-between px-8">
          <div className="flex items-center gap-2">
            {React.createElement(tabs.find(t => t.id === activeTab)?.icon || Sun, { className: "w-4 h-4 text-[#D97757]", strokeWidth: 1.5 })}
            <h1 className="text-sm font-medium text-[#2C2A29]">
              {tabs.find(t => t.id === activeTab)?.label}
            </h1>
          </div>
          <p className="text-xs text-[#A39E93]">
            {user.name || user.email}
          </p>
        </header>

        <main className="px-4 sm:px-6 lg:px-8 py-6 lg:py-8 max-w-5xl">
          {activeTab === 'home' && <DailyVerse />}
          {activeTab === 'search' && <SearchTab />}
          {activeTab === 'browse' && <BrowseTexts />}
          {activeTab === 'bookmarks' && <BookmarksTab />}
        </main>
      </div>
    </div>
  );
}
