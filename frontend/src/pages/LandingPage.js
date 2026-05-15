import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate, Link } from 'react-router-dom';
import { Search, BookOpen, Bookmark, Share2, Sparkles, ArrowRight, Flame, Star, Layers } from 'lucide-react';

export default function LandingPage() {
  const { user, loading } = useAuth();

  if (loading) return null;
  if (user) return <Navigate to="/dashboard" />;

  const texts = [
    { name: "Bhagavad Gita", chapters: "18 Chapters", era: "~500 BCE" },
    { name: "Ramayana", chapters: "7 Kandas", era: "~500 BCE" },
    { name: "Devi Mahatmyam", chapters: "13 Chapters", era: "~500 CE" },
    { name: "Upanishads", chapters: "8 Texts", era: "~800 BCE" },
    { name: "Yoga Sutras", chapters: "4 Padas", era: "~200 BCE" },
    { name: "Mahabharata", chapters: "5 Parvas", era: "~400 BCE" },
    { name: "Vedas", chapters: "4 Vedas", era: "~1500 BCE" },
    { name: "Hanuman Chalisa", chapters: "40 Verses", era: "~1575 CE" },
    { name: "Puranas", chapters: "4 Texts", era: "~300 CE" },
  ];

  return (
    <div className="min-h-screen bg-[#FDFBF7] overflow-x-hidden">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#FDFBF7]/60 backdrop-blur-2xl border-b border-[#E8E3D9]/50" data-testid="landing-header">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5">
            <Flame className="w-6 h-6 text-[#D97757]" strokeWidth={1.5} />
            <span className="font-heading text-lg font-bold tracking-tight text-[#2C2A29]">DharmaSearch</span>
          </Link>
          <div className="flex items-center gap-2">
            <Link to="/login" className="text-sm text-[#75716B] hover:text-[#2C2A29] transition-colors px-4 py-2 rounded-lg hover:bg-[#F5F2EA]" data-testid="landing-login-btn">
              Sign In
            </Link>
            <Link to="/register" className="text-sm bg-[#2C2A29] text-[#FDFBF7] px-5 py-2 rounded-lg hover:bg-[#1a1918] transition-colors font-medium" data-testid="landing-register-btn">
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero — asymmetric split */}
      <section className="pt-32 pb-20 lg:pb-32 relative" data-testid="landing-hero">
        {/* Decorative grain */}
        <div className="absolute inset-0 opacity-[0.03]" style={{backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 256 256\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noise)\'/%3E%3C/svg%3E")'}} />
        <div className="max-w-7xl mx-auto px-6">
          <div className="lg:grid lg:grid-cols-12 lg:gap-8 items-start">
            {/* Left: text — 7 cols, left-aligned */}
            <div className="lg:col-span-7 lg:pr-8">
              <div className="inline-flex items-center gap-2 text-[#D97757] text-xs font-semibold tracking-widest uppercase mb-8">
                <div className="w-8 h-px bg-[#D97757]" />
                9 Sacred Texts &middot; 180+ Verses
              </div>

              <h1 className="font-heading text-4xl sm:text-5xl lg:text-[3.5rem] xl:text-6xl leading-[1.05] tracking-tight text-[#2C2A29] mb-6">
                The scriptures of<br className="hidden sm:block" /> ancient India,<br className="hidden sm:block" />
                <span className="text-[#D97757]">searchable.</span>
              </h1>

              <p className="text-base lg:text-lg text-[#75716B] leading-relaxed max-w-md mb-10">
                Search by meaning across the Gita, Ramayana, Upanishads, Vedas, and more. Bookmark, share as images, and let AI explain the context.
              </p>

              <div className="flex items-center gap-4 mb-16">
                <Link to="/register" className="group inline-flex items-center gap-2 bg-[#D97757] text-white px-7 py-3.5 rounded-lg font-medium hover:bg-[#C16648] transition-all" data-testid="hero-cta-btn">
                  Start Exploring
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Link>
                <Link to="/login" className="text-sm text-[#75716B] hover:text-[#2C2A29] transition-colors underline underline-offset-4 decoration-[#E8E3D9] hover:decoration-[#2C2A29]" data-testid="hero-login-btn">
                  I have an account
                </Link>
              </div>

              {/* Scrolling text ticker */}
              <div className="border-t border-[#E8E3D9] pt-8">
                <p className="text-xs text-[#A39E93] uppercase tracking-widest mb-4">Texts included</p>
                <div className="flex flex-wrap gap-2">
                  {texts.map((t, i) => (
                    <span key={i} className="text-xs border border-[#E8E3D9] text-[#75716B] rounded-md px-3 py-1.5 bg-white/50">
                      {t.name}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Right: stacked quote cards — 5 cols */}
            <div className="lg:col-span-5 mt-12 lg:mt-0 relative">
              <div className="space-y-4">
                {/* Card 1 - featured */}
                <div className="bg-[#2C2A29] text-white rounded-xl p-8 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-[#D97757]/20 rounded-full -translate-y-1/2 translate-x-1/2 blur-2xl" />
                  <p className="font-scripture text-xl sm:text-2xl italic leading-relaxed relative z-10">
                    "You have a right to perform your prescribed duty, but you are not entitled to the fruits of action."
                  </p>
                  <div className="mt-4 flex items-center gap-2 relative z-10">
                    <div className="w-1 h-4 bg-[#D97757] rounded-full" />
                    <span className="text-sm text-white/60">Bhagavad Gita 2.47</span>
                  </div>
                </div>

                {/* Card 2 */}
                <div className="bg-white border border-[#E8E3D9] rounded-xl p-6">
                  <p className="font-scripture text-lg italic leading-relaxed text-[#2C2A29]">
                    "Lead me from the unreal to the real, lead me from darkness to light."
                  </p>
                  <div className="mt-3 flex items-center gap-2">
                    <div className="w-1 h-3 bg-[#8A9A86] rounded-full" />
                    <span className="text-xs text-[#A39E93]">Brihadaranyaka Upanishad</span>
                  </div>
                </div>

                {/* Card 3 */}
                <div className="bg-[#F5F2EA] rounded-xl p-6">
                  <p className="font-scripture text-lg italic leading-relaxed text-[#2C2A29]">
                    "Yoga is the cessation of the fluctuations of the mind."
                  </p>
                  <div className="mt-3 flex items-center gap-2">
                    <div className="w-1 h-3 bg-[#D97757] rounded-full" />
                    <span className="text-xs text-[#A39E93]">Yoga Sutras 1.2</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features — horizontal list, not cards grid */}
      <section className="py-20 border-t border-[#E8E3D9]" data-testid="landing-features">
        <div className="max-w-7xl mx-auto px-6">
          <div className="lg:grid lg:grid-cols-12 lg:gap-16 items-start">
            <div className="lg:col-span-4 mb-12 lg:mb-0">
              <h2 className="font-heading text-2xl sm:text-3xl lg:text-4xl tracking-tight text-[#2C2A29] mb-4">
                Built for deep study, not surface reading.
              </h2>
              <p className="text-base text-[#75716B] leading-relaxed">
                Every feature is designed to help you find, understand, and remember sacred knowledge.
              </p>
            </div>
            <div className="lg:col-span-8">
              <div className="grid sm:grid-cols-2 gap-x-8 gap-y-10">
                {[
                  { icon: Sparkles, title: "AI Semantic Search", desc: "Ask in plain language: 'What does Krishna say about the soul?' — the AI finds the right verses by meaning, not keywords." },
                  { icon: Search, title: "Keyword Search", desc: "Quick text matching across 180+ verses from 9 texts. Filter by scripture for focused study." },
                  { icon: Layers, title: "Browse by Structure", desc: "Navigate texts the traditional way — by book, chapter, and verse. See the full context around each shloka." },
                  { icon: Bookmark, title: "Save & Organize", desc: "Bookmark verses that speak to you. Build your personal collection of sacred wisdom." },
                  { icon: Share2, title: "Share as Image", desc: "Generate beautiful quote cards from any verse. Share on social media or save for personal reflection." },
                  { icon: Star, title: "Verse of the Day", desc: "A new verse each day, chosen from across all 9 texts. Start your morning with ancient wisdom." },
                ].map((f, i) => (
                  <div key={i} className="group">
                    <div className="flex items-center gap-3 mb-2">
                      <f.icon className="w-5 h-5 text-[#D97757]" strokeWidth={1.5} />
                      <h3 className="font-medium text-[#2C2A29]">{f.title}</h3>
                    </div>
                    <p className="text-sm text-[#75716B] leading-relaxed pl-8">{f.desc}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Texts grid — visual, not uniform */}
      <section className="py-20 bg-[#2C2A29]" data-testid="landing-texts">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center gap-3 mb-12">
            <div className="w-8 h-px bg-[#D97757]" />
            <h2 className="font-heading text-2xl sm:text-3xl text-white tracking-tight">Nine sacred texts, one search.</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
            {texts.map((t, i) => (
              <div key={i} className="group bg-white/5 border border-white/10 rounded-lg p-5 hover:bg-white/10 hover:border-[#D97757]/30 transition-all duration-300 cursor-default">
                <p className="font-heading text-lg text-white mb-1">{t.name}</p>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-white/40">{t.chapters}</span>
                  <span className="text-[10px] text-[#D97757]/80">{t.era}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24">
        <div className="max-w-2xl mx-auto px-6 text-center">
          <h2 className="font-heading text-3xl sm:text-4xl tracking-tight text-[#2C2A29] mb-4">
            Begin your search.
          </h2>
          <p className="text-base text-[#75716B] mb-8">
            Free to use. No credit card required.
          </p>
          <Link to="/register" className="inline-flex items-center gap-2 bg-[#D97757] text-white px-8 py-4 rounded-lg font-medium hover:bg-[#C16648] transition-all text-lg" data-testid="cta-register-btn">
            Create Account
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#E8E3D9] py-6">
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Flame className="w-4 h-4 text-[#D97757]" strokeWidth={1.5} />
            <span className="font-heading text-sm font-bold text-[#2C2A29]">DharmaSearch</span>
          </div>
          <p className="text-xs text-[#A39E93]">9 texts &middot; 180+ verses &middot; AI-powered</p>
        </div>
      </footer>
    </div>
  );
}
