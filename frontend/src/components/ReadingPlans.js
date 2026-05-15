import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { BookOpen, RefreshCw, ArrowLeft, Check, Plus, ChevronRight, Trophy, Calendar } from 'lucide-react';
import VerseCard from './VerseCard';

const API = process.env.REACT_APP_BACKEND_URL;

export default function ReadingPlans() {
  const [plans, setPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [planDetail, setPlanDetail] = useState(null);
  const [selectedDay, setSelectedDay] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);

  const fetchPlans = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await axios.get(`${API}/api/plans`, { withCredentials: true });
      setPlans(data);
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { fetchPlans(); }, [fetchPlans]);

  const openPlan = async (planId) => {
    setSelectedPlan(planId);
    setSelectedDay(null);
    try {
      const { data } = await axios.get(`${API}/api/plans/${planId}`, { withCredentials: true });
      setPlanDetail(data);
    } catch (err) { console.error(err); }
  };

  const markDayComplete = async (dayNum) => {
    try {
      await axios.post(`${API}/api/plans/${selectedPlan}/progress`, { day_number: dayNum }, { withCredentials: true });
      setPlanDetail(prev => ({
        ...prev,
        completed_days: [...(prev.completed_days || []), dayNum]
      }));
    } catch (err) { console.error(err); }
  };

  const goBack = () => {
    if (selectedDay !== null) setSelectedDay(null);
    else { setSelectedPlan(null); setPlanDetail(null); }
  };

  if (loading) return (
    <div className="flex items-center justify-center py-20">
      <RefreshCw className="w-5 h-5 text-[#D97757] animate-spin" />
    </div>
  );

  // Plan detail view with day selected
  if (planDetail && selectedDay !== null) {
    const day = planDetail.days?.[selectedDay];
    const dayVerses = day?.verse_ids?.map(id => planDetail.verse_details?.[id]).filter(Boolean) || [];
    const completed = (planDetail.completed_days || []).includes(day?.day);

    return (
      <div className="animate-fade-in" data-testid="plan-day-view">
        <button onClick={goBack} className="flex items-center gap-1.5 text-xs text-[#75716B] hover:text-[#D97757] mb-4" data-testid="plan-day-back">
          <ArrowLeft className="w-3.5 h-3.5" /> Back to plan
        </button>
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-xs text-[#A39E93] uppercase tracking-wider">Day {day?.day} of {planDetail.total_days}</p>
            <h2 className="font-heading text-xl font-bold text-[#2C2A29]">{day?.title || `Day ${day?.day}`}</h2>
          </div>
          {!completed && (
            <button onClick={() => markDayComplete(day?.day)} className="flex items-center gap-1.5 bg-[#D97757] text-white px-4 py-2 rounded-lg text-xs font-medium hover:bg-[#C16648] transition-colors" data-testid="mark-complete-btn">
              <Check className="w-3.5 h-3.5" /> Mark Complete
            </button>
          )}
          {completed && (
            <span className="flex items-center gap-1.5 text-xs text-green-600 bg-green-50 px-3 py-1.5 rounded-lg">
              <Check className="w-3.5 h-3.5" /> Completed
            </span>
          )}
        </div>
        <div className="space-y-3">
          {dayVerses.map(v => <VerseCard key={v.verse_id} verse={v} />)}
        </div>
      </div>
    );
  }

  // Plan detail view
  if (planDetail) {
    const completed = planDetail.completed_days || [];
    const progress = planDetail.total_days > 0 ? Math.round((completed.length / planDetail.total_days) * 100) : 0;

    return (
      <div className="animate-fade-in" data-testid="plan-detail-view">
        <button onClick={goBack} className="flex items-center gap-1.5 text-xs text-[#75716B] hover:text-[#D97757] mb-4" data-testid="plan-back">
          <ArrowLeft className="w-3.5 h-3.5" /> All Plans
        </button>

        <div className="mb-8">
          <h2 className="font-heading text-2xl font-bold text-[#2C2A29] mb-1">{planDetail.title}</h2>
          <p className="text-sm text-[#75716B]">{planDetail.description}</p>
        </div>

        {/* Progress bar */}
        <div className="bg-white border border-[#E8E3D9] rounded-lg p-4 mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-[#75716B]">Progress</span>
            <span className="text-xs font-medium text-[#D97757]">{completed.length}/{planDetail.total_days} days</span>
          </div>
          <div className="h-2 bg-[#F5F2EA] rounded-full overflow-hidden">
            <div className="h-full bg-[#D97757] rounded-full transition-all duration-500" style={{width: `${progress}%`}} />
          </div>
          {progress === 100 && (
            <div className="flex items-center gap-2 mt-3 text-xs text-green-600">
              <Trophy className="w-4 h-4" /> Plan complete! Well done.
            </div>
          )}
        </div>

        {/* Days list */}
        <div className="space-y-1" data-testid="plan-days-list">
          {planDetail.days?.map((day, i) => {
            const isDone = completed.includes(day.day);
            return (
              <button
                key={i}
                onClick={() => setSelectedDay(i)}
                className={`w-full flex items-center gap-3 p-4 rounded-lg border text-left transition-all ${
                  isDone ? 'bg-green-50/50 border-green-200/50' : 'bg-white border-[#E8E3D9] hover:border-[#D97757]/30'
                }`}
                data-testid={`plan-day-${day.day}`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${isDone ? 'bg-green-100 text-green-600' : 'bg-[#F5F2EA] text-[#75716B]'}`}>
                  {isDone ? <Check className="w-4 h-4" /> : <span className="text-xs font-bold">{day.day}</span>}
                </div>
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-medium ${isDone ? 'text-green-700' : 'text-[#2C2A29]'}`}>
                    {day.title || `Day ${day.day}`}
                  </p>
                  <p className="text-xs text-[#A39E93]">{day.verse_ids?.length || 0} verses</p>
                </div>
                <ChevronRight className="w-4 h-4 text-[#E8E3D9] flex-shrink-0" />
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  // Plans list
  const prebuilt = plans.filter(p => p.is_prebuilt);
  const custom = plans.filter(p => !p.is_prebuilt);

  return (
    <div className="animate-fade-in" data-testid="plans-section">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="font-heading text-xl sm:text-2xl font-bold text-[#2C2A29] mb-1">Reading Plans</h2>
          <p className="text-xs text-[#A39E93]">Structured paths through sacred wisdom</p>
        </div>
      </div>

      {/* Pre-built plans */}
      <div className="mb-8">
        <p className="text-xs text-[#A39E93] uppercase tracking-wider mb-3">Guided Plans</p>
        <div className="space-y-2" data-testid="prebuilt-plans">
          {prebuilt.map(p => {
            const completed = p.completed_days?.length || 0;
            const total = p.total_days || 1;
            const progress = Math.round((completed / total) * 100);
            return (
              <button
                key={p.plan_id}
                onClick={() => openPlan(p.plan_id)}
                className="w-full flex items-center gap-4 p-4 bg-white border border-[#E8E3D9] rounded-lg hover:border-[#D97757]/30 transition-all text-left group"
                data-testid={`plan-${p.plan_id}`}
              >
                <div className="w-10 h-10 rounded-lg bg-[#D97757]/10 flex items-center justify-center flex-shrink-0">
                  <Calendar className="w-5 h-5 text-[#D97757]" strokeWidth={1.5} />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-medium text-[#2C2A29] group-hover:text-[#D97757] transition-colors">{p.title}</h3>
                  <p className="text-xs text-[#A39E93] truncate">{p.description}</p>
                  {completed > 0 && (
                    <div className="mt-2 flex items-center gap-2">
                      <div className="h-1 flex-1 bg-[#F5F2EA] rounded-full max-w-[120px]">
                        <div className="h-full bg-[#D97757] rounded-full" style={{width: `${progress}%`}} />
                      </div>
                      <span className="text-[10px] text-[#A39E93]">{completed}/{total}</span>
                    </div>
                  )}
                </div>
                <div className="text-right flex-shrink-0">
                  <p className="text-xs text-[#A39E93]">{total} days</p>
                </div>
                <ChevronRight className="w-4 h-4 text-[#E8E3D9] group-hover:text-[#D97757] flex-shrink-0" />
              </button>
            );
          })}
        </div>
      </div>

      {/* Custom plans */}
      {custom.length > 0 && (
        <div>
          <p className="text-xs text-[#A39E93] uppercase tracking-wider mb-3">Your Custom Plans</p>
          <div className="space-y-2">
            {custom.map(p => (
              <button
                key={p.plan_id}
                onClick={() => openPlan(p.plan_id)}
                className="w-full flex items-center gap-4 p-4 bg-white border border-[#E8E3D9] rounded-lg hover:border-[#D97757]/30 transition-all text-left"
                data-testid={`plan-${p.plan_id}`}
              >
                <div className="w-10 h-10 rounded-lg bg-[#8A9A86]/10 flex items-center justify-center flex-shrink-0">
                  <BookOpen className="w-5 h-5 text-[#8A9A86]" strokeWidth={1.5} />
                </div>
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-[#2C2A29]">{p.title}</h3>
                  <p className="text-xs text-[#A39E93]">{p.total_days} days</p>
                </div>
                <ChevronRight className="w-4 h-4 text-[#E8E3D9]" />
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
