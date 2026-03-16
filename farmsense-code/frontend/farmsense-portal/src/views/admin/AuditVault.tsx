import React, { useState } from 'react';
import { 
  ShieldCheck, Lock, Fingerprint, Eye, 
  Search, ShieldAlert, Cpu, Network,
  Info, CheckCircle2, AlertCircle, Terminal
} from 'lucide-react';

export const AuditVault: React.FC = () => {
  const [logs] = useState([
    { id: 'EV-10293', event: 'ADMIN_LOGIN', user: 'bx3_master', timestamp: '2026-03-11 10:42:15', status: 'VERIFIED', proof: 'fs_proof_8a2d...' },
    { id: 'EV-10294', event: 'WATER_LEDGER_GENERATE', user: 'bx3_master', field: 'SLV-CSU-CTR', timestamp: '2026-03-11 10:48:20', status: 'VERIFIED', proof: 'fs_proof_7f4b...' },
    { id: 'EV-10295', event: 'INVESTOR_NDA_SIGN', user: 'system', firm: 'G-Capital', timestamp: '2026-03-11 10:50:04', status: 'UNVERIFIED', proof: 'fs_proof_pending' },
    { id: 'EV-10296', event: 'SATELLITE_API_SYNC', user: 'service_acc', timestamp: '2026-03-11 10:51:30', status: 'VERIFIED', proof: 'fs_proof_9c6a...' },
  ]);

  return (
    <div className="p-8">
      <div className="mb-12">
        <h1 className="text-3xl font-black text-slate-900 flex items-center gap-3">
          <ShieldCheck className="text-emerald-600 w-8 h-8" />
          Security & Audit Vault
        </h1>
        <p className="text-slate-500 mt-1">Non-repudiable logs of all critical Command & Control operations.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-12">
        <div className="bg-slate-900 rounded-3xl p-8 text-white flex flex-col justify-between h-48 group">
          <div className="flex items-center justify-between">
            <Lock className="text-emerald-400 w-6 h-6" />
            <div className="text-[10px] font-black uppercase tracking-widest text-emerald-400">HSM Status</div>
          </div>
          <div>
            <p className="text-3xl font-black">ENCRYPTED</p>
            <p className="text-[10px] text-slate-500 font-bold mt-1">AES-256-GCM / Ed25519</p>
          </div>
        </div>
        
        <div className="bg-white border border-slate-100 rounded-3xl p-8 shadow-sm flex flex-col justify-between h-48">
          <div className="flex items-center justify-between text-slate-400">
            <Fingerprint className="w-6 h-6" />
            <div className="text-[10px] font-black uppercase tracking-widest">Attestation</div>
          </div>
          <div>
            <p className="text-3xl font-black text-slate-900">100%</p>
            <p className="text-[10px] text-slate-400 font-bold mt-1">Verified Audit Consistency</p>
          </div>
        </div>

        <div className="bg-white border border-slate-100 rounded-3xl p-8 shadow-sm flex flex-col justify-between h-48">
          <div className="flex items-center justify-between text-slate-400">
             <Cpu className="w-6 h-6" />
             <div className="text-[10px] font-black uppercase tracking-widest">Ledger Sync</div>
          </div>
          <div>
            <p className="text-3xl font-black text-slate-900">4 / 4</p>
            <p className="text-[10px] text-slate-400 font-bold mt-1">Quorum consensus online</p>
          </div>
        </div>

        <div className="bg-white border border-slate-100 rounded-3xl p-8 shadow-sm flex flex-col justify-between h-48">
          <div className="flex items-center justify-between text-rose-500">
             <ShieldAlert className="w-6 h-6" />
             <div className="text-[10px] font-black uppercase tracking-widest">Incidents</div>
          </div>
          <div>
            <p className="text-3xl font-black text-slate-900">0</p>
            <p className="text-[10px] text-slate-400 font-bold mt-1">Total anomalies detected</p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-3xl border border-slate-100 shadow-xl shadow-slate-200/50 overflow-hidden">
        <div className="p-6 bg-slate-50/50 border-b border-slate-100 flex items-center justify-between">
           <div className="flex items-center gap-3">
             <Terminal className="w-5 h-5 text-slate-400" />
             <h3 className="text-sm font-black text-slate-900 uppercase tracking-widest">Master Audit Trail</h3>
           </div>
           <div className="relative">
             <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
             <input type="text" placeholder="Search events..." className="pl-9 pr-4 py-2 text-xs bg-white border border-slate-200 rounded-xl outline-none" />
           </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-white divide-x divide-slate-50">
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Event ID</th>
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Operation</th>
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Identity</th>
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Proof Hash</th>
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {logs.map(log => (
                <tr key={log.id} className="hover:bg-slate-50 transition-colors font-medium">
                  <td className="px-8 py-5">
                    <div className="font-bold text-slate-900">{log.id}</div>
                    <div className="text-[10px] text-slate-400 mt-0.5">{log.timestamp}</div>
                  </td>
                  <td className="px-8 py-5">
                    <div className="text-xs font-black text-slate-700 bg-slate-100 px-2 py-1 rounded inline-block">{log.event}</div>
                    {log.field && <div className="text-[10px] text-emerald-600 font-bold mt-1 uppercase tracking-tighter">Field: {log.field}</div>}
                  </td>
                  <td className="px-8 py-5">
                    <div className="flex items-center gap-2 text-xs text-slate-600">
                      <div className="w-6 h-6 bg-slate-200 rounded-full flex items-center justify-center text-[10px] font-black text-slate-500 uppercase">
                        {log.user.substring(0,2)}
                      </div>
                      {log.user}
                    </div>
                  </td>
                  <td className="px-8 py-5">
                    <div className="flex items-center gap-2 text-[10px] font-mono text-slate-400 bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-100 truncate max-w-[150px]">
                      {log.proof}
                    </div>
                  </td>
                  <td className="px-8 py-5">
                    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider ${
                      log.status === 'VERIFIED' ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'
                    }`}>
                      {log.status === 'VERIFIED' ? <CheckCircle2 className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                      {log.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="p-6 bg-slate-50/30 text-center">
           <button className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] hover:text-slate-600 flex items-center gap-2 mx-auto">
             <Info className="w-3 h-3" /> Load cryptographic depth history
           </button>
        </div>
      </div>
    </div>
  );
};
