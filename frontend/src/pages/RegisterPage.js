import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate, Link } from 'react-router-dom';
import { BookOpen, Eye, EyeOff } from 'lucide-react';

function formatApiErrorDetail(detail) {
  if (detail == null) return "Something went wrong. Please try again.";
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map(e => (e && typeof e.msg === "string" ? e.msg : JSON.stringify(e))).filter(Boolean).join(" ");
  if (detail && typeof detail.msg === "string") return detail.msg;
  return String(detail);
}

export default function RegisterPage() {
  const { user, loading, register } = useAuth();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPass, setShowPass] = useState(false);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (loading) return null;
  if (user) return <Navigate to="/dashboard" />;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (password.length < 6) { setError('Password must be at least 6 characters'); return; }
    setSubmitting(true);
    try {
      await register(name, email, password);
    } catch (err) {
      setError(formatApiErrorDetail(err.response?.data?.detail) || err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FDFBF7] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-6">
            <div className="w-10 h-10 bg-[#D97757] rounded-full flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <span className="font-heading text-2xl font-bold text-[#2C2A29]">DharmaSearch</span>
          </Link>
          <h1 className="font-heading text-3xl font-bold text-[#2C2A29] mb-2">Begin Your Journey</h1>
          <p className="text-[#75716B]">Create an account to explore sacred texts</p>
        </div>

        <div className="bg-white border border-[#E8E3D9] rounded-2xl p-8 shadow-sm">
          <form onSubmit={handleSubmit} data-testid="register-form">
            {error && (
              <div className="bg-red-50 text-red-700 rounded-xl px-4 py-3 text-sm mb-4" data-testid="register-error">
                {error}
              </div>
            )}
            <div className="mb-4">
              <label className="block text-sm font-medium text-[#2C2A29] mb-1.5">Name</label>
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                className="w-full border border-[#E8E3D9] rounded-xl px-4 py-3 bg-[#FDFBF7] focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none transition-all"
                placeholder="Your name"
                required
                data-testid="register-name-input"
              />
            </div>
            <div className="mb-4">
              <label className="block text-sm font-medium text-[#2C2A29] mb-1.5">Email</label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="w-full border border-[#E8E3D9] rounded-xl px-4 py-3 bg-[#FDFBF7] focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none transition-all"
                placeholder="your@email.com"
                required
                data-testid="register-email-input"
              />
            </div>
            <div className="mb-6">
              <label className="block text-sm font-medium text-[#2C2A29] mb-1.5">Password</label>
              <div className="relative">
                <input
                  type={showPass ? "text" : "password"}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  className="w-full border border-[#E8E3D9] rounded-xl px-4 py-3 bg-[#FDFBF7] focus:ring-2 focus:ring-[#D97757] focus:border-transparent outline-none transition-all pr-12"
                  placeholder="Min 6 characters"
                  required
                  data-testid="register-password-input"
                />
                <button type="button" onClick={() => setShowPass(!showPass)} className="absolute right-3 top-1/2 -translate-y-1/2 text-[#A39E93] hover:text-[#75716B]">
                  {showPass ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>
            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-[#D97757] text-white rounded-full py-3 font-medium hover:bg-[#C16648] transition-colors disabled:opacity-50"
              data-testid="register-submit-btn"
            >
              {submitting ? 'Creating account...' : 'Create Account'}
            </button>
          </form>
        </div>

        <p className="text-center mt-6 text-[#75716B]">
          Already have an account?{' '}
          <Link to="/login" className="text-[#D97757] font-medium hover:underline" data-testid="register-login-link">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
