import React, { useState } from 'react';
import axios from 'axios';
import { Bookmark, BookmarkCheck, Share2, Copy, Check, Sparkles, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';
import { toast } from 'sonner';

const API = process.env.REACT_APP_BACKEND_URL;

export default function VerseCard({ verse, expanded: initialExpanded = false, isBookmarked: initialBookmark = false, onBookmarkChange }) {
  const [showExplanation, setShowExplanation] = useState(false);
  const [explanation, setExplanation] = useState('');
  const [loadingExplain, setLoadingExplain] = useState(false);
  const [bookmarked, setBookmarked] = useState(initialBookmark);
  const [bookmarkLoading, setBookmarkLoading] = useState(false);
  const [expanded, setExpanded] = useState(initialExpanded);
  const [copied, setCopied] = useState(false);

  const handleExplain = async () => {
    if (explanation) {
      setShowExplanation(!showExplanation);
      return;
    }
    setLoadingExplain(true);
    setShowExplanation(true);
    try {
      const { data } = await axios.post(`${API}/api/ai-explain`, { verse_id: verse.verse_id }, { withCredentials: true });
      setExplanation(data.explanation);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setExplanation(typeof detail === 'string' ? detail : 'Failed to load explanation. Please try again.');
    } finally {
      setLoadingExplain(false);
    }
  };

  const handleBookmark = async () => {
    setBookmarkLoading(true);
    try {
      if (bookmarked) {
        await axios.delete(`${API}/api/bookmarks/${verse.verse_id}`, { withCredentials: true });
        setBookmarked(false);
        toast.success('Bookmark removed');
        if (onBookmarkChange) onBookmarkChange(verse.verse_id, false);
      } else {
        await axios.post(`${API}/api/bookmarks`, { verse_id: verse.verse_id }, { withCredentials: true });
        setBookmarked(true);
        toast.success('Verse bookmarked');
        if (onBookmarkChange) onBookmarkChange(verse.verse_id, true);
      }
    } catch (err) {
      const msg = err.response?.data?.detail;
      if (typeof msg === 'string' && msg.includes('Already')) {
        setBookmarked(true);
      } else {
        toast.error('Failed to update bookmark');
      }
    } finally {
      setBookmarkLoading(false);
    }
  };

  const handleCopy = async () => {
    const text = `"${verse.translation}"\n\n— ${verse.text_name}, Chapter ${verse.chapter}, Verse ${verse.verse_number}`;
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      toast.success('Copied to clipboard');
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback for non-clipboard environments
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      try { document.execCommand('copy'); setCopied(true); toast.success('Copied to clipboard'); setTimeout(() => setCopied(false), 2000); } catch { toast.error('Could not copy text'); }
      document.body.removeChild(textarea);
    }
  };

  const handleShare = async () => {
    const text = `"${verse.translation}"\n\n— ${verse.text_name}, Chapter ${verse.chapter}, Verse ${verse.verse_number}`;
    if (navigator.share) {
      try {
        await navigator.share({ title: `${verse.text_name} ${verse.chapter}.${verse.verse_number}`, text });
      } catch {}
    } else {
      handleCopy();
    }
  };

  return (
    <div className="bg-white border border-[#E8E3D9] rounded-2xl p-6 sm:p-8 hover:shadow-md transition-all duration-300" data-testid={`verse-card-${verse.verse_id}`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs font-medium bg-[#D97757]/10 text-[#D97757] rounded-full px-3 py-1">
            {verse.text_name}
          </span>
          <span className="text-xs text-[#A39E93]">
            Ch. {verse.chapter} {verse.chapter_name ? `· ${verse.chapter_name}` : ''} · V. {verse.verse_number}
          </span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={handleCopy}
            className="p-2 rounded-full text-[#A39E93] hover:text-[#D97757] hover:bg-[#D97757]/10 transition-all"
            title="Copy"
            data-testid={`copy-${verse.verse_id}`}
          >
            {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
          </button>
          <button
            onClick={handleShare}
            className="p-2 rounded-full text-[#A39E93] hover:text-[#D97757] hover:bg-[#D97757]/10 transition-all"
            title="Share"
            data-testid={`share-${verse.verse_id}`}
          >
            <Share2 className="w-4 h-4" />
          </button>
          <button
            onClick={handleBookmark}
            disabled={bookmarkLoading}
            className={`p-2 rounded-full transition-all ${bookmarked ? 'text-[#D97757] bg-[#D97757]/10' : 'text-[#A39E93] hover:text-[#D97757] hover:bg-[#D97757]/10'}`}
            title={bookmarked ? 'Remove bookmark' : 'Bookmark'}
            data-testid={`bookmark-${verse.verse_id}`}
          >
            {bookmarked ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Sanskrit text */}
      {verse.text && (
        <p className="font-scripture text-lg sm:text-xl italic text-[#2C2A29]/60 leading-relaxed mb-3">
          {expanded ? verse.text : verse.text.substring(0, 150) + (verse.text.length > 150 ? '...' : '')}
        </p>
      )}

      {/* Translation */}
      <p className="text-base text-[#2C2A29] leading-relaxed mb-4">
        {expanded ? verse.translation : verse.translation.substring(0, 200) + (verse.translation.length > 200 ? '...' : '')}
      </p>

      {!expanded && (verse.translation.length > 200 || (verse.text && verse.text.length > 150)) && (
        <button onClick={() => setExpanded(true)} className="text-sm text-[#D97757] hover:underline flex items-center gap-1 mb-3" data-testid={`expand-${verse.verse_id}`}>
          Read more <ChevronDown className="w-3 h-3" />
        </button>
      )}

      {expanded && (
        <button onClick={() => setExpanded(false)} className="text-sm text-[#D97757] hover:underline flex items-center gap-1 mb-3">
          Show less <ChevronUp className="w-3 h-3" />
        </button>
      )}

      {/* Keywords */}
      {verse.keywords && (
        <div className="flex flex-wrap gap-1.5 mb-4">
          {verse.keywords.split(',').map((k, i) => (
            <span key={i} className="text-xs bg-[#F5F2EA] text-[#75716B] rounded-full px-2.5 py-0.5">
              {k.trim()}
            </span>
          ))}
        </div>
      )}

      {/* AI Explain */}
      <button
        onClick={handleExplain}
        className="flex items-center gap-2 text-sm font-medium text-[#D97757] hover:text-[#C16648] transition-colors"
        data-testid={`explain-${verse.verse_id}`}
      >
        {loadingExplain ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
        {showExplanation ? 'Hide Explanation' : 'AI Explanation'}
      </button>

      {showExplanation && (
        <div className="mt-4 bg-[#FDFBF7] border border-[#E8E3D9] rounded-xl p-4 animate-slide-down" data-testid={`explanation-${verse.verse_id}`}>
          {loadingExplain ? (
            <div className="flex items-center gap-2 text-[#75716B]">
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span className="text-sm">Generating explanation...</span>
            </div>
          ) : (
            <div className="text-sm text-[#2C2A29] leading-relaxed whitespace-pre-line">{explanation}</div>
          )}
        </div>
      )}
    </div>
  );
}
