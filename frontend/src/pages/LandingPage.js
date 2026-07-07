import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Search, BookOpen, Bookmark, Share2, Sparkles, ArrowRight, Flame, Star, Layers, ChevronDown, ChevronUp, MapPin, Globe, Calendar } from 'lucide-react';

const API = process.env.REACT_APP_BACKEND_URL;

function SampleVerseCard({ verse, defaultExpanded = false }) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const [transLang, setTransLang] = useState(null);
  const LANG_LABELS = { ml: 'Malayalam', hi: 'Hindi', ta: 'Tamil' };
  const availableTranslits = verse.transliterations ? Object.keys(verse.transliterations) : [];

  return (
    <div className="bg-white border border-[#E8E3D9] rounded-xl overflow-hidden hover:border-[#D97757]/30 transition-all duration-300" data-testid={`sample-verse-${verse.verse_id}`}>
      <div className="h-0.5 bg-gradient-to-r from-[#D97757] via-[#D97757]/50 to-transparent" />
      <div className="p-5">
        <div className="mb-3">
          <span className="text-xs font-semibold uppercase tracking-wider text-[#D97757]">{verse.text_name}</span>
          <p className="text-xs text-[#A39E93] mt-0.5">Ch. {verse.chapter}{verse.chapter_name ? ` · ${verse.chapter_name}` : ''} · V. {verse.verse_number}</p>
        </div>

        {verse.text && (
          <p className="font-scripture text-base italic text-[#2C2A29]/40 leading-relaxed mb-2">
            {expanded ? verse.text : verse.text.substring(0, 100) + (verse.text.length > 100 ? '...' : '')}
          </p>
        )}

        <p className="text-[15px] text-[#2C2A29] leading-[1.7] mb-2">
          {expanded ? verse.translation : verse.translation.substring(0, 150) + (verse.translation.length > 150 ? '...' : '')}
        </p>

        {(verse.translation.length > 150 || (verse.text && verse.text.length > 100)) && (
          <button onClick={() => setExpanded(!expanded)} className="text-xs text-[#D97757] hover:underline flex items-center gap-1 mb-2">
            {expanded ? <>Show less <ChevronUp className="w-3 h-3" /></> : <>Read more <ChevronDown className="w-3 h-3" /></>}
          </button>
        )}

        {expanded && verse.keywords && (
          <div className="flex flex-wrap gap-1 mb-2">
            {verse.keywords.split(',').slice(0, 4).map((k, i) => (
              <span key={i} className="text-[10px] bg-[#F5F2EA] text-[#75716B] rounded px-2 py-0.5">{k.trim()}</span>
            ))}
          </div>
        )}

        {/* Transliteration */}
        {expanded && availableTranslits.length > 0 && (
          <div className="mb-2">
            <div className="flex items-center gap-1 mb-1.5">
              <Globe className="w-3 h-3 text-[#A39E93]" />
              {availableTranslits.map(lang => (
                <button key={lang} onClick={() => setTransLang(transLang === lang ? null : lang)}
                  className={`text-[10px] px-2 py-0.5 rounded transition-all ${transLang === lang ? 'bg-[#D97757] text-white' : 'bg-[#F5F2EA] text-[#75716B]'}`}>
                  {LANG_LABELS[lang] || lang}
                </button>
              ))}
            </div>
            {transLang && verse.transliterations[transLang] && (
              <p className="text-sm text-[#2C2A29]/70 bg-[#FDFBF7] border border-[#E8E3D9] rounded-lg p-2.5">{verse.transliterations[transLang]}</p>
            )}
          </div>
        )}

        {/* Temple connection */}
        {expanded && verse.temple_connection && (
          <div className="bg-amber-50/50 border border-amber-200/30 rounded-lg p-2.5">
            <div className="flex items-start gap-1.5">
              <MapPin className="w-3 h-3 text-amber-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-xs font-medium text-amber-800">{verse.temple_connection.temple}</p>
                <p className="text-[10px] text-amber-600">{verse.temple_connection.location}</p>
                {verse.temple_connection.detail && <p className="text-xs text-amber-700/80 mt-1 leading-relaxed">{verse.temple_connection.detail}</p>}
              </div>
            </div>
          </div>
        )}

        {!expanded && (
          <p className="text-[10px] text-[#A39E93] mt-2">Click "Read more" to see transliterations, temple connections & more</p>
        )}
      </div>
    </div>
  );
}


