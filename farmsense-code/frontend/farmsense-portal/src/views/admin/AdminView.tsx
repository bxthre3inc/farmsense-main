import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard, Users, TrendingUp, FileSignature,
  Settings, ChevronRight, BarChart3, ShieldCheck,
  Globe, Radio, Activity
} from 'lucide-react';
import { AdminMetrics } from './AdminMetrics';
import { UserList } from './UserList';
import { InvestorManagement } from './InvestorManagement';
import { GrantManager } from './GrantManager';
import { MaterialsLibrary } from './MaterialsLibrary';
import { WaterLedger } from './WaterLedger';
import { FleetDiagnostics } from './FleetDiagnostics';
import { AuditVault } from './AuditVault';
import { AdminSettings } from './AdminSettings';
import { EcologicalCommand } from './EcologicalCommand';
import { PlatformIntelligence } from './PlatformIntelligence';
import { GeospatialIntelligence } from './GeospatialIntelligence';

const AdminView: React.FC = () => {
  const location = useLocation();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const navItems = [
    { path: '/admin', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/admin/users', label: 'User Management', icon: Users },
    { path: '/admin/investors', label: 'Investor Relations', icon: ShieldCheck },
    { path: '/admin/grants', label: 'Grant Manager', icon: FileSignature },
    { path: '/admin/materials', label: 'Materials Hub', icon: FileSignature },
    { path: '/admin/ledger', label: 'Water Ledger', icon: BarChart3 },
    { path: '/admin/fleet', label: 'Fleet Logic', icon: Radio, color: 'text-amber-400' },
    { path: '/admin/intelligence', label: 'Platform Intelligence', icon: BarChart3 },
    { path: '/admin/geospatial', label: 'Geo Intelligence', icon: Globe },
    { path: '/admin/ecological', label: 'Ecological Command', icon: Activity },
    { path: '/admin/audit', label: 'Audit Vault', icon: ShieldCheck, color: 'text-blue-400' },
    { path: '/admin/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className={`${sidebarCollapsed ? 'w-20' : 'w-64'} bg-slate-900 text-slate-300 transition-all duration-300 flex flex-col`}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-emerald-500/20 rounded-xl flex items-center justify-center">
              <ShieldCheck className="w-6 h-6 text-emerald-400" />
            </div>
            {!sidebarCollapsed && (
              <div>
                <div className="text-white font-bold">FarmSense</div>
                <div className="text-xs text-slate-500">Admin Console</div>
              </div>
            )}
          </div>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(item => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path || location.pathname.startsWith(item.path + '/');
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                  isActive
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    : 'hover:bg-slate-800 text-slate-400'
                }`}
              >
                <Icon className="w-5 h-5" />
                {!sidebarCollapsed && <span className="font-bold text-sm">{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-800">
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="w-full flex items-center justify-center p-3 hover:bg-slate-800 rounded-xl transition-all"
          >
            <ChevronRight className={`w-5 h-5 transition-transform ${sidebarCollapsed ? '' : 'rotate-180'}`} />
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <Routes>
          <Route path="/" element={<DashboardOverview />} />
          <Route path="/users" element={<UserList />} />
          <Route path="/investors" element={<InvestorManagement />} />
          <Route path="/grants/*" element={<GrantManager />} />
          <Route path="/materials" element={<MaterialsLibrary />} />
          <Route path="/ledger" element={<WaterLedger />} />
          <Route path="/fleet" element={<FleetDiagnostics />} />
          <Route path="/intelligence" element={<PlatformIntelligence />} />
          <Route path="/geospatial" element={<GeospatialIntelligence />} />
          <Route path="/ecological" element={<EcologicalCommand />} />
          <Route path="/audit" element={<AuditVault />} />
          <Route path="/settings" element={<AdminSettings />} />
        </Routes>
      </main>
    </div>
  );
};

const DashboardOverview: React.FC = () => {
  return (
    <div className="p-8">
      <div className="mb-12">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Platform Command</h1>
        <p className="text-slate-500 mt-1 font-medium italic">Strategic overview of FarmSense global assets.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-12">
        {/* Grant Pulse */}
        <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-emerald-500/5 rounded-full blur-2xl group-hover:bg-emerald-500/10 transition-all" />
          <div className="flex items-center gap-3 text-emerald-600 mb-4">
            <FileSignature className="w-5 h-5" />
            <span className="text-[10px] font-black uppercase tracking-[0.2em]">Grant Pulse</span>
          </div>
          <p className="text-3xl font-black text-slate-900">$2.85M</p>
          <p className="text-xs text-slate-400 mt-2 font-bold">15 Active Applications</p>
        </div>

        {/* Ledger Integrity */}
        <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-blue-500/5 rounded-full blur-2xl group-hover:bg-blue-500/10 transition-all" />
          <div className="flex items-center gap-3 text-blue-600 mb-4">
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Strategic ROI</p>
                <p className="text-2xl font-black text-emerald-400">$2.4M</p>
                <p className="text-[9px] text-slate-400 mt-1">12-month projected</p>
            </div>
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Ecological Health</p>
                <p className="text-2xl font-black text-emerald-400">OPTIMAL</p>
                <p className="text-[9px] text-slate-400 mt-1">Spatial stability: High</p>
            </div>
          </div>
          <p className="text-3xl font-black text-slate-900">100.0%</p>
          <p className="text-xs text-slate-400 mt-2 font-bold">AllianceChain Verfied</p>
        </div>

        {/* Fleet Heartbeat */}
        <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-rose-500/5 rounded-full blur-2xl group-hover:bg-rose-500/10 transition-all" />
          <div className="flex items-center gap-3 text-rose-600 mb-4">
            <Activity className="w-5 h-5" />
            <span className="text-[10px] font-black uppercase tracking-[0.2em]">Fleet Sync</span>
          </div>
          <p className="text-3xl font-black text-slate-900">94.8%</p>
          <p className="text-xs text-slate-400 mt-2 font-bold text-rose-500">2 Nodes Requiring Sync</p>
        </div>

        {/* Investor Momentum */}
        <div className="bg-slate-900 p-6 rounded-3xl text-white relative overflow-hidden group">
          <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-emerald-500/10 rounded-full blur-2xl group-hover:bg-emerald-500/20 transition-all" />
          <div className="flex items-center gap-3 text-emerald-400 mb-4">
            <TrendingUp className="w-5 h-5" />
            <span className="text-[10px] font-black uppercase tracking-[0.2em]">IR Pipeline</span>
          </div>
          <p className="text-3xl font-black">$2.4M</p>
          <p className="text-xs text-slate-400 mt-2 font-bold">18% Series A Claimed</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <AdminMetrics />
        </div>
        <div className="flex flex-col gap-8">
          <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm border-l-4 border-l-emerald-500">
            <h3 className="font-black text-slate-900 mb-2">Statutory Compliance Ready</h3>
            <p className="text-sm text-slate-500 leading-relaxed mb-6">Regional water ledger is synchronized and valid for June 29 Water Court hearing evidence.</p>
            <Link to="/admin/ledger" className="text-xs font-black text-emerald-600 uppercase tracking-widest hover:text-emerald-700">Open Legal Vault →</Link>
          </div>

          <div className="bg-slate-50 p-8 rounded-3xl border border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-4">
               <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center shadow-sm">
                 <ShieldCheck className="w-6 h-6 text-slate-400" />
               </div>
               <div>
                 <p className="text-sm font-black text-slate-900">System Security</p>
                 <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Master Quorum Active</p>
               </div>
            </div>
            <Link to="/admin/audit" className="p-3 bg-white hover:bg-slate-100 rounded-xl border border-slate-200 transition-all">
              <ChevronRight className="w-5 h-5 text-slate-400" />
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminView;