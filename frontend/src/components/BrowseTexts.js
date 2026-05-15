import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Compass, ChevronRight, ArrowLeft, RefreshCw, BookOpen } from 'lucide-react';
import VerseCard from './VerseCard';

const API = process.env.REACT_APP_BACKEND_URL;

export default function BrowseTexts() {
  const [scriptures, setScriptures] = useState([]);
  const [selectedText, setSelectedText] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [selectedChapter, setSelectedChapter] = useState(null);
  const [verses, setVerses] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchScriptures();
  }, []);

  const fetchScriptures = async () => {
    try {
      const { data } = await axios.get(`${API}/api/scriptures`);
      setScriptures(data);
    } catch (err) {
      console.error('Failed to load scriptures', err);
    }
  };

  const selectText = async (textId) => {
    setSelectedText(textId);
    setSelectedChapter(null);
    setVerses([]);
    setLoading(true);
    try {
      const { data } = await axios.get(`${API}/api/scriptures/${textId}/chapters`);
      setChapters(data);
    } catch (err) {
      console.error('Failed to load chapters', err);
    } finally {
      setLoading(false);
    }
  };

  const selectChapter = async (chapter) => {
    setSelectedChapter(chapter);
    setLoading(true);
    try {
      const { data } = await axios.get(`${API}/api/scriptures/${selectedText}/chapters/${chapter}/verses`);
      setVerses(data);
    } catch (err) {
      console.error('Failed to load verses', err);
    } finally {
      setLoading(false);
    }
  };

  const goBack = () => {
    if (selectedChapter !== null) {
      setSelectedChapter(null);
      setVerses([]);
    } else if (selectedText) {
      setSelectedText(null);
      setChapters([]);
    }
  };

  const getTextName = (id) => scriptures.find(s => s.text_id === id)?.name || id;
  const getChapterName = (ch) => chapters.find(c => c.chapter === ch)?.chapter_name || `Chapter ${ch}`;

  const textImages = {
    'bhagavad-gita': 'https://images.unsplash.com/photo-1643300788512-64b38ad876c6?w=400',
    'ramayana': 'https://images.unsplash.com/photo-1617904472808-7e038208077a?w=400',
    'devi-mahatmyam': 'https://images.unsplash.com/photo-1488875482628-eee706cbfad5?w=400',
  };

  return (
    <div className="animate-fade-in-up" data-testid="browse-section">
      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        {(selectedText || selectedChapter !== null) && (
          <button onClick={goBack} className="text-[#75716B] hover:text-[#D97757] transition-colors" data-testid="browse-back-btn">
            <ArrowLeft className="w-5 h-5" />
          </button>
        )}
        <div className="w-10 h-10 bg-[#D97757]/10 rounded-xl flex items-center justify-center">
          <Compass className="w-5 h-5 text-[#D97757]" />
        </div>
        <div>
          <h2 className="font-heading text-2xl sm:text-3xl font-bold text-[#2C2A29]">
            {selectedChapter !== null
              ? `${getTextName(selectedText)} - ${getChapterName(selectedChapter)}`
              : selectedText
                ? getTextName(selectedText)
                : 'Browse Sacred Texts'}
          </h2>
          <p className="text-sm text-[#75716B]">
            {selectedChapter !== null
              ? `${verses.length} verses`
              : selectedText
                ? `${chapters.length} chapters`
                : 'Explore by text, chapter, and verse'}
          </p>
        </div>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-20">
          <RefreshCw className="w-6 h-6 text-[#D97757] animate-spin" />
        </div>
      )}

      {/* Scripture Selection */}
      {!selectedText && !loading && (
        <div className="grid md:grid-cols-3 gap-6" data-testid="scripture-list">
          {scriptures.map(s => (
            <button
              key={s.text_id}
              onClick={() => selectText(s.text_id)}
              className="group text-left bg-white border border-[#E8E3D9] rounded-2xl overflow-hidden hover:-translate-y-1 hover:shadow-md transition-all duration-300"
              data-testid={`scripture-${s.text_id}`}
            >
              <div className="relative h-40 overflow-hidden">
                <img
                  src={textImages[s.text_id] || s.image}
                  alt={s.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                <div className="absolute bottom-3 left-4 text-white">
                  <span className="text-xs bg-white/20 backdrop-blur-sm rounded-full px-2 py-0.5">{s.total_chapters} chapters</span>
                </div>
              </div>
              <div className="p-6">
                <h3 className="font-heading text-xl font-bold text-[#2C2A29] mb-2 group-hover:text-[#D97757] transition-colors">
                  {s.name}
                  <ChevronRight className="w-5 h-5 inline ml-1 opacity-0 group-hover:opacity-100 transition-opacity" />
                </h3>
                <p className="text-sm text-[#75716B] leading-relaxed line-clamp-2">{s.description}</p>
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Chapter Selection */}
      {selectedText && selectedChapter === null && !loading && (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4" data-testid="chapter-list">
          {chapters.map(c => (
            <button
              key={c.chapter}
              onClick={() => selectChapter(c.chapter)}
              className="group text-left bg-white border border-[#E8E3D9] rounded-2xl p-6 hover:-translate-y-1 hover:shadow-md transition-all duration-300"
              data-testid={`chapter-${c.chapter}`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="w-10 h-10 bg-[#D97757]/10 rounded-xl flex items-center justify-center mb-3">
                    <span className="font-heading text-lg font-bold text-[#D97757]">{c.chapter}</span>
                  </div>
                  <h3 className="font-heading text-lg font-bold text-[#2C2A29] group-hover:text-[#D97757] transition-colors">
                    {c.chapter_name || `Chapter ${c.chapter}`}
                  </h3>
                  <p className="text-sm text-[#75716B] mt-1">{c.verse_count} verse{c.verse_count > 1 ? 's' : ''}</p>
                </div>
                <ChevronRight className="w-5 h-5 text-[#A39E93] group-hover:text-[#D97757] transition-colors mt-2" />
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Verse List */}
      {selectedChapter !== null && !loading && (
        <div className="space-y-4" data-testid="verse-list">
          {verses.map(v => <VerseCard key={v.verse_id} verse={v} />)}
          {verses.length === 0 && (
            <div className="text-center py-16">
              <BookOpen className="w-12 h-12 text-[#E8E3D9] mx-auto mb-3" />
              <p className="text-[#75716B]">No verses found in this chapter.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
