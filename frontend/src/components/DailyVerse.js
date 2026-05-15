import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Sun, RefreshCw } from 'lucide-react';
import VerseCard from './VerseCard';

const API = process.env.REACT_APP_BACKEND_URL;

export default function DailyVerse() {
  const [verse, setVerse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ texts: 0, verses: 0 });

  useEffect(() => {
    fetchDailyVerse();
    fetchStats();
  }, []);

  const fetchDailyVerse = async () => {
    setLoading(true);
    try {
      const { data } = await axios.get(`${API}/api/daily-verse`);
      setVerse(data);
    } catch (err) {
      console.error('Failed to load daily verse', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const { data } = await axios.get(`${API}/api/scriptures`);
      setStats({ texts: data.length, verses: 180 });
    } catch {}
  };

  const today = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

  return (
    <div className="animate-fade-in" data-testid="daily-verse-section">
      {/* Welcome banner */}
      <div className="mb-8">
        <p className="text-xs text-[#A39E93] uppercase tracking-widest mb-2">{today}</p>
        <h2 className="font-heading text-2xl sm:text-3xl font-bold text-[#2C2A29] mb-1">Verse of the Day</h2>
        <p className="text-sm text-[#75716B]">A daily invitation to reflect on ancient wisdom</p>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <RefreshCw className="w-5 h-5 text-[#D97757] animate-spin" />
        </div>
      ) : verse ? (
        <div className="max-w-2xl">
          <VerseCard verse={verse} expanded />
        </div>
      ) : (
        <p className="text-[#75716B] text-center py-10">No verse available today.</p>
      )}

      {/* Stats strip */}
      <div className="mt-12 grid grid-cols-3 gap-4 max-w-lg">
        <div className="text-center py-4 border border-[#E8E3D9] rounded-lg bg-white">
          <p className="font-heading text-2xl font-bold text-[#D97757]">{stats.texts}</p>
          <p className="text-xs text-[#A39E93] mt-1">Sacred Texts</p>
        </div>
        <div className="text-center py-4 border border-[#E8E3D9] rounded-lg bg-white">
          <p className="font-heading text-2xl font-bold text-[#D97757]">180+</p>
          <p className="text-xs text-[#A39E93] mt-1">Verses</p>
        </div>
        <div className="text-center py-4 border border-[#E8E3D9] rounded-lg bg-white">
          <p className="font-heading text-2xl font-bold text-[#D97757]">AI</p>
          <p className="text-xs text-[#A39E93] mt-1">Explanations</p>
        </div>
      </div>

      {/* Inspiration cards */}
      <div className="mt-8 grid sm:grid-cols-2 gap-4 max-w-2xl">
        <div className="bg-[#2C2A29] rounded-lg p-5">
          <p className="font-scripture text-base italic text-white/90 leading-relaxed">
            "Truth alone triumphs, not falsehood."
          </p>
          <p className="text-xs text-white/40 mt-3">Mundaka Upanishad</p>
        </div>
        <div className="bg-[#F5F2EA] rounded-lg p-5">
          <p className="font-scripture text-base italic text-[#2C2A29] leading-relaxed">
            "Dharma protects those who protect dharma."
          </p>
          <p className="text-xs text-[#A39E93] mt-3">Mahabharata</p>
        </div>
      </div>
    </div>
  );
}
