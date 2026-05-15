import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Bookmark, RefreshCw, BookOpen } from 'lucide-react';
import VerseCard from './VerseCard';

const API = process.env.REACT_APP_BACKEND_URL;

export default function BookmarksTab() {
  const [bookmarks, setBookmarks] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchBookmarks = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await axios.get(`${API}/api/bookmarks`, { withCredentials: true });
      setBookmarks(data);
    } catch (err) {
      console.error('Failed to load bookmarks', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchBookmarks(); }, [fetchBookmarks]);

  const handleBookmarkChange = (verseId, isBookmarked) => {
    if (!isBookmarked) setBookmarks(prev => prev.filter(v => v.verse_id !== verseId));
  };

  return (
    <div className="animate-fade-in" data-testid="bookmarks-section">
      <div className="mb-6">
        <h2 className="font-heading text-xl sm:text-2xl font-bold text-[#2C2A29] mb-1">Saved Verses</h2>
        <p className="text-xs text-[#A39E93]">Your personal collection of bookmarked scriptures</p>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <RefreshCw className="w-5 h-5 text-[#D97757] animate-spin" />
        </div>
      ) : bookmarks.length === 0 ? (
        <div className="text-center py-20 max-w-sm mx-auto">
          <div className="w-12 h-12 bg-[#D97757]/10 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Bookmark className="w-5 h-5 text-[#D97757]" />
          </div>
          <p className="text-sm text-[#2C2A29] font-medium mb-1">No saved verses yet</p>
          <p className="text-xs text-[#A39E93] leading-relaxed">
            Browse or search scriptures and tap the bookmark icon on any verse. It will appear here.
          </p>
        </div>
      ) : (
        <div data-testid="bookmarks-list">
          <p className="text-xs text-[#A39E93] mb-4">{bookmarks.length} saved verse{bookmarks.length > 1 ? 's' : ''}</p>
          <div className="space-y-3">
            {bookmarks.map(v => (
              <VerseCard key={v.verse_id} verse={v} isBookmarked={true} onBookmarkChange={handleBookmarkChange} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
