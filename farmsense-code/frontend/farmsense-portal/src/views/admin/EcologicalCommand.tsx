import React, { useState, useEffect } from 'react';
import { Globe, ShieldCheck, Zap, Activity, Grid, Layers, Crosshair, BarChart3, Info, AlertTriangle, TrendingUp, Download } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

// Mock data for the 1m resolution soil variability grid (16x16)
const mockSoilGrid = () => {
    return Array.from({ length: 16 }, (_, row) =>
        Array.from({ length: 16 }, (_, col) => {
            const v = 0.28 + Math.sin(row / 4) * 0.12 + Math.cos(col / 5) * 0.08 + Math.random() * 0.04;
            return parseFloat(v.toFixed(3));
        })
    );
};

// Mock Kriging Integrity Metrics over time
const mockIntegrityHistory = [
    { time: '08:00', mape: 3.2, rmse: 0.012, samples: 22 },
    { time: '10:00', mape: 3.5, rmse: 0.014, samples: 24 },
    { time: '12:00', mape: 2.8, rmse: 0.011, samples: 26 },
    { time: '14:00', mape: 4.1, rmse: 0.016, samples: 25 },
    { time: '16:00', mape: 3.6, rmse: 0.015, samples: 28 },
    { time: '18:00', mape: 3.1, rmse: 0.013, samples: 30 },
];

const moistureColor = (v: number): string => {
    if (v > 0.42) return '#10b981'; // Optimal (Emerald)
    if (v > 0.34) return '#34d399'; // Good
    if (v > 0.28) return '#fbbf24'; // Monitor (Amber)
    if (v > 0.22) return '#f97316'; // Stressed (Orange)
    return '#ef4444'; // Critical (Red)
};

