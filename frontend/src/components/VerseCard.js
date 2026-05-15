import React, { useState, useRef, useCallback } from 'react';
import axios from 'axios';
import { Bookmark, BookmarkCheck, Share2, Copy, Check, Sparkles, RefreshCw, ChevronDown, ChevronUp, Image, Download, X, Globe, MapPin, AlertTriangle } from 'lucide-react';
import { toast } from 'sonner';
import { useAuth } from '../contexts/AuthContext';
import CommunityAnnotations from './CommunityAnnotations';
import CorrectionModal from './CorrectionModal';

const API = process.env.REACT_APP_BACKEND_URL;

const CARD_THEMES = [
  { bg: '#2C2A29', text: '#FDFBF7', accent: '#D97757', name: 'Dark' },
  { bg: '#FDFBF7', text: '#2C2A29', accent: '#D97757', name: 'Light' },
  { bg: '#1a2332', text: '#e8dfd0', accent: '#c9956b', name: 'Night' },
  { bg: '#f0e6d3', text: '#3d2b1f', accent: '#8A6552', name: 'Parchment' },
];

export default function VerseCard({ verse, expanded: initialExpanded = false, isBookmarked: initialBookmark = false, onBookmarkChange }) {
  const { user } = useAuth();
  const currentUserId = user?.id || user?._id || null;
  const [showExplanation, setShowExplanation] = useState(false);
  const [explanation, setExplanation] = useState('');
  const [loadingExplain, setLoadingExplain] = useState(false);
  const [bookmarked, setBookmarked] = useState(initialBookmark);
  const [bookmarkLoading, setBookmarkLoading] = useState(false);
  const [expanded, setExpanded] = useState(initialExpanded);
  const [copied, setCopied] = useState(false);
  const [showImageModal, setShowImageModal] = useState(false);
  const [selectedTheme, setSelectedTheme] = useState(0);
  const [transLang, setTransLang] = useState(null);
  const [showCorrection, setShowCorrection] = useState(false);
  const canvasRef = useRef(null);

  const LANG_LABELS = { ml: 'Malayalam', hi: 'Hindi', ta: 'Tamil', te: 'Telugu', kn: 'Kannada' };
  const availableTranslits = verse.transliterations ? Object.keys(verse.transliterations) : [];

  const handleExplain = async () => {
    if (explanation) { setShowExplanation(!showExplanation); return; }
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
      } else if (err.response?.status === 400) {
        setBookmarked(true);
      } else {
        toast.error('Failed to update bookmark');
      }
    } finally { setBookmarkLoading(false); }
  };

  const handleCopy = async () => {
    const text = `"${verse.translation}"\n\n- ${verse.text_name}, Chapter ${verse.chapter}, Verse ${verse.verse_number}`;
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true); toast.success('Copied to clipboard'); setTimeout(() => setCopied(false), 2000);
    } catch {
      const ta = document.createElement('textarea'); ta.value = text; ta.style.cssText = 'position:fixed;opacity:0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); setCopied(true); toast.success('Copied'); setTimeout(() => setCopied(false), 2000); } catch { toast.error('Could not copy'); }
      document.body.removeChild(ta);
    }
  };

  const handleShare = async () => {
    const text = `"${verse.translation}"\n\n- ${verse.text_name}, Chapter ${verse.chapter}, Verse ${verse.verse_number}`;
    if (navigator.share) { try { await navigator.share({ title: `${verse.text_name} ${verse.chapter}.${verse.verse_number}`, text }); } catch {} }
    else handleCopy();
  };

  // Share as image
  const generateImage = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const theme = CARD_THEMES[selectedTheme];
    const W = 1080, H = 1080;
    canvas.width = W; canvas.height = H;

    // Background
    ctx.fillStyle = theme.bg;
    ctx.fillRect(0, 0, W, H);

    // Decorative corner accent
    ctx.fillStyle = theme.accent;
    ctx.globalAlpha = 0.15;
    ctx.beginPath(); ctx.arc(0, 0, 200, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(W, H, 300, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = 1;

    // Top line accent
    ctx.fillStyle = theme.accent;
    ctx.fillRect(80, 80, 60, 4);

    // Source text
    ctx.font = '600 24px Manrope, sans-serif';
    ctx.fillStyle = theme.accent;
    ctx.fillText(`${verse.text_name}`, 80, 120);

    ctx.font = '400 18px Manrope, sans-serif';
    ctx.fillStyle = theme.text;
    ctx.globalAlpha = 0.5;
    ctx.fillText(`Chapter ${verse.chapter} · Verse ${verse.verse_number}`, 80, 150);
    ctx.globalAlpha = 1;

    // Quote text - word wrap
    const quote = `"${verse.translation}"`;
    ctx.font = 'italic 36px "Cormorant Garamond", Georgia, serif';
    ctx.fillStyle = theme.text;

    const maxWidth = W - 160;
    const words = quote.split(' ');
    let lines = [];
    let currentLine = '';
    for (const word of words) {
      const test = currentLine ? `${currentLine} ${word}` : word;
      if (ctx.measureText(test).width > maxWidth) {
        lines.push(currentLine);
        currentLine = word;
      } else {
        currentLine = test;
      }
    }
    if (currentLine) lines.push(currentLine);

    // Center the text block vertically
    const lineHeight = 52;
    const blockHeight = lines.length * lineHeight;
    const startY = Math.max(220, (H - blockHeight) / 2);

    lines.forEach((line, i) => {
      ctx.fillText(line, 80, startY + i * lineHeight);
    });

    // Bottom: chapter name
    if (verse.chapter_name) {
      ctx.font = '400 16px Manrope, sans-serif';
      ctx.fillStyle = theme.text;
      ctx.globalAlpha = 0.4;
      ctx.fillText(verse.chapter_name, 80, H - 100);
      ctx.globalAlpha = 1;
    }

    // Bottom branding
    ctx.font = '500 16px Manrope, sans-serif';
    ctx.fillStyle = theme.accent;
    ctx.fillText('DharmaSearch', 80, H - 60);

    ctx.fillStyle = theme.text;
    ctx.globalAlpha = 0.3;
    ctx.font = '400 14px Manrope, sans-serif';
    ctx.fillText('dharmasearch.app', W - 180, H - 60);
    ctx.globalAlpha = 1;
  }, [verse, selectedTheme]);

  const downloadImage = () => {
    generateImage();
    const canvas = canvasRef.current;
    if (!canvas) return;
    const link = document.createElement('a');
    link.download = `${verse.text_name}-${verse.chapter}-${verse.verse_number}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    toast.success('Image downloaded');
  };

  return (
    <>
      <div className="group bg-white border border-[#E8E3D9] rounded-xl overflow-hidden hover:border-[#D97757]/30 transition-all duration-300" data-testid={`verse-card-${verse.verse_id}`}>
        {/* Accent top bar */}
        <div className="h-0.5 bg-gradient-to-r from-[#D97757] via-[#D97757]/50 to-transparent" />

        <div className="p-5 sm:p-6">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div>
              <span className="text-xs font-semibold uppercase tracking-wider text-[#D97757]">
                {verse.text_name}
              </span>
              <p className="text-xs text-[#A39E93] mt-0.5">
                Ch. {verse.chapter}{verse.chapter_name ? ` · ${verse.chapter_name}` : ''} · V. {verse.verse_number}
              </p>
            </div>
            <div className="flex items-center gap-0.5">
              <button onClick={handleCopy} className="p-1.5 rounded-md text-[#A39E93] hover:text-[#D97757] hover:bg-[#D97757]/5 transition-all" title="Copy" data-testid={`copy-${verse.verse_id}`}>
                {copied ? <Check className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
              </button>
              <button onClick={() => { setShowImageModal(true); setTimeout(generateImage, 100); }} className="p-1.5 rounded-md text-[#A39E93] hover:text-[#D97757] hover:bg-[#D97757]/5 transition-all" title="Share as Image" data-testid={`image-${verse.verse_id}`}>
                <Image className="w-4 h-4" />
              </button>
              <button onClick={handleShare} className="p-1.5 rounded-md text-[#A39E93] hover:text-[#D97757] hover:bg-[#D97757]/5 transition-all" title="Share" data-testid={`share-${verse.verse_id}`}>
                <Share2 className="w-4 h-4" />
              </button>
              <button onClick={handleBookmark} disabled={bookmarkLoading} className={`p-1.5 rounded-md transition-all ${bookmarked ? 'text-[#D97757] bg-[#D97757]/10' : 'text-[#A39E93] hover:text-[#D97757] hover:bg-[#D97757]/5'}`} title={bookmarked ? 'Remove bookmark' : 'Bookmark'} data-testid={`bookmark-${verse.verse_id}`}>
                {bookmarked ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Sanskrit */}
          {verse.text && (
            <p className="font-scripture text-base sm:text-lg italic text-[#2C2A29]/40 leading-relaxed mb-3">
              {expanded ? verse.text : verse.text.substring(0, 120) + (verse.text.length > 120 ? '...' : '')}
            </p>
          )}

          {/* Translation */}
          <p className="text-[15px] text-[#2C2A29] leading-[1.7] mb-3">
            {expanded ? verse.translation : verse.translation.substring(0, 200) + (verse.translation.length > 200 ? '...' : '')}
          </p>

          {!expanded && (verse.translation.length > 200 || (verse.text && verse.text.length > 120)) && (
            <button onClick={() => setExpanded(true)} className="text-xs text-[#D97757] hover:underline flex items-center gap-1 mb-3" data-testid={`expand-${verse.verse_id}`}>
              Read more <ChevronDown className="w-3 h-3" />
            </button>
          )}
          {expanded && (verse.translation.length > 200 || (verse.text && verse.text.length > 120)) && (
            <button onClick={() => setExpanded(false)} className="text-xs text-[#D97757] hover:underline flex items-center gap-1 mb-3">
              Show less <ChevronUp className="w-3 h-3" />
            </button>
          )}

          {/* Keywords */}
          {verse.keywords && (
            <div className="flex flex-wrap gap-1 mb-3">
              {verse.keywords.split(',').slice(0, 5).map((k, i) => (
                <span key={i} className="text-[10px] bg-[#F5F2EA] text-[#75716B] rounded px-2 py-0.5">
                  {k.trim()}
                </span>
              ))}
            </div>
          )}

          {/* Transliteration toggle */}
          {availableTranslits.length > 0 && (
            <div className="mb-3">
              <div className="flex items-center gap-1 mb-2">
                <Globe className="w-3 h-3 text-[#A39E93]" />
                <span className="text-[10px] text-[#A39E93] uppercase tracking-wider">Script</span>
                {availableTranslits.map(lang => (
                  <button
                    key={lang}
                    onClick={() => setTransLang(transLang === lang ? null : lang)}
                    className={`text-[10px] px-2 py-0.5 rounded transition-all ${
                      transLang === lang ? 'bg-[#D97757] text-white' : 'bg-[#F5F2EA] text-[#75716B] hover:bg-[#E8E3D9]'
                    }`}
                    data-testid={`translit-${lang}-${verse.verse_id}`}
                  >
                    {LANG_LABELS[lang] || lang}
                  </button>
                ))}
                {transLang && (
                  <button onClick={() => setTransLang(null)} className="text-[10px] text-[#A39E93] hover:text-[#D97757] ml-1">
                    Reset
                  </button>
                )}
              </div>
              {transLang && verse.transliterations[transLang] && (
                <p className="text-sm leading-relaxed text-[#2C2A29]/70 bg-[#FDFBF7] border border-[#E8E3D9] rounded-lg p-3 animate-slide-down" data-testid={`translit-text-${verse.verse_id}`}>
                  {verse.transliterations[transLang]}
                </p>
              )}
            </div>
          )}

          {/* Temple connection */}
          {verse.temple_connection && (
            <div className="mb-3 bg-amber-50/50 border border-amber-200/30 rounded-lg p-3" data-testid={`temple-${verse.verse_id}`}>
              <div className="flex items-start gap-2">
                <MapPin className="w-3.5 h-3.5 text-amber-600 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-xs font-medium text-amber-800">{verse.temple_connection.temple}</p>
                  <p className="text-[10px] text-amber-600">{verse.temple_connection.location}</p>
                  <p className="text-xs text-amber-700/80 mt-1 leading-relaxed">{verse.temple_connection.detail}</p>
                </div>
              </div>
            </div>
          )}

          {/* Actions row */}
          <div className="pt-3 border-t border-[#E8E3D9]/50 flex items-center gap-4 flex-wrap">
            <button onClick={handleExplain} className="flex items-center gap-1.5 text-xs font-medium text-[#D97757] hover:text-[#C16648] transition-colors" data-testid={`explain-${verse.verse_id}`}>
              {loadingExplain ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
              {showExplanation ? 'Hide Explanation' : 'AI Explanation'}
            </button>
            <CommunityAnnotations verseId={verse.verse_id} verseName={verse.text_name} currentUserId={currentUserId} />
            <button onClick={() => setShowCorrection(true)} className="flex items-center gap-1.5 text-xs font-medium text-[#A39E93] hover:text-[#D97757] transition-colors" data-testid={`correction-btn-${verse.verse_id}`}>
              <AlertTriangle className="w-3.5 h-3.5" />
              Suggest Correction
            </button>
          </div>

          {/* Explanation panel */}
          {showExplanation && (
            <div className="mt-3 bg-[#FDFBF7] border border-[#E8E3D9] rounded-lg p-4 animate-slide-down" data-testid={`explanation-${verse.verse_id}`}>
              {loadingExplain ? (
                <div className="flex items-center gap-2 text-[#75716B]">
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span className="text-xs">Generating explanation...</span>
                </div>
              ) : (
                <div className="text-sm text-[#2C2A29] leading-relaxed whitespace-pre-line">{explanation}</div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Correction Modal */}
      {showCorrection && (
        <CorrectionModal verse={verse} onClose={() => setShowCorrection(false)} />
      )}

      {/* Share as Image Modal */}
      {showImageModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4" data-testid="image-modal">
          <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={() => setShowImageModal(false)} />
          <div className="relative bg-white rounded-xl shadow-2xl max-w-lg w-full p-6 max-h-[90vh] overflow-y-auto animate-fade-in">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-heading text-xl font-bold text-[#2C2A29]">Share as Image</h3>
              <button onClick={() => setShowImageModal(false)} className="p-1 text-[#A39E93] hover:text-[#2C2A29]" data-testid="image-modal-close">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Theme selector */}
            <div className="flex gap-2 mb-4">
              {CARD_THEMES.map((t, i) => (
                <button
                  key={i}
                  onClick={() => { setSelectedTheme(i); setTimeout(generateImage, 50); }}
                  className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                    selectedTheme === i ? 'border-[#D97757] bg-[#D97757]/5 text-[#D97757]' : 'border-[#E8E3D9] text-[#75716B] hover:bg-[#F5F2EA]'
                  }`}
                  data-testid={`theme-${t.name.toLowerCase()}`}
                >
                  <div className="w-4 h-4 rounded-full border" style={{backgroundColor: t.bg, borderColor: t.accent}} />
                  {t.name}
                </button>
              ))}
            </div>

            {/* Canvas preview */}
            <div className="border border-[#E8E3D9] rounded-lg overflow-hidden mb-4">
              <canvas ref={canvasRef} className="w-full" style={{aspectRatio: '1/1'}} />
            </div>

            <button
              onClick={downloadImage}
              className="w-full flex items-center justify-center gap-2 bg-[#D97757] text-white py-3 rounded-lg font-medium hover:bg-[#C16648] transition-colors"
              data-testid="download-image-btn"
            >
              <Download className="w-4 h-4" />
              Download Image
            </button>
          </div>
        </div>
      )}
    </>
  );
}
