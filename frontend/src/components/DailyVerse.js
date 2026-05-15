import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Sun, RefreshCw } from 'lucide-react';
import VerseCard from './VerseCard';

const API = process.env.REACT_APP_BACKEND_URL;

export default function DailyVerse() {
  const [verse, setVerse] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDailyVerse();
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

  return (
    <div className="animate-fade-in-up" data-testid="daily-verse-section">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 bg-[#D97757]/10 rounded-xl flex items-center justify-center">
          <Sun className="w-5 h-5 text-[#D97757]" />
        </div>
        <div>
          <h2 className="font-heading text-2xl sm:text-3xl font-bold text-[#2C2A29]">Verse of the Day</h2>
          <p className="text-sm text-[#75716B]">A daily dose of ancient wisdom</p>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <RefreshCw className="w-6 h-6 text-[#D97757] animate-spin" />
        </div>
      ) : verse ? (
        <div className="max-w-3xl">
          <VerseCard verse={verse} expanded />
        </div>
      ) : (
        <p className="text-[#75716B] text-center py-10">No verse available today.</p>
      )}

      {/* Decorative section */}
      <div className="mt-16 grid md:grid-cols-2 gap-6">
        <div className="relative rounded-2xl overflow-hidden h-64">
          <img
            src="https://images.unsplash.com/photo-1488875482628-eee706cbfad5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTZ8MHwxfHNlYXJjaHwzfHxsb3R1cyUyMGZsb3dlciUyMGNhbG0lMjBzdW5yaXNlfGVufDB8fHx8MTc3ODgyODQ1Nnww&ixlib=rb-4.1.0&q=85"
            alt="Lotus flower"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
          <div className="absolute bottom-4 left-4 right-4 text-white">
            <p className="font-scripture text-lg italic">"The soul is never born, nor does it die."</p>
            <p className="text-xs mt-1 opacity-80">Bhagavad Gita 2.20</p>
          </div>
        </div>
        <div className="relative rounded-2xl overflow-hidden h-64">
          <img
            src="https://images.unsplash.com/photo-1643300788512-64b38ad876c6?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA2ODl8MHwxfHNlYXJjaHwyfHxzYW5za3JpdCUyMG1hbnVzY3JpcHR8ZW58MHx8fHwxNzc4ODI4NDU2fDA&ixlib=rb-4.1.0&q=85"
            alt="Ancient manuscript"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
          <div className="absolute bottom-4 left-4 right-4 text-white">
            <p className="font-scripture text-lg italic">"Dharma protects those who protect dharma."</p>
            <p className="text-xs mt-1 opacity-80">Ramayana 3.1</p>
          </div>
        </div>
      </div>
    </div>
  );
}