export const EcologicalCommand: React.FC = () => {
    const [grid, setGrid] = useState(mockSoilGrid());
    const [selectedPixel, setSelectedPixel] = useState<{ r: number, c: number } | null>(null);
    const [integrityScore] = useState(96.8);
    const [activeFusion, setActiveFusion] = useState<'moisture' | 'ndvi' | 'lst'>('moisture');

    const handlePixelClick = (r: number, c: number) => {
        setSelectedPixel({ r, c });
    };

    return (
        <div className="p-6 space-y-6 bg-[#050308] min-h-full text-slate-300">
            {/* Header section with C2 branding */}
            <div className="flex items-center justify-between border-b border-purple-900/30 pb-5">
                <div className="flex items-center gap-4">
                    <div className="bg-emerald-600/20 p-3 rounded-2xl border border-emerald-500/20">
                        <Globe className="w-6 h-6 text-emerald-400" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-black text-white uppercase tracking-tighter">Ecological Command</h1>
                        <p className="text-[10px] text-emerald-500 font-mono uppercase tracking-widest mt-1">Biophysical Integrity & Real-Time Soil Variability</p>
                    </div>
                </div>
                <div className="flex items-center gap-3">
                    <div className="px-4 py-2 bg-black/40 border border-purple-900/30 rounded-xl flex items-center gap-3">
                        <div className="flex flex-col items-end">
                            <span className="text-[9px] font-bold text-slate-500 uppercase">Integrity Score</span>
                            <span className="text-sm font-black text-emerald-400">{integrityScore}%</span>
                        </div>
                        <ShieldCheck className="w-5 h-5 text-emerald-500" />
                    </div>
                    <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2.5 rounded-xl transition-all shadow-lg shadow-emerald-900/20 text-xs font-black uppercase tracking-widest">
                        <Download className="w-4 h-4" /> Export GeoTIFF
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                {/* Left Column: High-Res Map Explorer */}
                <div className="lg:col-span-8 flex flex-col gap-6">
                    <div className="bg-[#0A0713] rounded-3xl border border-purple-900/20 p-6 shadow-2xl relative overflow-hidden">
                        <div className="flex items-center justify-between mb-6">
                            <div className="flex items-center gap-4">
                                <Grid className="w-5 h-5 text-purple-400" />
                                <h2 className="text-sm font-bold text-white uppercase tracking-widest">1m Resolution Spatial Matrix</h2>
                            </div>
                            <div className="flex bg-black/40 p-1 rounded-xl border border-white/5">
                                {(['moisture', 'ndvi', 'lst'] as const).map(mode => (
                                    <button
                                        key={mode}
                                        onClick={() => setActiveFusion(mode)}
                                        className={`px-4 py-1.5 rounded-lg text-[10px] font-bold transition-all uppercase ${activeFusion === mode ? 'bg-emerald-600 text-white' : 'text-slate-500 hover:text-slate-300'}`}
                                    >
                                        {mode}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="grid grid-cols-16 gap-1 bg-black/20 p-2 rounded-2xl border border-white/5 aspect-square lg:aspect-video max-h-[500px] overflow-hidden">
                            {grid.map((row, r) => 
                                row.map((val, c) => (
                                    <div 
                                        key={`${r}-${c}`}
                                        onClick={() => handlePixelClick(r, c)}
                                        className={`aspect-square rounded-sm cursor-crosshair transition-all hover:scale-125 hover:z-10 border border-black/20 ${selectedPixel?.r === r && selectedPixel?.c === c ? 'ring-2 ring-white scale-110 z-20' : ''}`}
                                        style={{ backgroundColor: moistureColor(val) + 'dd' }}
                                        title={`Pixel [${r},${c}]: ${val}`}
                                    />
                                ))
                            )}
                        </div>

                        <div className="mt-6 flex items-center justify-between">
                            <div className="flex gap-4 text-[9px] font-bold text-slate-500 uppercase tracking-widest">
                                <span className="flex items-center gap-1.5"><div className="w-3 h-3 rounded-sm bg-[#ef4444]" /> Critical</span>
                                <span className="flex items-center gap-1.5"><div className="w-3 h-3 rounded-sm bg-[#f97316]" /> Stress</span>
                                <span className="flex items-center gap-1.5"><div className="w-3 h-3 rounded-sm bg-[#fbbf24]" /> Monitor</span>
                                <span className="flex items-center gap-1.5"><div className="w-3 h-3 rounded-sm bg-[#34d399]" /> Optimal</span>
                            </div>
                            <div className="flex items-center gap-2 text-[10px] text-purple-400 font-mono">
                                <Layers className="w-3 h-3" /> FHE ENCLAVE: RSS-1M-HIGH-FIDELITY
                            </div>
                        </div>
                    </div>

                    {/* Pixel Diagnostics */}
                    <div className="bg-[#0A0713] rounded-3xl border border-purple-900/20 p-6">
                        <div className="flex items-center gap-3 mb-6">
                            <Crosshair className="w-5 h-5 text-blue-400" />
                            <h2 className="text-sm font-bold text-white uppercase tracking-widest">Spectral Pixel Inspector</h2>
                        </div>
                        {selectedPixel ? (
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="bg-black/40 border border-white/5 p-4 rounded-2xl">
                                    <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">Volumetric SWC</p>
                                    <p className="text-xl font-black text-emerald-400 font-mono">{(grid[selectedPixel.r][selectedPixel.c] * 100).toFixed(1)}%</p>
                                </div>
                                <div className="bg-black/40 border border-white/5 p-4 rounded-2xl">
                                    <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">NDVI Proxy</p>
                                    <p className="text-xl font-black text-blue-400 font-mono">{(0.68 + (Math.random() * 0.1)).toFixed(2)}</p>
                                </div>
                                <div className="bg-black/40 border border-white/5 p-4 rounded-2xl">
                                    <p className="text-[10px] font-bold text-slate-500 uppercase mb-1">Thermal LST</p>
                                    <p className="text-xl font-black text-amber-400 font-mono">{(32.4 + (Math.random() * 2)).toFixed(1)}°C</p>
                                </div>
                                <div className="bg-black/40 border border-white/5 p-4 rounded-2xl">
                                    <p className="text-[10px] font-bold text-red-500 uppercase mb-1">Stress Risk</p>
                                    <p className="text-xl font-black text-red-400 font-mono">LOW</p>
                                </div>
                            </div>
                        ) : (
                            <div className="flex flex-col items-center justify-center py-8 text-slate-600">
                                <Info className="w-8 h-8 mb-2 opacity-20" />
                                <p className="text-xs italic uppercase tracking-widest font-bold">Select a pixel on the matrix to view biophysical telemetry</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Right Column: Integrity & Variance Analytics */}
                <div className="lg:col-span-4 space-y-6">
                    {/* Kriging Quality Control */}
                    <div className="bg-[#0A0713] rounded-3xl border border-emerald-900/20 p-6 overflow-hidden relative">
                        <div className="absolute top-0 right-0 p-4 opacity-10">
                            <Activity className="w-24 h-24 text-emerald-500" />
                        </div>
                        <h3 className="text-xs font-black text-white uppercase tracking-widest mb-6 flex items-center gap-2">
                             <TrendingUp className="w-4 h-4 text-emerald-400" /> Kriging Accuracy (MAPE)
                        </h3>
                        <div className="h-48">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={mockIntegrityHistory}>
                                    <defs>
                                        <linearGradient id="colorMape" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                                            <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#1e0a3e" vertical={false} />
                                    <XAxis dataKey="time" stroke="#475569" fontSize={10} axisLine={false} tickLine={false} />
                                    <YAxis stroke="#475569" fontSize={10} axisLine={false} tickLine={false} domain={[0, 6]} />
                                    <Tooltip 
                                        contentStyle={{ backgroundColor: '#070511', border: '1px solid #1e0a3e', borderRadius: '12px', fontSize: '10px' }}
                                        itemStyle={{ color: '#10b981', fontWeight: 'bold' }}
                                    />
                                    <Area type="monotone" dataKey="mape" stroke="#10b981" fillOpacity={1} fill="url(#colorMape)" strokeWidth={3} />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="mt-4 grid grid-cols-2 gap-4">
                            <div className="text-center">
                                <p className="text-[9px] font-bold text-slate-500 uppercase">Mean Error</p>
                                <p className="text-lg font-black text-white font-mono">3.4%</p>
                            </div>
                            <div className="text-center">
                                <p className="text-[9px] font-bold text-slate-500 uppercase">Court Threshold</p>
                                <p className="text-lg font-black text-emerald-400 font-mono">5.0%</p>
                            </div>
                        </div>
                    </div>

                    {/* Systematic Anomalies */}
                    <div className="bg-[#0A0713] rounded-3xl border border-red-900/20 p-6">
                        <h3 className="text-xs font-black text-white uppercase tracking-widest mb-4 flex items-center gap-2">
                             <AlertTriangle className="w-4 h-4 text-red-400" /> Ecological Anomalies
                        </h3>
                        <div className="space-y-3">
                            {[
                                { id: 'ANOM-01', type: 'Moisture Discrepancy', location: 'SW Quadrant', severity: 'Medium', time: '14:22' },
                                { id: 'ANOM-02', type: 'Sensor Drift Delta', location: 'Node RSS-02', severity: 'Low', time: '15:10' },
                                { id: 'ANOM-03', type: 'Kriging Variance Peak', location: 'Central Ridge', severity: 'High', time: '16:05' },
                            ].map(anom => (
                                <div key={anom.id} className="p-3 bg-black/40 rounded-xl border border-white/5 hover:border-red-900/30 transition-all group flex items-start gap-3">
                                    <div className={`p-1.5 rounded-lg ${anom.severity === 'High' ? 'bg-red-500/20 text-red-500' : anom.severity === 'Medium' ? 'bg-amber-500/20 text-amber-500' : 'bg-slate-500/20 text-slate-400'}`}>
                                        <Zap className="w-3.5 h-3.5" />
                                    </div>
                                    <div className="flex-1">
                                        <div className="flex justify-between items-center mb-0.5">
                                            <span className="text-[10px] font-black text-white">{anom.type}</span>
                                            <span className="text-[9px] font-mono text-slate-600">{anom.time}</span>
                                        </div>
                                        <p className="text-[9px] text-slate-500">{anom.location} • <span className={anom.severity === 'High' ? 'text-red-400' : ''}>{anom.severity} Impact</span></p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Regional Stress Index */}
                    <div className="bg-gradient-to-br from-emerald-950/20 to-slate-950 p-6 rounded-3xl border border-white/5">
                        <div className="flex items-center gap-2 mb-4">
                            <BarChart3 className="w-4 h-4 text-emerald-400" />
                            <h3 className="text-xs font-black text-white uppercase tracking-widest">Master Stress Index</h3>
                        </div>
                        <div className="space-y-4">
                            {[
                                { label: 'Basin Hydration', value: 88, color: 'bg-emerald-500' },
                                { label: 'Spectral Vigor', value: 72, color: 'bg-blue-500' },
                                { label: 'Thermal Stability', value: 91, color: 'bg-amber-500' },
                            ].map(idx => (
                                <div key={idx.label} className="space-y-1">
                                    <div className="flex justify-between text-[9px] font-bold uppercase tracking-widest">
                                        <span className="text-slate-400">{idx.label}</span>
                                        <span className="text-white">{idx.value}%</span>
                                    </div>
                                    <div className="h-1.5 w-full bg-black/40 rounded-full overflow-hidden">
                                        <div className={`h-full ${idx.color}`} style={{ width: `${idx.value}%` }} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EcologicalCommand;
