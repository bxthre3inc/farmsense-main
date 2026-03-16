import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { 
  Trophy, Search, Landmark, ClipboardCheck, 
  ArrowUpRight, Calculator, Calendar, Plus
} from 'lucide-react';
import { GrantPipeline } from './GrantPipeline';
import { GrantOpportunityList } from './GrantOpportunityList';
import { GrantProfileView } from './GrantProfileView';

export const GrantManager: React.FC = () => {
  const location = useLocation();

  const tabs = [
    { id: 'pipeline', label: 'Pipeline', path: '/admin/grants', icon: Trophy },
    { id: 'opportunities', label: 'Opportunities', path: '/admin/grants/opportunities', icon: Search },
    { id: 'profile', label: 'Org Profile', path: '/admin/grants/profile', icon: Landmark },
  ];

  return (
    <div className="p-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
        <div>
          <h1 className="text-3xl font-black text-slate-900">Grant Manager</h1>
          <p className="text-slate-500 mt-1">Command & Control for global funding operations.</p>
        </div>

        <div className="flex bg-white p-1 rounded-2xl border border-slate-200 shadow-sm">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = location.pathname === tab.path;
            return (
              <Link
                key={tab.id}
                to={tab.path}
                className={`flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-bold transition-all ${
                  isActive 
                    ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-200' 
                    : 'text-slate-500 hover:bg-slate-50'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </Link>
            );
          })}
        </div>
      </div>

      <div className="bg-white rounded-3xl border border-slate-100 shadow-xl shadow-slate-200/50 min-h-[600px] overflow-hidden">
        <Routes>
          <Route path="/" element={<GrantPipeline />} />
          <Route path="/opportunities" element={<GrantOpportunityList />} />
          <Route path="/profile" element={<GrantProfileView />} />
        </Routes>
      </div>
    </div>
  );
};