export default function LandingPage() {
  const { user, loading } = useAuth();
  const [sampleVerses, setSampleVerses] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [showMoreSamples, setShowMoreSamples] = useState(false);

  useEffect(() => {
    axios.get(`${API}/api/public/sample-verses`).then(r => setSampleVerses(r.data)).catch(() => {});
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    setSearching(true);
    setHasSearched(true);
    try {
      const { data } = await axios.get(`${API}/api/public/search?q=${encodeURIComponent(searchQuery.trim())}`);
      setSearchResults(data);
    } catch { setSearchResults([]); }
    finally { setSearching(false); }
  };

  if (loading) return null;
  if (user) return <Navigate to="/dashboard" />;

  const texts = [
    { name: "Bhagavad Gita", era: "~500 BCE" }, { name: "Ramayana", era: "~500 BCE" },
    { name: "Devi Mahatmyam", era: "~500 CE" }, { name: "Upanishads", era: "~800 BCE" },
    { name: "Yoga Sutras", era: "~200 BCE" }, { name: "Mahabharata", era: "~400 BCE" },
    { name: "Vedas", era: "~1500 BCE" }, { name: "Hanuman Chalisa", era: "~1575 CE" },
    { name: "Puranas", era: "~300 CE" }, { name: "Srimad Bhagavatam", era: "~500 CE" },
    { name: "Narayaneeyam", era: "1586 CE" }, { name: "Adhyatma Ramayanam", era: "~1575 CE" },
    { name: "Lalita Sahasranama", era: "~500 CE" }, { name: "Vishnu Sahasranama", era: "~400 BCE" },
    { name: "Soundarya Lahari", era: "~800 CE" }, { name: "Vivekachudamani", era: "~800 CE" },
  ];

  const visibleSamples = showMoreSamples ? sampleVerses : sampleVerses.slice(0, 4);

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
            <Link to="/login" className="text-sm text-[#75716B] hover:text-[#2C2A29] transition-colors px-4 py-2 rounded-lg hover:bg-[#F5F2EA]" data-testid="landing-login-btn">Sign In</Link>
            <Link to="/register" className="text-sm bg-[#2C2A29] text-[#FDFBF7] px-5 py-2 rounded-lg hover:bg-[#1a1918] transition-colors font-medium" data-testid="landing-register-btn">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-16 relative" data-testid="landing-hero">
        <div className="absolute inset-0 opacity-[0.03]" style={{backgroundImage: 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 256 256\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.9\' numOctaves=\'4\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noise)\'/%3E%3C/svg%3E")'}} />
        <div className="max-w-7xl mx-auto px-6">
          <div className="lg:grid lg:grid-cols-12 lg:gap-8 items-start">
            <div className="lg:col-span-7 lg:pr-8">
              <div className="inline-flex items-center gap-2 text-[#D97757] text-xs font-semibold tracking-widest uppercase mb-8">
                <div className="w-8 h-px bg-[#D97757]" />
                16 Sacred Texts &middot; 260+ Verses
              </div>
              <h1 className="font-heading text-4xl sm:text-5xl lg:text-[3.5rem] xl:text-6xl leading-[1.05] tracking-tight text-[#2C2A29] mb-6">
                The scriptures of<br className="hidden sm:block" /> ancient India,<br className="hidden sm:block" />
                <span className="text-[#D97757]">searchable.</span>
              </h1>
              <p className="text-base lg:text-lg text-[#75716B] leading-relaxed max-w-md mb-10">
                Search by meaning across the Gita, Ramayana, Upanishads, Narayaneeyam, and more. With Malayalam & Hindi transliterations, temple connections, and reading plans.
              </p>
              <div className="flex items-center gap-4 mb-12">
                <Link to="/register" className="group inline-flex items-center gap-2 bg-[#D97757] text-white px-7 py-3.5 rounded-lg font-medium hover:bg-[#C16648] transition-all" data-testid="hero-cta-btn">
                  Start Exploring <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </Link>
                <a href="#try-it" className="text-sm text-[#75716B] hover:text-[#2C2A29] transition-colors underline underline-offset-4 decoration-[#E8E3D9] hover:decoration-[#2C2A29]" data-testid="hero-try-btn">
                  Try it first
                </a>
              </div>
            </div>
            {/* Right: stacked quote cards */}
            <div className="lg:col-span-5 mt-8 lg:mt-0">
              <div className="space-y-3">
                <div className="bg-[#2C2A29] text-white rounded-xl p-7 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-[#D97757]/20 rounded-full -translate-y-1/2 translate-x-1/2 blur-2xl" />
                  <p className="font-scripture text-xl italic leading-relaxed relative z-10">"You have a right to perform your prescribed duty, but you are not entitled to the fruits of action."</p>
                  <div className="mt-3 flex items-center gap-2 relative z-10"><div className="w-1 h-4 bg-[#D97757] rounded-full" /><span className="text-sm text-white/60">Bhagavad Gita 2.47</span></div>
                </div>
                <div className="bg-white border border-[#E8E3D9] rounded-xl p-5">
                  <p className="font-scripture text-lg italic leading-relaxed text-[#2C2A29]">"Lead me from the unreal to the real, lead me from darkness to light."</p>
                  <div className="mt-2 flex items-center gap-2"><div className="w-1 h-3 bg-[#8A9A86] rounded-full" /><span className="text-xs text-[#A39E93]">Brihadaranyaka Upanishad</span></div>
                </div>
                <div className="bg-[#F5F2EA] rounded-xl p-5">
                  <p className="font-scripture text-lg italic leading-relaxed text-[#2C2A29]">"I behold a mass of radiance, the complete form of the inner Self."</p>
                  <div className="mt-2 flex items-center gap-2"><div className="w-1 h-3 bg-[#D97757] rounded-full" /><span className="text-xs text-[#A39E93]">Narayaneeyam 1.2 &middot; Guruvayur</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ===== TRY IT - Interactive Preview ===== */}
      <section id="try-it" className="py-20 border-t border-[#E8E3D9] bg-white" data-testid="landing-try-it">
        <div className="max-w-7xl mx-auto px-6">
          <div className="max-w-2xl mb-12">
            <div className="inline-flex items-center gap-2 text-[#D97757] text-xs font-semibold tracking-widest uppercase mb-4">
              <div className="w-8 h-px bg-[#D97757]" /> Try Before You Sign Up
            </div>
            <h2 className="font-heading text-2xl sm:text-3xl lg:text-4xl tracking-tight text-[#2C2A29] mb-3">
              Search the scriptures right now.
            </h2>
            <p className="text-base text-[#75716B]">
              Type any word — dharma, soul, devotion, Krishna, Goddess — and see real verses from our database. No account needed to preview.
            </p>
          </div>

          {/* Live search */}
          <form onSubmit={handleSearch} className="mb-8 max-w-xl" data-testid="public-search-form">
            <div className="flex gap-2">
              <input
                type="text"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Try: dharma, soul, karma, Guruvayur, Goddess..."
                className="flex-1 border border-[#E8E3D9] rounded-lg bg-[#FDFBF7] px-4 py-3 text-sm focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none transition-all text-[#2C2A29] placeholder:text-[#A39E93]"
                data-testid="public-search-input"
              />
              <button type="submit" disabled={searching || !searchQuery.trim()} className="bg-[#2C2A29] text-white rounded-lg px-5 py-3 text-sm font-medium hover:bg-[#1a1918] transition-colors disabled:opacity-40 flex items-center gap-2" data-testid="public-search-btn">
                <Search className="w-4 h-4" /> Search
              </button>
            </div>
          </form>

          {/* Search results */}
          {hasSearched && (
            <div className="mb-12 max-w-2xl" data-testid="public-search-results">
              {searching ? (
                <p className="text-sm text-[#75716B]">Searching...</p>
              ) : searchResults.length > 0 ? (
                <div>
                  <p className="text-xs text-[#A39E93] mb-3">{searchResults.length} result{searchResults.length > 1 ? 's' : ''} (showing up to 5 — sign up for full access)</p>
                  <div className="space-y-3">
                    {searchResults.map(v => <SampleVerseCard key={v.verse_id} verse={v} />)}
                  </div>
                  <div className="mt-4 p-4 bg-[#D97757]/5 border border-[#D97757]/20 rounded-lg flex items-center justify-between">
                    <p className="text-sm text-[#2C2A29]">Want AI-powered search, bookmarks, and reading plans?</p>
                    <Link to="/register" className="text-sm bg-[#D97757] text-white px-4 py-2 rounded-lg font-medium hover:bg-[#C16648] transition-colors" data-testid="search-results-cta">Sign Up Free</Link>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-[#75716B]">No results for "{searchQuery}". Try: dharma, soul, devotion, Om, Rama</p>
              )}
            </div>
          )}

          {/* Sample verses grid */}
          {!hasSearched && (
            <div>
              <p className="text-xs text-[#A39E93] uppercase tracking-wider mb-4">Sample Verses — Click to Explore</p>
              <div className="grid md:grid-cols-2 gap-3 max-w-4xl" data-testid="sample-verses-grid">
                {visibleSamples.map((v, i) => (
                  <SampleVerseCard key={v.verse_id} verse={v} defaultExpanded={i === 0} />
                ))}
              </div>
              {sampleVerses.length > 4 && (
                <button
                  onClick={() => setShowMoreSamples(!showMoreSamples)}
                  className="mt-4 text-sm text-[#D97757] hover:underline flex items-center gap-1"
                  data-testid="show-more-samples"
                >
                  {showMoreSamples ? <>Show fewer <ChevronUp className="w-3 h-3" /></> : <>Show {sampleVerses.length - 4} more verses <ChevronDown className="w-3 h-3" /></>}
                </button>
              )}
              <div className="mt-6 p-4 bg-[#D97757]/5 border border-[#D97757]/20 rounded-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 max-w-4xl">
                <div>
                  <p className="text-sm font-medium text-[#2C2A29]">Ready for the full experience?</p>
                  <p className="text-xs text-[#75716B]">AI search, reading plans, bookmarks, share as image, and 260+ verses</p>
                </div>
                <Link to="/register" className="text-sm bg-[#D97757] text-white px-5 py-2.5 rounded-lg font-medium hover:bg-[#C16648] transition-colors whitespace-nowrap" data-testid="sample-cta">Create Free Account</Link>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Features */}
      <section className="py-20 border-t border-[#E8E3D9]" data-testid="landing-features">
        <div className="max-w-7xl mx-auto px-6">
          <div className="lg:grid lg:grid-cols-12 lg:gap-16 items-start">
            <div className="lg:col-span-4 mb-12 lg:mb-0">
              <h2 className="font-heading text-2xl sm:text-3xl lg:text-4xl tracking-tight text-[#2C2A29] mb-4">Built for deep study.</h2>
              <p className="text-base text-[#75716B] leading-relaxed">Every feature designed to help you find, understand, and remember sacred knowledge.</p>
            </div>
            <div className="lg:col-span-8">
              <div className="grid sm:grid-cols-2 gap-x-8 gap-y-10">
                {[
                  { icon: Sparkles, title: "AI Semantic Search", desc: "Ask naturally: 'What does Krishna say about the soul?' — AI finds the right verses by meaning." },
                  { icon: Search, title: "Keyword Search", desc: "Quick text matching across 260+ verses from 16 texts. Filter by any scripture." },
                  { icon: Calendar, title: "Reading Plans", desc: "Structured study paths: 7 Days of Gita, Kerala's Devotional Heritage, Karkkidakam 30-day Ramayana, and more." },
                  { icon: Globe, title: "Transliterations", desc: "Read verses in Malayalam, Hindi, and other Indian scripts. Especially for Kerala's sacred texts." },
                  { icon: MapPin, title: "Temple Connections", desc: "Discover which temples are linked to each verse — Guruvayur, Padmanabhaswamy, Sabarimala, and more." },
                  { icon: Star, title: "Verse of the Day", desc: "A new verse each day from across all 16 texts. Start your morning with ancient wisdom." },
                ].map((f, i) => (
                  <div key={i}>
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

      {/* Texts grid */}
      <section className="py-20 bg-[#2C2A29]" data-testid="landing-texts">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center gap-3 mb-12">
            <div className="w-8 h-px bg-[#D97757]" />
            <h2 className="font-heading text-2xl sm:text-3xl text-white tracking-tight">Sixteen sacred texts, one search.</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
            {texts.map((t, i) => (
              <div key={i} className="group bg-white/5 border border-white/10 rounded-lg p-5 hover:bg-white/10 hover:border-[#D97757]/30 transition-all duration-300">
                <p className="font-heading text-lg text-white mb-1">{t.name}</p>
                <span className="text-[10px] text-[#D97757]/80">{t.era}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24">
        <div className="max-w-2xl mx-auto px-6 text-center">
          <h2 className="font-heading text-3xl sm:text-4xl tracking-tight text-[#2C2A29] mb-4">Begin your search.</h2>
          <p className="text-base text-[#75716B] mb-8">Free to use. No credit card required.</p>
          <Link to="/register" className="inline-flex items-center gap-2 bg-[#D97757] text-white px-8 py-4 rounded-lg font-medium hover:bg-[#C16648] transition-all text-lg" data-testid="cta-register-btn">
            Create Account <ArrowRight className="w-5 h-5" />
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
          <p className="text-xs text-[#A39E93]">16 texts &middot; 260+ verses &middot; AI-powered</p>
        </div>
      </footer>
    </div>
  );
}
