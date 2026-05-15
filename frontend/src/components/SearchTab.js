import React, { useState } from 'react';
import axios from 'axios';
import { Search, Sparkles, RefreshCw, Filter } from 'lucide-react';
import VerseCard from './VerseCard';

const API = process.env.REACT_APP_BACKEND_URL;

const textOptions = [
  { value: '', label: 'All Texts' },
  { value: 'bhagavad-gita', label: 'Bhagavad Gita' },
  { value: 'ramayana', label: 'Ramayana' },
  { value: 'devi-mahatmyam', label: 'Devi Mahatmyam' },
];

export default function SearchTab() {
  const [query, setQuery] = useState('');
  const [textFilter, setTextFilter] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchMode, setSearchMode] = useState('ai');
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setSearched(true);
    try {
      if (searchMode === 'ai') {
        const { data } = await axios.post(`${API}/api/ai-search`, {
          query: query.trim(),
          text_filter: textFilter || null
        }, { withCredentials: true });
        setResults(data);
      } else {
        const params = new URLSearchParams({ q: query.trim() });
        if (textFilter) params.append('text_filter', textFilter);
        const { data } = await axios.get(`${API}/api/search?${params}`);
        setResults(data);
      }
    } catch (err) {
      console.error('Search failed', err);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in-up" data-testid="search-section">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 bg-[#D97757]/10 rounded-xl flex items-center justify-center">
          <Sparkles className="w-5 h-5 text-[#D97757]" />
        </div>
        <div>
          <h2 className="font-heading text-2xl sm:text-3xl font-bold text-[#2C2A29]">Search Scriptures</h2>
          <p className="text-sm text-[#75716B]">Find verses by meaning or keywords</p>
        </div>
      </div>

      {/* Search Mode Toggle */}
      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setSearchMode('ai')}
          className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all ${
            searchMode === 'ai'
              ? 'bg-[#D97757] text-white'
              : 'bg-white border border-[#E8E3D9] text-[#75716B] hover:bg-[#F5F2EA]'
          }`}
          data-testid="search-mode-ai"
        >
          <Sparkles className="w-4 h-4" />
          AI Search
        </button>
        <button
          onClick={() => setSearchMode('keyword')}
          className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all ${
            searchMode === 'keyword'
              ? 'bg-[#D97757] text-white'
              : 'bg-white border border-[#E8E3D9] text-[#75716B] hover:bg-[#F5F2EA]'
          }`}
          data-testid="search-mode-keyword"
        >
          <Search className="w-4 h-4" />
          Keyword Search
        </button>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="mb-6" data-testid="search-form">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1 relative">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-[#A39E93]">
              {searchMode === 'ai' ? <Sparkles className="w-5 h-5" /> : <Search className="w-5 h-5" />}
            </div>
            <input
              type="text"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder={searchMode === 'ai' ? "Ask anything... e.g., 'verses about duty and righteousness'" : "Search by keyword..."}
              className="w-full rounded-full border border-[#E8E3D9] bg-white pl-12 pr-4 py-4 shadow-sm focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none transition-all text-[#2C2A29]"
              data-testid="search-input"
            />
          </div>
          <div className="flex gap-2">
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#A39E93]" />
              <select
                value={textFilter}
                onChange={e => setTextFilter(e.target.value)}
                className="appearance-none rounded-full border border-[#E8E3D9] bg-white pl-9 pr-8 py-4 text-sm text-[#2C2A29] focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none"
                data-testid="search-filter"
              >
                {textOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
              </select>
            </div>
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="bg-[#D97757] text-white rounded-full px-6 py-4 font-medium hover:bg-[#C16648] transition-colors disabled:opacity-50 flex items-center gap-2"
              data-testid="search-submit-btn"
            >
              {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
              Search
            </button>
          </div>
        </div>
        {searchMode === 'ai' && (
          <p className="text-xs text-[#A39E93] mt-2 ml-2">
            AI search understands meaning and context. Try natural language queries.
          </p>
        )}
      </form>

      {/* Results */}
      {loading && (
        <div className="flex flex-col items-center py-20">
          <RefreshCw className="w-8 h-8 text-[#D97757] animate-spin mb-3" />
          <p className="text-[#75716B]">{searchMode === 'ai' ? 'AI is searching through scriptures...' : 'Searching...'}</p>
        </div>
      )}

      {!loading && searched && results.length === 0 && (
        <div className="text-center py-16">
          <Search className="w-12 h-12 text-[#E8E3D9] mx-auto mb-3" />
          <p className="text-[#75716B]">No verses found. Try a different query or search mode.</p>
        </div>
      )}

      {!loading && results.length > 0 && (
        <div data-testid="search-results">
          <p className="text-sm text-[#75716B] mb-4">{results.length} verse{results.length > 1 ? 's' : ''} found</p>
          <div className="space-y-4">
            {results.map(v => <VerseCard key={v.verse_id} verse={v} />)}
          </div>
        </div>
      )}

      {!searched && !loading && (
        <div className="text-center py-16">
          <div className="w-16 h-16 bg-[#D97757]/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <Sparkles className="w-8 h-8 text-[#D97757]" />
          </div>
          <p className="font-heading text-xl text-[#2C2A29] mb-2">Search Ancient Wisdom</p>
          <p className="text-sm text-[#75716B] max-w-md mx-auto">
            {searchMode === 'ai'
              ? 'Ask in natural language, like "What does Krishna say about the eternal soul?" or "Verses about the power of the Goddess"'
              : 'Search for keywords like "dharma", "soul", "devotion", "Rama"'}
          </p>
        </div>
      )}
    </div>
  );
}
