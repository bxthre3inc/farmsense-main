import React, { useState } from 'react';
import { TrendingUp, BarChart3, PieChart, Target, Zap, Activity, Users, DollarSign, ArrowUpRight, ArrowDownRight, Info, Search } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, AreaChart, Area, ComposedChart, Bar, Legend } from 'recharts';

// Mock data for Master Intelligence
const mockPerformanceData = [
    { month: 'Jan', revenue: 45000, costs: 32000, efficiency: 84 },
    { month: 'Feb', revenue: 52000, costs: 31000, efficiency: 88 },
    { month: 'Mar', revenue: 48000, costs: 35000, efficiency: 82 },
    { month: 'Apr', revenue: 61000, costs: 38000, efficiency: 91 },
    { month: 'May', revenue: 59000, costs: 36000, efficiency: 89 },
    { month: 'Jun', revenue: 72000, costs: 42000, efficiency: 94 },
    { month: 'Jul', revenue: 85000, costs: 45000, efficiency: 96 },
];

const mockCohortData = [
    { name: 'Tier 1 (High Efficiency)', value: 142, color: '#10b981' },
    { name: 'Tier 2 (Stable)', value: 385, color: '#3b82f6' },
    { name: 'Tier 3 (Underperforming)', value: 94, color: '#f59e0b' },
    { name: 'Tier 4 (Critical)', value: 23, color: '#ef4444' },
];

const mockInsights = [
    { id: 1, type: 'positive', content: 'Regional ROI projected to increase by 12% following RSS-1M-FHE deployment.' },
    { id: 2, type: 'warning', content: 'Cohort 3 shows 18% higher sensor drift than global average. Calibration recommended.' },
    { id: 3, type: 'neutral', content: 'Grant pipeline velocity stabilized at 4.2 applications/week.' },
];

