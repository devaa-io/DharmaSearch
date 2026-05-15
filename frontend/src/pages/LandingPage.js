import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate } from 'react-router-dom';
import { Search, BookOpen, Bookmark, Share2, Sparkles, ChevronRight } from 'lucide-react';

const API_URL = process.env.REACT_APP_BACKEND_URL;

export default function LandingPage() {
  const { user, loading } = useAuth();

  if (loading) return null;
  if (user) return <Navigate to="/dashboard" />;

  return (
    <div className="min-h-screen bg-[#FDFBF7]">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-[#FDFBF7]/80 backdrop-blur-xl border-b border-[#E8E3D9]" data-testid="landing-header">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-[#D97757] rounded-full flex items-center justify-center">
              <BookOpen className="w-4 h-4 text-white" />
            </div>
            <span className="font-heading text-xl font-bold text-[#2C2A29]">DharmaSearch</span>
          </div>
          <div className="flex items-center gap-3">
            <a href="/login" className="text-[#75716B] hover:text-[#2C2A29] font-medium transition-colors px-4 py-2" data-testid="landing-login-btn">
              Sign In
            </a>
            <a href="/register" className="bg-[#D97757] text-white rounded-full px-6 py-2.5 font-medium hover:bg-[#C16648] transition-colors" data-testid="landing-register-btn">
              Get Started
            </a>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden" data-testid="landing-hero">
        <div className="max-w-7xl mx-auto px-6 py-20 lg:py-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="animate-fade-in-up">
              <div className="inline-flex items-center gap-2 bg-[#D97757]/10 text-[#D97757] rounded-full px-4 py-1.5 text-sm font-medium mb-6">
                <Sparkles className="w-4 h-4" />
                AI-Powered Scripture Search
              </div>
              <h1 className="font-heading text-4xl sm:text-5xl lg:text-6xl tracking-tight leading-none text-[#2C2A29] mb-6">
                Discover the Wisdom of Ancient India
              </h1>
              <p className="text-base lg:text-lg text-[#75716B] leading-relaxed mb-8 max-w-lg">
                Explore the Bhagavad Gita, Ramayana, and Devi Mahatmyam with intelligent search. Find exact verses, understand their meaning, and save your favorites.
              </p>
              <div className="flex flex-col sm:flex-row gap-3">
                <a href="/register" className="bg-[#D97757] text-white rounded-full px-8 py-3.5 font-medium hover:bg-[#C16648] transition-all hover:-translate-y-0.5 text-center" data-testid="hero-cta-btn">
                  Start Exploring
                  <ChevronRight className="w-4 h-4 inline ml-1" />
                </a>
                <a href="/login" className="border border-[#E8E3D9] text-[#2C2A29] rounded-full px-8 py-3.5 font-medium hover:bg-[#F5F2EA] transition-all text-center" data-testid="hero-login-btn">
                  Sign In
                </a>
              </div>
            </div>
            <div className="relative animate-fade-in-up stagger-2 hidden lg:block">
              <div className="relative rounded-2xl overflow-hidden shadow-2xl">
                <img
                  src="https://images.unsplash.com/photo-1617904472808-7e038208077a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHxoaW5kdSUyMHRlbXBsZSUyMGFyY2hpdGVjdHVyZSUyMHN1bnJpc2V8ZW58MHx8fHwxNzc4ODI4NDU2fDA&ixlib=rb-4.1.0&q=85"
                  alt="Hindu Temple"
                  className="w-full h-[400px] object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
                <div className="absolute bottom-6 left-6 right-6 text-white">
                  <p className="font-scripture text-2xl italic leading-relaxed">
                    "Wherever there is Krishna, the master of all mystics, and wherever there is Arjuna, there will also be victory."
                  </p>
                  <p className="text-sm mt-2 opacity-80">Bhagavad Gita 18.78</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-white border-y border-[#E8E3D9]" data-testid="landing-features">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="font-heading text-2xl sm:text-3xl lg:text-4xl tracking-tight text-[#2C2A29] mb-4">
              Everything You Need to Explore Sacred Texts
            </h2>
            <p className="text-base text-[#75716B] max-w-xl mx-auto">
              A modern tool designed with reverence for ancient wisdom.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: Search, title: "Smart Search", desc: "AI-powered semantic search finds verses by meaning, not just keywords." },
              { icon: BookOpen, title: "Browse Texts", desc: "Navigate through chapters and sections of Gita, Ramayana & Devi Mahatmyam." },
              { icon: Bookmark, title: "Save Favorites", desc: "Bookmark verses that resonate with you for quick access later." },
              { icon: Share2, title: "Share Wisdom", desc: "Copy and share beautiful verse cards with friends and family." },
            ].map((f, i) => (
              <div key={i} className={`bg-white border border-[#E8E3D9] rounded-2xl p-8 hover:-translate-y-1 hover:shadow-md transition-all duration-300 animate-fade-in-up stagger-${i+1}`}>
                <div className="w-12 h-12 bg-[#D97757]/10 rounded-xl flex items-center justify-center mb-4">
                  <f.icon className="w-6 h-6 text-[#D97757]" />
                </div>
                <h3 className="font-heading text-xl font-bold text-[#2C2A29] mb-2">{f.title}</h3>
                <p className="text-sm text-[#75716B] leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Texts Preview */}
      <section className="py-20" data-testid="landing-texts">
        <div className="max-w-7xl mx-auto px-6">
          <h2 className="font-heading text-2xl sm:text-3xl lg:text-4xl tracking-tight text-[#2C2A29] mb-12 text-center">
            Sacred Texts Available
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { name: "Bhagavad Gita", desc: "The Song of God - 18 chapters of timeless wisdom from Lord Krishna to Arjuna.", img: "https://images.unsplash.com/photo-1643300788512-64b38ad876c6?w=400" },
              { name: "Ramayana", desc: "The epic journey of Lord Rama - 7 Kandas covering duty, devotion, and dharma.", img: "https://images.unsplash.com/photo-1617904472808-7e038208077a?w=400" },
              { name: "Devi Mahatmyam", desc: "The Glory of the Goddess - 13 chapters celebrating the Divine Feminine power.", img: "https://images.unsplash.com/photo-1488875482628-eee706cbfad5?w=400" },
            ].map((t, i) => (
              <div key={i} className="group relative rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                <img src={t.img} alt={t.name} className="w-full h-64 object-cover group-hover:scale-105 transition-transform duration-500" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
                  <h3 className="font-heading text-2xl font-bold mb-1">{t.name}</h3>
                  <p className="text-sm opacity-90">{t.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#E8E3D9] py-8">
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-[#D97757]" />
            <span className="font-heading font-bold text-[#2C2A29]">DharmaSearch</span>
          </div>
          <p className="text-sm text-[#A39E93]">Exploring ancient wisdom with modern tools</p>
        </div>
      </footer>
    </div>
  );
}
