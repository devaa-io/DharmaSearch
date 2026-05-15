import React, { useState } from 'react';
import axios from 'axios';
import { AlertTriangle, Send, X } from 'lucide-react';
import { toast } from 'sonner';

const API = process.env.REACT_APP_BACKEND_URL;

const FIELDS = [
  { value: 'translation', label: 'Translation' },
  { value: 'text', label: 'Sanskrit/Original Text' },
  { value: 'keywords', label: 'Keywords' },
  { value: 'chapter_name', label: 'Chapter Name' },
];

export default function CorrectionModal({ verse, onClose }) {
  const [field, setField] = useState('translation');
  const [suggestedValue, setSuggestedValue] = useState('');
  const [reason, setReason] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const currentValue = verse[field] || '';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!suggestedValue.trim()) return;
    setSubmitting(true);
    try {
      await axios.post(`${API}/api/corrections`, {
        verse_id: verse.verse_id,
        field,
        current_value: currentValue,
        suggested_value: suggestedValue.trim(),
        reason: reason.trim()
      }, { withCredentials: true });
      toast.success('Correction submitted for review. Thank you!');
      onClose();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to submit');
    } finally { setSubmitting(false); }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" data-testid="correction-modal">
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-white rounded-xl shadow-2xl max-w-lg w-full p-6 max-h-[90vh] overflow-y-auto animate-fade-in">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-[#D97757]" />
            <h3 className="font-heading text-xl font-bold text-[#2C2A29]">Suggest a Correction</h3>
          </div>
          <button onClick={onClose} className="p-1 text-[#A39E93] hover:text-[#2C2A29]" data-testid="correction-close">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="bg-[#FDFBF7] border border-[#E8E3D9] rounded-lg p-3 mb-4">
          <p className="text-xs text-[#A39E93] uppercase tracking-wider mb-1">Verse</p>
          <p className="text-sm font-medium text-[#2C2A29]">{verse.text_name} Ch.{verse.chapter} V.{verse.verse_number}</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-xs font-medium text-[#2C2A29] mb-1.5">What needs correction?</label>
            <select
              value={field}
              onChange={e => setField(e.target.value)}
              className="w-full border border-[#E8E3D9] rounded-lg px-3 py-2.5 text-sm bg-white focus:ring-2 focus:ring-[#D97757] outline-none"
              data-testid="correction-field-select"
            >
              {FIELDS.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-xs font-medium text-[#2C2A29] mb-1.5">Current value</label>
            <div className="bg-[#F5F2EA] border border-[#E8E3D9] rounded-lg px-3 py-2.5 text-sm text-[#75716B] max-h-24 overflow-y-auto">
              {currentValue || '(empty)'}
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-xs font-medium text-[#2C2A29] mb-1.5">Suggested correction</label>
            <textarea
              value={suggestedValue}
              onChange={e => setSuggestedValue(e.target.value)}
              placeholder="Enter the corrected text..."
              className="w-full border border-[#E8E3D9] rounded-lg px-3 py-2.5 text-sm bg-white focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none resize-none min-h-[80px]"
              required
              data-testid="correction-suggested-input"
            />
          </div>

          <div className="mb-5">
            <label className="block text-xs font-medium text-[#2C2A29] mb-1.5">Reason (optional)</label>
            <input
              type="text"
              value={reason}
              onChange={e => setReason(e.target.value)}
              placeholder="Why this correction is needed..."
              className="w-full border border-[#E8E3D9] rounded-lg px-3 py-2.5 text-sm bg-white focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none"
              data-testid="correction-reason-input"
            />
          </div>

          <button
            type="submit"
            disabled={submitting || !suggestedValue.trim()}
            className="w-full flex items-center justify-center gap-2 bg-[#D97757] text-white py-3 rounded-lg font-medium hover:bg-[#C16648] transition-colors disabled:opacity-40"
            data-testid="correction-submit-btn"
          >
            <Send className="w-4 h-4" />
            {submitting ? 'Submitting...' : 'Submit Correction'}
          </button>
        </form>

        <p className="text-[10px] text-[#A39E93] text-center mt-3">
          Corrections are reviewed by admins before being applied. Thank you for helping improve our database.
        </p>
      </div>
    </div>
  );
}
