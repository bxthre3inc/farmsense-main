import React, { useState } from 'react';
import { Search, Copy, CheckCircle2, BookOpen, Globe, Shield, Users, DollarSign, Leaf } from 'lucide-react';

const materials = [
  {
    category: "Organization Profile",
    icon: Globe,
    items: [
      { title: "Standard Bio (250 words)", content: "Bxthre3 Inc. is a Colorado-based venture studio building deterministic infrastructure systems for agriculture, water, and logistics. Founded in 2026, we develop technology that solves resource scarcity through AI, robotics, and edge computing.\n\nOur flagship program, FarmSense, is a precision agriculture operating system that reduces irrigation water usage by 20-40% while increasing crop yields 15-25%..." },
      { title: "Short Bio (100 words)", content: "Bxthre3 Inc. builds deterministic infrastructure systems for agriculture and water management. Our FarmSense platform combines AI, IoT, and edge computing to reduce irrigation water usage 20-40% while increasing yields 15-25%." },
      { title: "Elevator Pitch", content: "FarmSense is the operating system for precision agriculture. We cut water use 20-40% and boost yields 15-25% using AI-powered sensors and edge computing. Think Tesla Autopilot for irrigation." }
    ]
  },
  {
    category: "Problem Statements",
    icon: Shield,
    items: [
      { title: "Universal Water Scarcity", content: "Global water demand is projected to exceed supply by 40% by 2030. Agriculture consumes 70% of freshwater withdrawals, yet irrigation remains largely unmanaged — growers over-water by 30-50% due to lack of real-time data." },
      { title: "Defense/Federal Focus", content: "Military installations face dual water crises: operational (maintaining readiness during drought) and infrastructure (aging distribution systems with 30%+ leakage). Current telemetry relies on cloud connectivity — vulnerable in contested environments." }
    ]
  },
  {
    category: "Impact Metrics",
    icon: Leaf,
    items: [
      { title: "Environmental Outcomes", content: "• Water conserved: 50-80 acre-feet annually (per 100 acres)\n• Energy reduced: 12-18 MWh (pump efficiency)\n• Carbon avoided: 8-12 tonnes CO2e" },
      { title: "Economic Development", content: "• Farmer income increase: 15-25% from yield optimization\n• Water cost reduction: 20-40% from efficiency gains\n• ROI: 300-500% over 5 years" }
    ]
  }
];

export const MaterialsLibrary: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-900">Strategic Materials Hub</h1>
        <p className="text-slate-500 mt-1">Ready-to-use institutional assets for grants, IR, and policy.</p>
      </div>

      <div className="relative mb-12">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
        <input 
          type="text" 
          placeholder="Search materials library (bio, impact, budget)..."
          className="w-full pl-12 pr-4 py-4 bg-white border border-slate-200 rounded-2xl focus:ring-2 focus:ring-emerald-500 outline-none transition-all shadow-sm font-medium"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="space-y-16">
        {materials.map((cat) => (
          <section key={cat.category}>
            <div className="flex items-center gap-3 mb-8">
              <div className="w-12 h-12 bg-slate-900 text-white rounded-2xl flex items-center justify-center shadow-xl shadow-slate-200">
                <cat.icon className="w-6 h-6" />
              </div>
              <h2 className="text-2xl font-black text-slate-900">{cat.category}</h2>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
              {cat.items.map((item, idx) => {
                const id = `${cat.category}-${idx}`;
                return (
                  <div key={id} className="bg-white border border-slate-100 rounded-3xl p-8 hover:shadow-2xl hover:shadow-slate-200/50 transition-all flex flex-col group relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button 
                        onClick={() => handleCopy(item.content, id)}
                        className={`p-3 rounded-xl transition-all ${copiedId === id ? 'bg-emerald-500 text-white' : 'bg-slate-50 text-slate-400 hover:text-slate-900 hover:bg-slate-100'}`}
                      >
                        {copiedId === id ? <CheckCircle2 className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                      </button>
                    </div>

                    <h3 className="text-lg font-black text-slate-800 mb-4">{item.title}</h3>
                    <div className="text-slate-600 text-sm leading-relaxed whitespace-pre-line bg-slate-50/50 p-6 rounded-2xl border border-slate-50">
                      {item.content}
                    </div>
                    {copiedId === id && (
                      <div className="absolute inset-0 bg-emerald-500/5 backdrop-blur-[2px] pointer-events-none flex items-center justify-center">
                        <span className="bg-emerald-500 text-white px-4 py-2 rounded-full font-bold text-xs shadow-lg">Copied to Dashboard</span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
};
