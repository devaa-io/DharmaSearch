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

  useEffect(() => {
    fetchBookmarks();
  }, [fetchBookmarks]);

  const handleBookmarkChange = (verseId, isBookmarked) => {
    if (!isBookmarked) {
      setBookmarks(prev => prev.filter(v => v.verse_id !== verseId));
    }
  };

  return (
    <div className="animate-fade-in-up" data-testid="bookmarks-section">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 bg-[#D97757]/10 rounded-xl flex items-center justify-center">
          <Bookmark className="w-5 h-5 text-[#D97757]" />
        </div>
        <div>
          <h2 className="font-heading text-2xl sm:text-3xl font-bold text-[#2C2A29]">Saved Verses</h2>
          <p className="text-sm text-[#75716B]">Your bookmarked scriptures</p>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <RefreshCw className="w-6 h-6 text-[#D97757] animate-spin" />
        </div>
      ) : bookmarks.length === 0 ? (
        <div className="text-center py-20">
          <div className="w-16 h-16 bg-[#D97757]/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <BookOpen className="w-8 h-8 text-[#D97757]" />
          </div>
          <p className="font-heading text-xl text-[#2C2A29] mb-2">No saved verses yet</p>
          <p className="text-sm text-[#75716B] max-w-md mx-auto">
            Browse or search scriptures and bookmark the verses that resonate with you. They'll appear here for easy access.
          </p>
        </div>
      ) : (
        <div data-testid="bookmarks-list">
          <p className="text-sm text-[#75716B] mb-4">{bookmarks.length} saved verse{bookmarks.length > 1 ? 's' : ''}</p>
          <div className="space-y-4">
            {bookmarks.map(v => (
              <VerseCard key={v.verse_id} verse={v} isBookmarked={true} onBookmarkChange={handleBookmarkChange} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
