import React from 'react';
import { 
  TrendingUp, Calendar, AlertCircle, 
  CheckCircle2, Clock, DollarSign, Target 
} from 'lucide-react';

export const GrantPipeline: React.FC = () => {
  // Mock data for the pipeline summary
  const stages = [
    { label: 'Identified', count: 42, color: 'bg-slate-100 text-slate-600' },
    { label: 'Researching', count: 12, color: 'bg-blue-50 text-blue-600' },
    { label: 'Pitching', count: 5, color: 'bg-amber-50 text-amber-600' },
    { label: 'Applied', count: 8, color: 'bg-emerald-50 text-emerald-600' },
    { label: 'Shortlist', count: 2, color: 'bg-purple-50 text-purple-600' },
  ];

  const upcomingDeadlines = [
    { name: 'ESTCP Installation Resilience', date: 'March 26, 2026', priority: 'P0', amount: '$1.2M' },
    { name: 'NSF SBIR Phase I', date: 'April 15, 2026', priority: 'P1', amount: '$275K' },
    { name: 'CWCB Water Plan Grant', date: 'July 1, 2026', priority: 'P1', amount: '$500K' },
  ];

  return (
    <div className="p-8">
      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <div className="bg-slate-900 rounded-3xl p-6 text-white relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl transition-all group-hover:bg-emerald-500/20" />
          <div className="flex items-center gap-2 text-emerald-400 mb-4">
            <DollarSign className="w-5 h-5" />
            <span className="text-[10px] font-black uppercase tracking-widest">Expected Value</span>
          </div>
          <p className="text-4xl font-black">$2.85M</p>
          <p className="text-xs text-slate-400 mt-2">Weighted by probability (15 active)</p>
        </div>

        <div className="bg-white border border-slate-100 rounded-3xl p-6 shadow-sm">
          <div className="flex items-center gap-2 text-blue-600 mb-4">
            <Target className="w-5 h-5" />
            <span className="text-[10px] font-black uppercase tracking-widest">Win Rate</span>
          </div>
          <p className="text-4xl font-black text-slate-900">38%</p>
          <p className="text-xs text-slate-400 mt-2">+5% from last quarter</p>
        </div>

        <div className="bg-white border border-slate-100 rounded-3xl p-6 shadow-sm">
          <div className="flex items-center gap-2 text-amber-600 mb-4">
            <Clock className="w-5 h-5" />
            <span className="text-[10px] font-black uppercase tracking-widest">Active Applications</span>
          </div>
          <p className="text-4xl font-black text-slate-900">15</p>
          <p className="text-xs text-slate-400 mt-2">Across State & Federal agencies</p>
        </div>

        <div className="bg-white border border-slate-100 rounded-3xl p-6 shadow-sm">
          <div className="flex items-center gap-2 text-emerald-600 mb-4">
            <CheckCircle2 className="w-5 h-5" />
            <span className="text-[10px] font-black uppercase tracking-widest">Funding Secured</span>
          </div>
          <p className="text-4xl font-black text-slate-900">$840K</p>
          <p className="text-xs text-slate-400 mt-2">Year-to-date (2026)</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        {/* Pipeline Stages */}
        <div className="lg:col-span-2">
          <h3 className="text-lg font-black text-slate-900 mb-6 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-600" />
            Pipeline Velocity
          </h3>
          <div className="space-y-4">
            {stages.map((stage) => (
              <div key={stage.label} className="bg-white border border-slate-50 rounded-2xl p-4 flex items-center justify-between hover:border-slate-200 transition-all cursor-pointer group">
                <div className="flex items-center gap-4">
                  <div className={`px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-wider ${stage.color}`}>
                    {stage.label}
                  </div>
                  <div className="h-2 w-32 bg-slate-100 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-slate-900 rounded-full transition-all group-hover:bg-emerald-500" 
                      style={{ width: `${(stage.count / 42) * 100}%` }}
                    />
                  </div>
                </div>
                <div className="text-lg font-black text-slate-900">{stage.count}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Deadlines */}
        <div>
          <h3 className="text-lg font-black text-slate-900 mb-6 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-600" />
            Critical Deadlines
          </h3>
          <div className="space-y-4">
            {upcomingDeadlines.map((deadline) => (
              <div key={deadline.name} className="bg-slate-50 rounded-2xl p-5 border-l-4 border-emerald-500 hover:bg-white hover:shadow-lg transition-all cursor-pointer">
                <div className="flex justify-between items-start mb-2">
                  <span className="text-[10px] font-black text-emerald-600 px-2 py-0.5 bg-emerald-100 rounded uppercase">
                    {deadline.priority}
                  </span>
                  <span className="text-sm font-black text-slate-900">{deadline.amount}</span>
                </div>
                <h4 className="font-bold text-slate-900 text-sm leading-tight mb-2">{deadline.name}</h4>
                <p className="text-xs text-slate-500 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  Due {deadline.date}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
