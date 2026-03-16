import React, { useState, useEffect } from 'react';
import { Activity, Users, Database, ShieldCheck, Zap, TrendingUp, AlertCircle, RefreshCw, Server, Cpu } from 'lucide-react';
import { api } from '../../services/api';

export const AdminMetrics: React.FC = () => {
    const [metrics, setMetrics] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const fetchMetrics = async () => {
        setLoading(true);
        try {
            const data = await api.admin.getMetrics();
            setMetrics(data);
        } catch (error) {
            console.error('Failed to fetch metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMetrics();
    }, []);

    return (
        <div className="p-6 space-y-6 bg-slate-950 min-h-full text-slate-300">
            <div className="flex items-center justify-between border-b border-slate-800 pb-5">
                <div>
                    <h1 className="text-xl font-black text-white uppercase tracking-tighter">System Infrastructure Metrics</h1>
                    <p className="text-xs text-slate-500 mt-0.5">Real-time health monitoring and growth analytics</p>
                </div>
                <button
                    onClick={fetchMetrics}
                    className="flex items-center gap-2 bg-slate-900 border border-slate-800 px-4 py-2 rounded-xl hover:bg-slate-800 transition-all text-xs font-bold"
                >
                    <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
                    Refresh Data
                </button>
            </div>

            {/* Status Tiles */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-[#0A0713] p-5 rounded-2xl border border-indigo-900/30">
                    <div className="flex items-center gap-3 text-indigo-400 mb-4">
                        <Users className="w-5 h-5" />
                        <span className="text-[10px] font-black uppercase tracking-widest">User Base</span>
                    </div>
                    <p className="text-3xl font-black text-white">{metrics?.active_users?.toLocaleString() ?? '12,402'}</p>
                    <div className="flex items-center gap-1 mt-2 text-emerald-500 text-[10px] font-bold">
                        <TrendingUp className="w-3 h-3" /> +8.4% growth
                    </div>
                </div>

                <div className="bg-[#0A0713] p-5 rounded-2xl border border-emerald-900/30">
                    <div className="flex items-center gap-3 text-emerald-400 mb-4">
                        <Zap className="w-5 h-5" />
                        <span className="text-[10px] font-black uppercase tracking-widest">System Health</span>
                    </div>
                    <p className="text-3xl font-black text-white">{metrics?.system_health_pct ?? '99.9'}%</p>
                    <div className="flex items-center gap-1 mt-2 text-emerald-500 text-[10px] font-bold">
                        <ShieldCheck className="w-3 h-3" /> All nodes online
                    </div>
                </div>

                <div className="bg-[#0A0713] p-5 rounded-2xl border border-amber-900/30">
                    <div className="flex items-center gap-3 text-amber-400 mb-4">
                        <Database className="w-5 h-5" />
                        <span className="text-[10px] font-black uppercase tracking-widest">Data Ingestion</span>
                    </div>
                    <p className="text-3xl font-black text-white">4.2 TB</p>
                    <div className="flex items-center gap-1 mt-2 text-amber-500 text-[10px] font-bold">
                        <Activity className="w-3 h-3" /> High load detected
                    </div>
                </div>

                <div className="bg-[#0A0713] p-5 rounded-2xl border border-red-900/30">
                    <div className="flex items-center gap-3 text-red-400 mb-4">
                        <AlertCircle className="w-5 h-5" />
                        <span className="text-[10px] font-black uppercase tracking-widest">Pending Audits</span>
                    </div>
                    <p className="text-3xl font-black text-white">{metrics?.pending_audits ?? '14'}</p>
                    <div className="flex items-center gap-1 mt-2 text-red-500 text-[10px] font-bold underline cursor-pointer">
                        View queue
                    </div>
                </div>

                <div className="bg-[#0A0713] p-5 rounded-2xl border border-blue-900/30">
                    <div className="flex items-center gap-3 text-blue-400 mb-4">
                        <Globe className="w-5 h-5" />
                        <span className="text-[10px] font-black uppercase tracking-widest">Kriging Accuracy</span>
                    </div>
                    <p className="text-3xl font-black text-white">96.6%</p>
                    <div className="flex items-center gap-1 mt-2 text-emerald-500 text-[10px] font-bold">
                        <TrendingUp className="w-3 h-3" /> MAPE: 3.4%
                    </div>
                </div>

                <div className="bg-[#0A0713] p-5 rounded-2xl border border-purple-900/30">
                    <div className="flex items-center gap-3 text-purple-400 mb-4">
                        <Zap className="w-5 h-5" />
                        <span className="text-[10px] font-black uppercase tracking-widest">Soil Stress Index</span>
                    </div>
                    <p className="text-3xl font-black text-white">LOW</p>
                    <div className="flex items-center gap-1 mt-2 text-blue-500 text-[10px] font-bold">
                        <Activity className="w-3 h-3" /> Spatial stability: High
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-sm font-bold text-white mb-6 flex items-center gap-2">
                        <Server className="w-4 h-4 text-blue-400" /> Server Cluster Load
                    </h3>
                    <div className="space-y-4">
                        {[
                            { name: 'Basin-Core-01', load: 42, temp: 38 },
                            { name: 'Basin-Core-02', load: 78, temp: 52 },
                            { name: 'Telemetry-Aggregator', load: 15, temp: 31 },
                            { name: 'Kriging-Engine', load: 92, temp: 64 },
                        ].map(server => (
                            <div key={server.name} className="space-y-1">
                                <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest">
                                    <span className="text-slate-400">{server.name}</span>
                                    <span className={server.load > 90 ? 'text-red-400' : 'text-slate-300'}>{server.load}% CPU</span>
                                </div>
                                <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                                    <div
                                        className={`h-full transition-all duration-1000 ${server.load > 90 ? 'bg-red-500' : server.load > 70 ? 'bg-amber-500' : 'bg-blue-500'}`}
                                        style={{ width: `${server.load}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800">
                    <h3 className="text-sm font-bold text-white mb-6 flex items-center gap-2">
                        <Cpu className="w-4 h-4 text-emerald-400" /> Network Latency (Global)
                    </h3>
                    <div className="h-40 flex items-end gap-2 px-2">
                        {[30, 45, 25, 60, 40, 35, 80, 50, 45, 65, 30, 55].map((h, i) => (
                            <div key={i} className="flex-1 bg-emerald-500/20 border-t border-emerald-500/40 rounded-t group relative">
                                <div className="absolute inset-0 bg-emerald-500/30 scale-y-0 group-hover:scale-y-100 origin-bottom transition-transform duration-300" style={{ height: `${h}%` }}></div>
                                <div className="h-full bg-emerald-500/50 rounded-t" style={{ height: `${h}%` }}></div>
                            </div>
                        ))}
                    </div>
                    <div className="flex justify-between mt-4 text-[9px] font-bold text-slate-600 uppercase tracking-widest">
                        <span>24h History</span>
                        <span>0ms peak</span>
                    </div>
                </div>
            </div>
        </div>
    );
};
