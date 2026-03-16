import React, { useState } from 'react';
import { 
  Settings, Database, Key, Bell, 
  ShieldCheck, RefreshCw, Save, Sliders,
  Cloud, Wind, Activity
} from 'lucide-react';

export const AdminSettings: React.FC = () => {
  const [isSaving, setIsSaving] = useState(false);
  const [thresholds, setThresholds] = useState({
    auditDiscrepancy: 15,
    batteryAlert: 20,
    signalThreshold: 40,
    krigingErrorMax: 5
  });

  const handleSave = () => {
    setIsSaving(true);
    setTimeout(() => setIsSaving(false), 1500);
  };

  return (
    <div className="p-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <div>
          <h1 className="text-3xl font-black text-slate-900 flex items-center gap-3">
            <Settings className="text-emerald-600 w-8 h-8" />
            System Command & Config
          </h1>
          <p className="text-slate-500 mt-1">Master configuration for FarmSense protocols and integrations.</p>
        </div>
        <button 
          onClick={handleSave}
          disabled={isSaving}
          className="bg-slate-900 text-white px-8 py-4 rounded-2xl font-black shadow-2xl shadow-slate-200 hover:bg-slate-800 transition-all flex items-center gap-3 disabled:opacity-50"
        >
          {isSaving ? <RefreshCw className="animate-spin w-5 h-5" /> : <Save className="w-5 h-5 text-emerald-400" />}
          Apply Global Config
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Protocol Thresholds */}
        <div className="space-y-8">
          <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
            <h3 className="text-sm font-black text-slate-900 uppercase tracking-widest flex items-center gap-2 mb-8">
              <Sliders className="w-4 h-4 text-emerald-600" />
              Protocol Thresholds
            </h3>
            
            <div className="space-y-6">
              {[
                { label: 'Audit Discrepancy Trigger', value: thresholds.auditDiscrepancy, unit: '%', key: 'auditDiscrepancy' },
                { label: 'Battery Low Warning', value: thresholds.batteryAlert, unit: '%', key: 'batteryAlert' },
                { label: 'Signal Strength Min.', value: thresholds.signalThreshold, unit: 'dBm', key: 'signalThreshold' },
                { label: 'Max Kriging Variance', value: thresholds.krigingErrorMax, unit: '%', key: 'krigingErrorMax' },
              ].map((t) => (
                <div key={t.key}>
                  <div className="flex justify-between mb-2">
                    <label className="text-xs font-bold text-slate-600">{t.label}</label>
                    <span className="text-xs font-black text-emerald-600">{t.value}{t.unit}</span>
                  </div>
                  <input 
                    type="range"
                    min="1"
                    max="100"
                    value={t.value}
                    onChange={(e) => setThresholds({ ...thresholds, [t.key]: parseInt(e.target.value) })}
                    className="w-full h-1.5 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                  />
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-50 rounded-3xl p-8 border border-slate-100 relative overflow-hidden group">
            <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-indigo-500/5 rounded-full blur-2xl group-hover:bg-indigo-500/10 transition-all" />
            <h3 className="text-sm font-black text-slate-900 uppercase tracking-widest flex items-center gap-2 mb-6">
              <Bell className="w-4 h-4 text-indigo-600" />
              Administrative Alerts
            </h3>
            <div className="space-y-4">
              {[
                { label: 'Compliance Violation (Instant)', active: true },
                { label: 'Critical Fleet Failure', active: true },
                { label: 'New Investor Access Request', active: false },
                { label: 'Daily Win-Rate Digest', active: true },
              ].map((n, i) => (
                <label key={i} className="flex items-center justify-between cursor-pointer group">
                  <span className="text-xs font-bold text-slate-500 group-hover:text-slate-900 transition-colors">{n.label}</span>
                  <div className={`w-10 h-5 rounded-full relative transition-all ${n.active ? 'bg-emerald-500' : 'bg-slate-300'}`}>
                    <div className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all ${n.active ? 'left-6' : 'left-1'}`} />
                  </div>
                </label>
              ))}
            </div>
          </div>
        </div>

        {/* Integration Credentials */}
        <div className="space-y-8">
          <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
            <h3 className="text-sm font-black text-slate-900 uppercase tracking-widest flex items-center gap-2 mb-8">
              <Key className="w-4 h-4 text-amber-600" />
              Integration Data Hub
            </h3>
            <div className="space-y-6">
              {[
                { name: 'Satellite Engine API', icon: Cloud, status: 'CONNECTED', key: '••••••••••••••••' },
                { name: 'NOAA Weather Ensemble', icon: Wind, status: 'CONNECTED', key: '••••••••••••••••' },
                { name: 'AllianceChain Quorum', icon: ShieldCheck, status: 'SYNCED', key: 'fs_block_master_v2' },
              ].map((api) => (
                <div key={api.name} className="p-4 bg-slate-50 rounded-2xl border border-slate-100 group hover:border-slate-200 transition-all">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center text-slate-400">
                        <api.icon className="w-4 h-4" />
                      </div>
                      <span className="text-xs font-black text-slate-900">{api.name}</span>
                    </div>
                    <span className="text-[10px] font-black text-emerald-600 tracking-tighter">{api.status}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <input 
                      type="text" 
                      value={api.key} 
                      readOnly 
                      className="flex-1 bg-white border border-slate-100 rounded-lg px-3 py-1.5 text-[10px] font-mono text-slate-400" 
                    />
                    <button className="text-[10px] font-black text-slate-400 hover:text-slate-900">ROTATE</button>
                  </div>
                </div>
              ))}
            </div>
            <button className="w-full mt-8 py-3 border-2 border-dashed border-slate-200 rounded-2xl text-[10px] font-black text-slate-400 uppercase tracking-widest hover:border-slate-300 hover:text-slate-500 transition-all">
              + Register New Data Source
            </button>
          </div>

          <div className="bg-rose-50 rounded-3xl p-8 border border-rose-100 text-rose-900">
            <div className="flex items-center gap-2 mb-4">
              <ShieldCheck className="w-5 h-5 text-rose-600" />
              <span className="text-xs font-black uppercase tracking-widest">Master Safety Override</span>
            </div>
            <p className="text-xs font-medium leading-relaxed opacity-80 mb-6">
              If the AllianceChain consensus fails to reach a quorum, administrative override allows for temporary Statutory Compliance generation.
            </p>
            <button className="w-full py-3 bg-rose-600 text-white rounded-xl font-black text-xs shadow-lg shadow-rose-200 hover:bg-rose-700 transition-all">
              PAUSE GLOBAL AUTONOMY
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
