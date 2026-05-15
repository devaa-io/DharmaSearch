import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import { BookOpen, Search, Compass, Bookmark, LogOut, Sparkles, Sun } from 'lucide-react';
import DailyVerse from '../components/DailyVerse';
import SearchTab from '../components/SearchTab';
import BrowseTexts from '../components/BrowseTexts';
import BookmarksTab from '../components/BookmarksTab';

const tabs = [
  { id: 'home', label: 'Daily Verse', icon: Sun },
  { id: 'search', label: 'AI Search', icon: Sparkles },
  { id: 'browse', label: 'Browse Texts', icon: Compass },
  { id: 'bookmarks', label: 'Saved', icon: Bookmark },
];

export default function Dashboard() {
  const { user, loading, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('home');

  if (loading) return null;
  if (!user) return <Navigate to="/login" />;

  return (
    <div className="min-h-screen bg-[#FDFBF7]" data-testid="dashboard">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-[#FDFBF7]/80 backdrop-blur-xl border-b border-[#E8E3D9]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-[#D97757] rounded-full flex items-center justify-center">
              <BookOpen className="w-4 h-4 text-white" />
            </div>
            <span className="font-heading text-xl font-bold text-[#2C2A29] hidden sm:block">DharmaSearch</span>
          </div>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1" data-testid="dashboard-nav">
            {tabs.map(t => (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all ${
                  activeTab === t.id
                    ? 'bg-[#D97757] text-white'
                    : 'text-[#75716B] hover:bg-[#F5F2EA] hover:text-[#2C2A29]'
                }`}
                data-testid={`nav-${t.id}`}
              >
                <t.icon className="w-4 h-4" />
                {t.label}
              </button>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <span className="text-sm text-[#75716B] hidden sm:block">{user.name || user.email}</span>
            <button
              onClick={logout}
              className="text-[#A39E93] hover:text-[#D97757] transition-colors p-2"
              data-testid="logout-btn"
              title="Sign Out"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Nav */}
      <div className="md:hidden sticky top-[57px] z-40 bg-[#FDFBF7] border-b border-[#E8E3D9] px-2 py-2">
        <div className="flex gap-1 overflow-x-auto" data-testid="mobile-nav">
          {tabs.map(t => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-full text-xs font-medium whitespace-nowrap transition-all ${
                activeTab === t.id
                  ? 'bg-[#D97757] text-white'
                  : 'text-[#75716B] bg-white border border-[#E8E3D9]'
              }`}
              data-testid={`mobile-nav-${t.id}`}
            >
              <t.icon className="w-3.5 h-3.5" />
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        {activeTab === 'home' && <DailyVerse />}
        {activeTab === 'search' && <SearchTab />}
        {activeTab === 'browse' && <BrowseTexts />}
        {activeTab === 'bookmarks' && <BookmarksTab />}
      </main>
    </div>
  );
}
