import React from 'react';
import { 
  Activity, Zap, Signal, Battery, 
  MapPin, AlertTriangle, TrendingUp, 
  Target, BarChart3, Filter
} from 'lucide-react';

export const FleetDiagnostics: React.FC = () => {
  const nodes = [
    { id: 'RSS-01', type: 'Base Station', field: 'CSU Pivot 1', status: 'online', sig: 98, bat: 100 },
    { id: 'DHU-104', type: 'Domain Hub', field: 'CSU Pivot 1', status: 'online', sig: 85, bat: 92 },
    { id: 'DHU-105', type: 'Domain Hub', field: 'SLV-North-01', status: 'degraded', sig: 42, bat: 18 },
    { id: 'DHU-201', type: 'Domain Hub', field: 'CO-Private-8', status: 'offline', sig: 0, bat: 0 },
  ];

  return (
    <div className="p-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <div>
          <h1 className="text-3xl font-black text-slate-900 flex items-center gap-3">
            <Activity className="text-emerald-600 w-8 h-8" />
            Fleet Logic Command
          </h1>
          <p className="text-slate-500 mt-1">Global node health and autonomous logic performance monitoring.</p>
        </div>
        
        <div className="flex bg-white p-1 rounded-2xl border border-slate-200">
          <button className="px-6 py-2.5 bg-slate-100 text-slate-900 rounded-xl text-xs font-black uppercase">Fleet</button>
          <button className="px-6 py-2.5 text-slate-400 rounded-xl text-xs font-black uppercase hover:text-slate-900">Logic Hub</button>
          <button className="px-6 py-2.5 text-slate-400 rounded-xl text-xs font-black uppercase hover:text-slate-900">RO-I</button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
          <div className="flex items-center gap-2 text-emerald-600 mb-6">
            <Zap className="w-5 h-5" />
            <span className="text-xs font-black uppercase tracking-widest">Autonomous Logic ROI</span>
          </div>
          <p className="text-4xl font-black text-slate-900">$18,420</p>
          <p className="text-xs text-slate-400 mt-2">Saved this week across active fleets</p>
          <div className="mt-6 flex items-center justify-between">
            <div className="h-1.5 flex-1 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full bg-emerald-500 w-[78%]" />
            </div>
            <span className="ml-4 text-xs font-black text-emerald-600">78% Efficiency</span>
          </div>
        </div>

        <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
          <div className="flex items-center gap-2 text-indigo-600 mb-6">
            <TrendingUp className="w-5 h-5" />
            <span className="text-xs font-black uppercase tracking-widest">Res-Pop Conversion</span>
          </div>
          <p className="text-4xl font-black text-slate-900">14.2%</p>
          <p className="text-xs text-slate-400 mt-2">Free → Enterprise upgrade conversion</p>
          <div className="mt-4 flex gap-1">
            {[1, 2, 3, 4, 5, 6, 7].map(i => (
              <div key={i} className={`h-6 flex-1 rounded-sm ${i < 5 ? 'bg-indigo-500' : 'bg-slate-100'}`} />
            ))}
          </div>
        </div>

        <div className="bg-slate-900 p-8 rounded-3xl text-white relative overflow-hidden">
          <div className="absolute -right-4 -bottom-4 w-32 h-32 bg-rose-500/10 rounded-full blur-3xl" />
          <div className="flex items-center gap-2 text-rose-400 mb-6">
            <Signal className="w-5 h-5" />
            <span className="text-xs font-black uppercase tracking-widest">Connectivity Status</span>
          </div>
          <div className="flex justify-between items-end">
            <div>
              <p className="text-4xl font-black">94.8%</p>
              <p className="text-xs text-slate-400 mt-2">Fleets with active SAT/LoRa uplink</p>
            </div>
            <div className="text-rose-400 text-xs font-bold bg-rose-400/10 px-3 py-1 rounded-full flex items-center gap-1">
              <AlertTriangle className="w-3 h-3" />
              2 Nodes Down
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-3xl border border-slate-100 shadow-xl shadow-slate-200/50 overflow-hidden">
        <div className="p-6 border-b border-slate-50 flex items-center justify-between">
          <h3 className="text-sm font-black text-slate-900 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-slate-400" />
            Active Fleet Inventory
          </h3>
          <div className="flex gap-4">
             <button className="text-xs font-black text-slate-400 hover:text-slate-600 flex items-center gap-2">
               <Filter className="w-3 h-3" /> Filter Labels
             </button>
             <button className="text-xs font-black text-emerald-600">Export CSV</button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50/50">
              <tr>
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Node ID</th>
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Assignment</th>
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Status</th>
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Signal</th>
                <th className="px-8 py-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-widest">Battery</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {nodes.map(node => (
                <tr key={node.id} className="hover:bg-slate-50/50 transition-colors cursor-pointer group">
                  <td className="px-8 py-5">
                    <div className="font-bold text-slate-900 group-hover:text-emerald-600 transition-colors">{node.id}</div>
                    <div className="text-[10px] text-slate-400 font-bold uppercase">{node.type}</div>
                  </td>
                  <td className="px-8 py-5">
                    <div className="flex items-center gap-2 text-xs font-bold text-slate-600">
                      <MapPin className="w-3 h-3 text-slate-300" />
                      {node.field}
                    </div>
                  </td>
                  <td className="px-8 py-5">
                    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${
                      node.status === 'online' ? 'bg-emerald-100 text-emerald-700' : 
                      node.status === 'degraded' ? 'bg-amber-100 text-amber-700' : 'bg-rose-100 text-rose-700'
                    }`}>
                      <div className={`w-1.5 h-1.5 rounded-full ${
                        node.status === 'online' ? 'bg-emerald-500' : 
                        node.status === 'degraded' ? 'bg-amber-500' : 'bg-rose-500'
                      }`} />
                      {node.status}
                    </span>
                  </td>
                  <td className="px-8 py-5">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                        <div className={`h-full rounded-full ${node.sig > 80 ? 'bg-emerald-500' : node.sig > 30 ? 'bg-amber-500' : 'bg-rose-500'}`} style={{ width: `${node.sig}%` }} />
                      </div>
                      <span className="text-[10px] font-black text-slate-400">{node.sig}%</span>
                    </div>
                  </td>
                  <td className="px-8 py-5">
                    <div className="flex items-center gap-3 font-bold text-xs text-slate-500">
                      <Battery className={`w-4 h-4 ${node.bat < 20 ? 'text-rose-500 animate-pulse' : 'text-slate-300'}`} />
                      {node.bat}%
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
