import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { MessageCircle, ThumbsUp, ThumbsDown, Send, Trash2, CheckCircle, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';
import { toast } from 'sonner';

const API = process.env.REACT_APP_BACKEND_URL;

const TRADITIONS = [
  { value: '', label: 'General' },
  { value: 'advaita', label: 'Advaita (Shankaracharya)' },
  { value: 'vishishtadvaita', label: 'Vishishtadvaita (Ramanuja)' },
  { value: 'dvaita', label: 'Dvaita (Madhva)' },
  { value: 'shaiva', label: 'Shaiva Siddhanta' },
  { value: 'shakta', label: 'Shakta' },
  { value: 'bhakti', label: 'Bhakti Movement' },
];

export default function CommunityAnnotations({ verseId, verseName, currentUserId }) {
  const [annotations, setAnnotations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [text, setText] = useState('');
  const [tradition, setTradition] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const fetchAnnotations = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await axios.get(`${API}/api/annotations/${verseId}`);
      setAnnotations(data);
    } catch {}
    finally { setLoading(false); }
  }, [verseId]);

  useEffect(() => {
    if (expanded) fetchAnnotations();
  }, [expanded, fetchAnnotations]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    setSubmitting(true);
    try {
      const { data } = await axios.post(`${API}/api/annotations`, {
        verse_id: verseId, text: text.trim(), tradition: tradition || null
      }, { withCredentials: true });
      setAnnotations(prev => [data, ...prev]);
      setText('');
      setTradition('');
      setShowForm(false);
      toast.success('Interpretation shared');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to post');
    } finally { setSubmitting(false); }
  };

  const handleVote = async (annotationId, vote) => {
    try {
      const { data } = await axios.post(`${API}/api/annotations/${annotationId}/vote`, { vote }, { withCredentials: true });
      if (data.message === 'Already voted') return;
      // Refetch to get accurate counts
      fetchAnnotations();
    } catch {}
  };

  const handleDelete = async (annotationId) => {
    try {
      await axios.delete(`${API}/api/annotations/${annotationId}`, { withCredentials: true });
      setAnnotations(prev => prev.filter(a => a.annotation_id !== annotationId));
      toast.success('Deleted');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Cannot delete');
    }
  };

  const traditionLabel = (t) => TRADITIONS.find(tr => tr.value === t)?.label || t || 'General';

  return (
    <div data-testid={`community-${verseId}`}>
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-1.5 text-xs font-medium text-[#8A9A86] hover:text-[#6b7d67] transition-colors"
        data-testid={`toggle-community-${verseId}`}
      >
        <MessageCircle className="w-3.5 h-3.5" />
        Community
        {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
      </button>

      {expanded && (
        <div className="mt-3 animate-slide-down" data-testid={`annotations-panel-${verseId}`}>
          {/* Add interpretation button */}
          {!showForm && (
            <button
              onClick={() => setShowForm(true)}
              className="w-full flex items-center justify-center gap-1.5 py-2.5 border border-dashed border-[#E8E3D9] rounded-lg text-xs text-[#75716B] hover:border-[#D97757] hover:text-[#D97757] transition-all mb-3"
              data-testid={`add-annotation-${verseId}`}
            >
              <MessageCircle className="w-3.5 h-3.5" />
              Share your interpretation
            </button>
          )}

          {/* Form */}
          {showForm && (
            <form onSubmit={handleSubmit} className="bg-[#FDFBF7] border border-[#E8E3D9] rounded-lg p-3 mb-3" data-testid={`annotation-form-${verseId}`}>
              <textarea
                value={text}
                onChange={e => setText(e.target.value)}
                placeholder="Share your understanding of this verse..."
                className="w-full border border-[#E8E3D9] rounded-lg px-3 py-2 text-sm bg-white focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none resize-none min-h-[80px]"
                data-testid={`annotation-text-${verseId}`}
              />
              <div className="flex items-center gap-2 mt-2">
                <select
                  value={tradition}
                  onChange={e => setTradition(e.target.value)}
                  className="border border-[#E8E3D9] rounded-lg px-2 py-1.5 text-xs bg-white text-[#2C2A29] focus:ring-2 focus:ring-[#D97757] outline-none"
                  data-testid={`annotation-tradition-${verseId}`}
                >
                  {TRADITIONS.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                </select>
                <div className="flex-1" />
                <button type="button" onClick={() => setShowForm(false)} className="text-xs text-[#A39E93] hover:text-[#75716B] px-3 py-1.5">Cancel</button>
                <button type="submit" disabled={submitting || !text.trim()} className="flex items-center gap-1 bg-[#D97757] text-white px-3 py-1.5 rounded-lg text-xs font-medium hover:bg-[#C16648] disabled:opacity-40 transition-colors" data-testid={`submit-annotation-${verseId}`}>
                  <Send className="w-3 h-3" /> {submitting ? 'Posting...' : 'Post'}
                </button>
              </div>
            </form>
          )}

          {/* Annotations list */}
          {loading ? (
            <div className="flex items-center justify-center py-4">
              <RefreshCw className="w-4 h-4 text-[#D97757] animate-spin" />
            </div>
          ) : annotations.length === 0 ? (
            <p className="text-xs text-[#A39E93] text-center py-4">No interpretations yet. Be the first to share yours.</p>
          ) : (
            <div className="space-y-2">
              {annotations.map(a => (
                <div key={a.annotation_id} className="bg-white border border-[#E8E3D9] rounded-lg p-3" data-testid={`annotation-${a.annotation_id}`}>
                  <div className="flex items-start justify-between mb-1.5">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-[#2C2A29]">{a.user_name}</span>
                      {a.tradition && (
                        <span className="text-[10px] bg-[#8A9A86]/10 text-[#8A9A86] rounded px-1.5 py-0.5">{traditionLabel(a.tradition)}</span>
                      )}
                      {a.is_verified && (
                        <CheckCircle className="w-3 h-3 text-green-500" />
                      )}
                    </div>
                    {(a.user_id === currentUserId) && (
                      <button onClick={() => handleDelete(a.annotation_id)} className="p-0.5 text-[#E8E3D9] hover:text-red-400 transition-colors" data-testid={`delete-annotation-${a.annotation_id}`}>
                        <Trash2 className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                  <p className="text-sm text-[#2C2A29] leading-relaxed mb-2">{a.text}</p>
                  <div className="flex items-center gap-3">
                    <button onClick={() => handleVote(a.annotation_id, 1)} className="flex items-center gap-1 text-[10px] text-[#A39E93] hover:text-green-600 transition-colors" data-testid={`upvote-${a.annotation_id}`}>
                      <ThumbsUp className="w-3 h-3" /> {a.upvotes || 0}
                    </button>
                    <button onClick={() => handleVote(a.annotation_id, -1)} className="flex items-center gap-1 text-[10px] text-[#A39E93] hover:text-red-500 transition-colors" data-testid={`downvote-${a.annotation_id}`}>
                      <ThumbsDown className="w-3 h-3" /> {a.downvotes || 0}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