export const PlatformIntelligence: React.FC = () => {
    const [timeRange, setTimeRange] = useState('6M');

    return (
        <div className="p-6 space-y-6 bg-[#050308] min-h-full text-slate-300">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-purple-900/30 pb-5">
                <div className="flex items-center gap-4">
                    <div className="bg-purple-600/20 p-3 rounded-2xl border border-purple-500/20">
                        <Target className="w-6 h-6 text-purple-400" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-black text-white uppercase tracking-tighter">Master Intelligence</h1>
                        <p className="text-[10px] text-purple-500 font-mono uppercase tracking-widest mt-1">Deep Platform Analytics & Strategic ROI Synthesis</p>
                    </div>
                </div>
                <div className="flex gap-2">
                    {['1M', '3M', '6M', '1Y', 'ALL'].map(range => (
                        <button
                            key={range}
                            onClick={() => setTimeRange(range)}
                            className={`px-3 py-1.5 rounded-lg text-[10px] font-bold transition-all ${timeRange === range ? 'bg-purple-600 text-white' : 'bg-black/40 text-slate-500 hover:text-slate-300 border border-white/5'}`}
                        >
                            {range}
                        </button>
                    ))}
                </div>
            </div>

            {/* High-Level Pulse Widgets */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {[
                    { label: 'Platform ROI', value: '$2.4M', trend: '+14.2%', icon: DollarSign, color: 'text-emerald-400' },
                    { label: 'Growth Velocity', value: '4.8x', trend: '+0.4x', icon: TrendingUp, color: 'text-blue-400' },
                    { label: 'Active Cohorts', value: '12', trend: 'Stable', icon: Users, color: 'text-purple-400' },
                    { label: 'Resource Efficiency', value: '91.4%', trend: '-2.1%', icon: Zap, color: 'text-amber-400' },
                ].map(stat => (
                    <div key={stat.label} className="bg-[#0A0713] p-5 rounded-2xl border border-white/5 flex items-center justify-between">
                        <div>
                            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">{stat.label}</p>
                            <p className="text-2xl font-black text-white">{stat.value}</p>
                            <p className={`text-[10px] font-bold mt-1 flex items-center gap-1 ${stat.trend.startsWith('+') ? 'text-emerald-500' : stat.trend === 'Stable' ? 'text-slate-500' : 'text-red-500'}`}>
                                {stat.trend.startsWith('+') ? <ArrowUpRight className="w-3 h-3" /> : stat.trend.startsWith('-') ? <ArrowDownRight className="w-3 h-3" /> : null}
                                {stat.trend}
                            </p>
                        </div>
                        <stat.icon className={`w-8 h-8 ${stat.color} opacity-20`} />
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                {/* Main Performance Synthesis Chart */}
                <div className="lg:col-span-8 bg-[#0A0713] rounded-3xl border border-purple-900/20 p-6">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h3 className="text-sm font-black text-white uppercase tracking-widest flex items-center gap-2">
                                <Activity className="w-4 h-4 text-purple-400" /> Deep Performance Synthesis
                            </h3>
                            <p className="text-[10px] text-slate-500 mt-1">Correlating Revenue, Operational Cost, and Biophysical Efficiency</p>
                        </div>
                        <div className="flex items-center gap-4 text-[9px] font-bold uppercase">
                            <span className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-emerald-500" /> Revenue</span>
                            <span className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-red-500" /> Costs</span>
                            <span className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-purple-500" /> Efficiency</span>
                        </div>
                    </div>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <ComposedChart data={mockPerformanceData}>
                                <defs>
                                    <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.2} />
                                        <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e0a3e" vertical={false} />
                                <XAxis dataKey="month" stroke="#475569" fontSize={10} axisLine={false} tickLine={false} />
                                <YAxis yAxisId="left" stroke="#475569" fontSize={10} axisLine={false} tickLine={false} />
                                <YAxis yAxisId="right" orientation="right" stroke="#475569" fontSize={10} axisLine={false} tickLine={false} domain={[0, 100]} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#070511', border: '1px solid #1e0a3e', borderRadius: '12px', fontSize: '10px' }}
                                />
                                <Area yAxisId="left" type="monotone" dataKey="revenue" fill="url(#colorRev)" stroke="#10b981" strokeWidth={3} />
                                <Bar yAxisId="left" dataKey="costs" barSize={12} fill="#ef4444" radius={[4, 4, 0, 0]} />
                                <Line yAxisId="right" type="step" dataKey="efficiency" stroke="#a855f7" strokeWidth={3} dot={{ fill: '#a855f7', r: 4 }} />
                            </ComposedChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Cohort Analysis & Insights */}
                <div className="lg:col-span-4 space-y-6">
                    {/* Cohort Distribution */}
                    <div className="bg-[#0A0713] rounded-3xl border border-white/5 p-6">
                        <h3 className="text-xs font-black text-white uppercase tracking-widest mb-6 flex items-center gap-2">
                            <PieChart className="w-4 h-4 text-blue-400" /> Cohort Distribution
                        </h3>
                        <div className="space-y-4">
                            {mockCohortData.map(cohort => (
                                <div key={cohort.name} className="space-y-1">
                                    <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest">
                                        <span className="text-slate-400">{cohort.name}</span>
                                        <span className="text-white">{cohort.value} assets</span>
                                    </div>
                                    <div className="h-2 w-full bg-black/40 rounded-full overflow-hidden">
                                        <div
                                            className="h-full transition-all duration-1000"
                                            style={{ width: `${(cohort.value / 644) * 100}%`, backgroundColor: cohort.color }}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Executive Pulse Insights */}
                    <div className="bg-[#0A0713] rounded-3xl border border-purple-900/20 p-6">
                        <h3 className="text-xs font-black text-white uppercase tracking-widest mb-4 flex items-center gap-2">
                             <TrendingUp className="w-4 h-4 text-purple-400" /> Executive Pulse
                        </h3>
                        <div className="space-y-3">
                            {mockInsights.map(insight => (
                                <div key={insight.id} className="p-3 bg-black/40 rounded-xl border border-white/5 flex items-start gap-3">
                                    <div className={`p-1.5 rounded-lg ${insight.type === 'positive' ? 'bg-emerald-500/10 text-emerald-500' : insight.type === 'warning' ? 'bg-amber-500/10 text-amber-500' : 'bg-slate-500/10 text-slate-400'}`}>
                                        <Info className="w-3.5 h-3.5" />
                                    </div>
                                    <p className="text-[10px] leading-relaxed text-slate-300">
                                        {insight.content}
                                    </p>
                                </div>
                            ))}
                        </div>
                        <button className="w-full mt-4 py-2 text-[10px] font-bold text-purple-400 border border-purple-900/30 rounded-xl hover:bg-purple-900/10 transition-all uppercase tracking-widest">
                            Generate Full Report
                        </button>
                    </div>
                </div>
            </div>

            {/* Bottom Row: Predictive ROI & Global Anomaly Heatmap */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-[#0A0713] rounded-3xl border border-white/5 p-6">
                    <h3 className="text-sm font-black text-white uppercase tracking-widest mb-6 flex items-center gap-2">
                        <Target className="w-4 h-4 text-emerald-400" /> 12-Month ROI Forecasting
                    </h3>
                    <div className="h-60">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={mockPerformanceData}>
                                <XAxis dataKey="month" hide />
                                <YAxis hide domain={[0, 100000]} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#070511', border: '1px solid #1e0a3e', borderRadius: '12px', fontSize: '10px' }}
                                />
                                <Area type="monotone" dataKey="revenue" stroke="#10b981" fill="#10b981" fillOpacity={0.1} strokeWidth={2} strokeDasharray="5 5" name="Forecasted Revenue" />
                                <Area type="monotone" dataKey="costs" stroke="#ef4444" fill="#ef4444" fillOpacity={0.1} strokeWidth={2} strokeDasharray="5 5" name="Forecasted Costs" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="bg-gradient-to-br from-[#0A0713] to-[#1a0c2e] rounded-3xl border border-purple-900/30 p-8 flex flex-col items-center justify-center text-center">
                    <div className="bg-purple-500/20 p-4 rounded-full mb-4">
                        <PieChart className="w-12 h-12 text-purple-400" />
                    </div>
                    <h4 className="text-xl font-black text-white uppercase tracking-tighter mb-2">Omni-Channel Synthesis Ready</h4>
                    <p className="text-xs text-slate-400 max-w-sm">
                        Financial, Operational, and Biophysical data streams are fully synchronized in the Secure Enclave.
                    </p>
                    <button className="mt-6 flex items-center gap-2 bg-white text-black px-6 py-3 rounded-full text-xs font-black uppercase tracking-widest hover:scale-105 transition-all">
                        <Search className="w-4 h-4" /> Deep Dive Analysis
                    </button>
                </div>
            </div>
        </div>
    );
};

export default PlatformIntelligence;
