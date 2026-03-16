import React, { useState } from 'react';
import { 
  Scale, FileCheck, ShieldAlert, History, 
  Download, ExternalLink, RefreshCw, Hash,
  Database, Fingerprint, Lock
} from 'lucide-react';

export const WaterLedger: React.FC = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [reports, setReports] = useState([
    { id: 'LC-2026-001', field: 'SLV-CSU-CTR', date: '2026-03-01', hash: 'e3b0c44298fc1c149afbf4c8996fb924', status: 'VERIFIED' },
    { id: 'LC-2026-002', field: 'SLV-DAN-W', date: '2026-03-05', hash: '8f2e2451f2f18398a3e792e3a1f185d2', status: 'VERIFIED' },
  ]);

  const generateReport = () => {
    setIsGenerating(true);
    setTimeout(() => {
      const newReport = {
        id: `LC-2026-00${reports.length + 1}`,
        field: 'SLV-NEW-F',
        date: new Date().toISOString().split('T')[0],
        hash: Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15),
        status: 'VERIFIED'
      };
      setReports([newReport, ...reports]);
      setIsGenerating(false);
    }, 2000);
  };

  return (
    <div className="p-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <div>
          <h1 className="text-3xl font-black text-slate-900 flex items-center gap-3">
            <Scale className="text-emerald-600 w-8 h-8" />
            Digital Water Ledger
          </h1>
          <p className="text-slate-500 mt-1">Non-repudiable evidence for Water Court & Statutory Compliance.</p>
        </div>
        <button 
          onClick={generateReport}
          disabled={isGenerating}
          className="bg-slate-900 text-white px-8 py-4 rounded-2xl font-black shadow-2xl shadow-slate-200 hover:bg-slate-800 transition-all flex items-center gap-3 disabled:opacity-50"
        >
          {isGenerating ? <RefreshCw className="animate-spin w-5 h-5" /> : <FileCheck className="w-5 h-5 text-emerald-400" />}
          Generate Certified Court Report
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-100 shadow-xl shadow-slate-200/50 overflow-hidden">
          <div className="p-6 bg-slate-50 border-b border-slate-100 flex items-center justify-between">
            <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
              <Database className="w-4 h-4" />
              Recent Compliance Records
            </h3>
            <span className="text-[10px] font-black bg-emerald-100 text-emerald-700 px-3 py-1 rounded-full">AllianceChain PBFT Active</span>
          </div>
          <div className="divide-y divide-slate-50">
            {reports.map((report) => (
              <div key={report.id} className="p-6 hover:bg-slate-50 transition-all group flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <span className="font-black text-slate-900">{report.id}</span>
                    <span className="text-xs text-slate-400 font-medium">• {report.field}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                    <Fingerprint className="w-3 h-3" />
                    {report.hash.substring(0, 16)}...
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="flex flex-col items-end">
                    <span className="text-[10px] font-black text-emerald-600 uppercase tracking-widest">{report.status}</span>
                    <span className="text-xs text-slate-400 font-medium">{report.date}</span>
                  </div>
                  <button className="p-3 bg-white border border-slate-100 text-slate-400 hover:text-slate-900 hover:shadow-lg rounded-xl transition-all">
                    <Download className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-8">
          <div className="bg-emerald-900 rounded-3xl p-8 text-white relative overflow-hidden">
            <div className="absolute -right-4 -top-4 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl" />
            <h4 className="text-xs font-black uppercase tracking-[0.2em] text-emerald-400 mb-6">Ledger Health</h4>
            <div className="space-y-6">
              <div className="flex justify-between items-end">
                <span className="text-xs font-medium text-emerald-200/60 uppercase">Signed Records</span>
                <span className="text-2xl font-black">1.2k+</span>
              </div>
              <div className="flex justify-between items-end">
                <span className="text-xs font-medium text-emerald-200/60 uppercase">Integrity Drift</span>
                <span className="text-2xl font-black">0.00%</span>
              </div>
              <div className="flex justify-between items-end">
                <span className="text-xs font-medium text-emerald-200/60 uppercase">Vulnerability</span>
                <span className="text-2xl font-black text-emerald-400 italic">None</span>
              </div>
            </div>
            <div className="mt-8 pt-8 border-t border-emerald-800 flex items-center gap-3 text-xs text-emerald-500 font-bold">
              <Lock className="w-4 h-4" />
              Non-Repudiation Guaranteed
            </div>
          </div>

          <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm border-l-4 border-l-amber-500">
            <div className="flex items-center gap-2 text-amber-600 mb-4">
              <ShieldAlert className="w-5 h-5" />
              <span className="text-xs font-black uppercase tracking-widest">Compliance Alerts</span>
            </div>
            <p className="text-sm font-bold text-slate-800 leading-tight">1 Field requiring immediate audit due to satellite-meter discrepancy of 18.2%.</p>
            <button className="mt-6 text-xs font-black text-amber-600 uppercase tracking-widest hover:text-amber-700 transition-colors flex items-center gap-2">
              Investigate Discrepancy <ExternalLink className="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
