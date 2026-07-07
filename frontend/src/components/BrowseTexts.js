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

  useEffect(() => { fetchScriptures(); }, []);

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
    if (selectedChapter !== null) { setSelectedChapter(null); setVerses([]); }
    else if (selectedText) { setSelectedText(null); setChapters([]); }
  };

  const getTextName = (id) => scriptures.find(s => s.text_id === id)?.name || id;
  const getChapterName = (ch) => chapters.find(c => c.chapter === ch)?.chapter_name || `Chapter ${ch}`;

  // Breadcrumb
  const crumbs = ['All Texts'];
  if (selectedText) crumbs.push(getTextName(selectedText));
  if (selectedChapter !== null) crumbs.push(getChapterName(selectedChapter));

  return (
    <div className="animate-fade-in" data-testid="browse-section">
      {/* Breadcrumb */}
      <div className="flex items-center gap-1.5 text-xs text-[#A39E93] mb-6">
        {crumbs.map((c, i) => (
          <React.Fragment key={i}>
            {i > 0 && <ChevronRight className="w-3 h-3" />}
            <span className={i === crumbs.length - 1 ? 'text-[#2C2A29] font-medium' : 'cursor-pointer hover:text-[#D97757]'} onClick={() => {
              if (i === 0) { setSelectedText(null); setSelectedChapter(null); setChapters([]); setVerses([]); }
              else if (i === 1 && selectedChapter !== null) { setSelectedChapter(null); setVerses([]); }
            }}>
              {c}
            </span>
          </React.Fragment>
        ))}
      </div>

      {/* Header */}
      <div className="flex items-center gap-3 mb-6">
        {(selectedText || selectedChapter !== null) && (
          <button onClick={goBack} className="p-1.5 rounded-lg text-[#75716B] hover:text-[#D97757] hover:bg-[#D97757]/5 transition-all" data-testid="browse-back-btn">
            <ArrowLeft className="w-4 h-4" />
          </button>
        )}
        <div>
          <h2 className="font-heading text-xl sm:text-2xl font-bold text-[#2C2A29]">
            {selectedChapter !== null
              ? getChapterName(selectedChapter)
              : selectedText
                ? getTextName(selectedText)
                : 'Sacred Texts'}
          </h2>
          <p className="text-xs text-[#A39E93]">
            {selectedChapter !== null
              ? `${verses.length} verses`
              : selectedText
                ? `${chapters.length} chapters`
                : `${scriptures.length} texts available`}
          </p>
        </div>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-20">
          <RefreshCw className="w-5 h-5 text-[#D97757] animate-spin" />
        </div>
      )}

      {/* Scripture list — flat table-like */}
      {!selectedText && !loading && (
        <div className="space-y-1" data-testid="scripture-list">
          {scriptures.map((s, i) => (
            <button
              key={s.text_id}
              onClick={() => selectText(s.text_id)}
              className="group w-full flex items-center gap-4 p-4 bg-white border border-[#E8E3D9] rounded-lg hover:border-[#D97757]/30 hover:bg-[#D97757]/[0.02] transition-all text-left"
              data-testid={`scripture-${s.text_id}`}
            >
              <div className="w-10 h-10 rounded-lg bg-[#D97757]/10 flex items-center justify-center flex-shrink-0">
                <span className="font-heading text-sm font-bold text-[#D97757]">{i + 1}</span>
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="font-heading text-base font-bold text-[#2C2A29] group-hover:text-[#D97757] transition-colors">
                    {s.name}
                  </h3>
                  <span className="text-[10px] text-[#A39E93] bg-[#F5F2EA] px-2 py-0.5 rounded">{s.language}</span>
                </div>
                <p className="text-xs text-[#75716B] mt-0.5 truncate">{s.description}</p>
              </div>
              <div className="text-right flex-shrink-0">
                <p className="text-xs text-[#A39E93]">{s.total_chapters} ch. &middot; {s.total_verses || '—'} v.</p>
              </div>
              <ChevronRight className="w-4 h-4 text-[#E8E3D9] group-hover:text-[#D97757] transition-colors flex-shrink-0" />
            </button>
          ))}
        </div>
      )}

      {/* Chapter list */}
      {selectedText && selectedChapter === null && !loading && (
        <div className="space-y-1" data-testid="chapter-list">
          {chapters.map(c => (
            <button
              key={c.chapter}
              onClick={() => selectChapter(c.chapter)}
              className="group w-full flex items-center gap-4 p-4 bg-white border border-[#E8E3D9] rounded-lg hover:border-[#D97757]/30 hover:bg-[#D97757]/[0.02] transition-all text-left"
              data-testid={`chapter-${c.chapter}`}
            >
              <div className="w-8 h-8 rounded bg-[#F5F2EA] flex items-center justify-center flex-shrink-0">
                <span className="text-xs font-bold text-[#75716B]">{c.chapter}</span>
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-medium text-[#2C2A29] group-hover:text-[#D97757] transition-colors">
                  {c.chapter_name || `Chapter ${c.chapter}`}
                </h3>
              </div>
              <span className="text-xs text-[#A39E93] flex-shrink-0">{c.verse_count} v.</span>
              <ChevronRight className="w-4 h-4 text-[#E8E3D9] group-hover:text-[#D97757] transition-colors flex-shrink-0" />
            </button>
          ))}
        </div>
      )}

      {/* Verse list */}
      {selectedChapter !== null && !loading && (
        <div className="space-y-3" data-testid="verse-list">
          {verses.map(v => <VerseCard key={v.verse_id} verse={v} />)}
          {verses.length === 0 && (
            <div className="text-center py-16">
              <BookOpen className="w-10 h-10 text-[#E8E3D9] mx-auto mb-3" />
              <p className="text-sm text-[#75716B]">No verses in this chapter.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
