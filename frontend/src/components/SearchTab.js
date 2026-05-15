import React, { useState } from 'react';
import axios from 'axios';
import { Search, Sparkles, RefreshCw } from 'lucide-react';
import { toast } from 'sonner';
import VerseCard from './VerseCard';

const API = process.env.REACT_APP_BACKEND_URL;

const textOptions = [
  { value: '', label: 'All Texts' },
  { value: 'bhagavad-gita', label: 'Bhagavad Gita' },
  { value: 'ramayana', label: 'Ramayana' },
  { value: 'devi-mahatmyam', label: 'Devi Mahatmyam' },
  { value: 'upanishads', label: 'Upanishads' },
  { value: 'yoga-sutras', label: 'Yoga Sutras' },
  { value: 'mahabharata', label: 'Mahabharata' },
  { value: 'vedas', label: 'Vedas' },
  { value: 'hanuman-chalisa', label: 'Hanuman Chalisa' },
  { value: 'puranas', label: 'Puranas' },
  { value: 'srimad-bhagavatam', label: 'Srimad Bhagavatam' },
  { value: 'narayaneeyam', label: 'Narayaneeyam' },
  { value: 'adhyatma-ramayanam', label: 'Adhyatma Ramayanam' },
  { value: 'lalita-sahasranama', label: 'Lalita Sahasranama' },
  { value: 'vishnu-sahasranama', label: 'Vishnu Sahasranama' },
  { value: 'soundarya-lahari', label: 'Soundarya Lahari' },
  { value: 'vivekachudamani', label: 'Vivekachudamani' },
];

export default function SearchTab() {
  const [query, setQuery] = useState('');
  const [textFilter, setTextFilter] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchMode, setSearchMode] = useState('keyword');
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
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') toast.error(detail);
      else toast.error(searchMode === 'ai' ? 'AI search unavailable. Try keyword search.' : 'Search failed.');
      setResults([]);
      setSearched('error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in" data-testid="search-section">
      {/* Header */}
      <div className="mb-6">
        <h2 className="font-heading text-xl sm:text-2xl font-bold text-[#2C2A29] mb-1">Search Scriptures</h2>
        <p className="text-xs text-[#A39E93]">Find verses by meaning or exact keywords across 9 sacred texts</p>
      </div>

      {/* Mode toggle */}
      <div className="flex gap-1 p-1 bg-[#F5F2EA] rounded-lg w-fit mb-5">
        <button
          onClick={() => setSearchMode('ai')}
          className={`flex items-center gap-1.5 px-4 py-2 rounded-md text-xs font-medium transition-all ${
            searchMode === 'ai' ? 'bg-white text-[#2C2A29] shadow-sm' : 'text-[#75716B] hover:text-[#2C2A29]'
          }`}
          data-testid="search-mode-ai"
        >
          <Sparkles className="w-3.5 h-3.5" />
          AI Search
        </button>
        <button
          onClick={() => setSearchMode('keyword')}
          className={`flex items-center gap-1.5 px-4 py-2 rounded-md text-xs font-medium transition-all ${
            searchMode === 'keyword' ? 'bg-white text-[#2C2A29] shadow-sm' : 'text-[#75716B] hover:text-[#2C2A29]'
          }`}
          data-testid="search-mode-keyword"
        >
          <Search className="w-3.5 h-3.5" />
          Keyword
        </button>
      </div>

      {/* Search form */}
      <form onSubmit={handleSearch} className="mb-8" data-testid="search-form">
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <input
              type="text"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder={searchMode === 'ai' ? "e.g., 'What does Krishna say about the eternal soul?'" : "Search for: dharma, soul, devotion..."}
              className="w-full border border-[#E8E3D9] rounded-lg bg-white pl-4 pr-4 py-3 text-sm focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none transition-all text-[#2C2A29] placeholder:text-[#A39E93]"
              data-testid="search-input"
            />
          </div>
          <select
            value={textFilter}
            onChange={e => setTextFilter(e.target.value)}
            className="border border-[#E8E3D9] rounded-lg bg-white px-3 py-3 text-xs text-[#2C2A29] focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none hidden sm:block"
            data-testid="search-filter"
          >
            {textOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="bg-[#2C2A29] text-white rounded-lg px-5 py-3 text-sm font-medium hover:bg-[#1a1918] transition-colors disabled:opacity-40 flex items-center gap-2"
            data-testid="search-submit-btn"
          >
            {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
            <span className="hidden sm:inline">Search</span>
          </button>
        </div>
        {/* Mobile filter */}
        <select
          value={textFilter}
          onChange={e => setTextFilter(e.target.value)}
          className="sm:hidden mt-2 w-full border border-[#E8E3D9] rounded-lg bg-white px-3 py-2.5 text-xs text-[#2C2A29]"
        >
          {textOptions.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
      </form>

      {/* Results */}
      {loading && (
        <div className="flex flex-col items-center py-20">
          <RefreshCw className="w-5 h-5 text-[#D97757] animate-spin mb-3" />
          <p className="text-xs text-[#75716B]">{searchMode === 'ai' ? 'AI is searching through scriptures...' : 'Searching...'}</p>
        </div>
      )}

      {!loading && searched && results.length === 0 && (
        <div className="text-center py-16">
          <p className="text-sm text-[#75716B]">
            {searched === 'error'
              ? 'Search service is unavailable. Please try keyword search mode.'
              : 'No verses found. Try different words or another text filter.'}
          </p>
        </div>
      )}

      {!loading && results.length > 0 && (
        <div data-testid="search-results">
          <p className="text-xs text-[#A39E93] mb-4">{results.length} result{results.length > 1 ? 's' : ''}</p>
          <div className="space-y-3">
            {results.map(v => <VerseCard key={v.verse_id} verse={v} />)}
          </div>
        </div>
      )}

      {!searched && !loading && (
        <div className="text-center py-16 max-w-sm mx-auto">
          <div className="w-12 h-12 bg-[#D97757]/10 rounded-lg flex items-center justify-center mx-auto mb-4">
            {searchMode === 'ai' ? <Sparkles className="w-5 h-5 text-[#D97757]" /> : <Search className="w-5 h-5 text-[#D97757]" />}
          </div>
          <p className="text-sm text-[#2C2A29] font-medium mb-1">
            {searchMode === 'ai' ? 'Ask a question' : 'Search by keyword'}
          </p>
          <p className="text-xs text-[#A39E93] leading-relaxed">
            {searchMode === 'ai'
              ? 'Try: "verses about the nature of the soul" or "What does the Ramayana say about duty?"'
              : 'Try: "dharma", "soul", "devotion", "karma", "meditation"'}
          </p>
        </div>
      )}
    </div>
  );
}
