import React, { useState } from 'react';
import { api } from '../../services/api';
import { Drawer } from '../../components/ui/Drawer';

// Modular imports
import { User } from './user-list/types';
import { UserEditForm } from './user-list/components/UserEditForm';
import { UserModalSidebar } from './user-list/components/UserModalSidebar';

interface UserModalProps {
    user: User;
    onClose: () => void;
    onUpdate: () => void;
}

export const UserModal: React.FC<UserModalProps> = ({ user, onClose, onUpdate }) => {
    const [activeTab, setActiveTab] = useState<'profile' | 'interactions' | 'security'>('profile');

    const handleSave = async () => {
        setIsSaving(true);
        try {
            await api.admin.updateUser(user.id, formData);
            setSuccess(true);
            setTimeout(() => {
                setSuccess(false);
                onUpdate();
            }, 1500);
        } catch (error) {
            console.error('Update failed:', error);
        } finally {
            setIsSaving(false);
        }
    };

    const interactions = [
      { type: 'CALL', date: '2026-03-10', note: 'Discussed Q2 budget allocation for SLV pilot.', author: 'Danny R.' },
      { type: 'EMAIL', date: '2026-03-05', note: 'Sent updated Digital Water Ledger whitepaper.', author: 'System' },
      { type: 'MEETING', date: '2026-02-28', note: 'On-site field visit. Stakeholder expressed interest in Enterprise upgrade.', author: 'Zack C.' }
    ];

    return (
        <Drawer
            isOpen={true}
            onClose={onClose}
            title="Stakeholder Command Suite"
        >
            <div className="flex flex-col gap-8">
                {/* Header Info */}
                <div className="flex items-center gap-4 bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-2xl">
                    <div className="w-14 h-14 bg-emerald-600 rounded-2xl flex items-center justify-center text-2xl font-black text-white shadow-lg shadow-emerald-900/40 shrink-0">
                        {user.email[0].toUpperCase()}
                    </div>
                    <div className="flex-1">
                        <div className="flex items-center justify-between">
                            <h3 className="text-xl font-black text-white tracking-tight">{formData.name || 'Anonymous Stakeholder'}</h3>
                            <span className="text-[10px] font-black text-emerald-400 bg-emerald-400/10 px-2 py-0.5 rounded tracking-widest uppercase">{user.tier}</span>
                        </div>
                        <p className="text-slate-400 text-xs font-mono mt-1">{user.email}</p>
                    </div>
                </div>

                {/* CRM Tabs */}
                <div className="flex gap-1 bg-slate-100 p-1 rounded-xl">
                    {['profile', 'interactions', 'security'].map((tab) => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab as any)}
                            className={`flex-1 py-2 text-xs font-black uppercase tracking-wider rounded-lg transition-all ${
                                activeTab === tab ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
                            }`}
                        >
                            {tab}
                        </button>
                    ))}
                </div>

                <div className="min-h-[400px]">
                    {activeTab === 'profile' && (
                        <div className="grid grid-cols-1 gap-8">
                            <UserEditForm
                                formData={formData}
                                onFormChange={setFormData}
                            />

                            <UserModalSidebar
                                formData={formData}
                                onFormChange={setFormData}
                                user={user}
                                isSaving={isSaving}
                                success={success}
                                onSave={handleSave}
                            />
                        </div>
                    )}

                    {activeTab === 'interactions' && (
                        <div className="space-y-6">
                            <div className="flex items-center justify-between mb-2">
                                <h4 className="text-xs font-black text-slate-400 uppercase tracking-widest">Touchpoint History</h4>
                                <button className="text-[10px] font-black text-emerald-600 uppercase tracking-widest">+ Log Interaction</button>
                            </div>
                            <div className="space-y-4">
                                {interactions.map((i, idx) => (
                                    <div key={idx} className="bg-slate-50 border border-slate-100 p-4 rounded-xl relative group">
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="text-[10px] font-black bg-slate-900 text-white px-2 py-0.5 rounded">
                                                {i.type}
                                            </span>
                                            <span className="text-[10px] text-slate-400 font-bold">{i.date}</span>
                                        </div>
                                        <p className="text-xs text-slate-700 leading-tight mb-2">{i.note}</p>
                                        <div className="text-[9px] text-slate-400 font-black uppercase tracking-widest">
                                            Logged by <span className="text-slate-600">{i.author}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {activeTab === 'security' && (
                        <div className="space-y-8">
                            <div className="bg-rose-50 border border-rose-100 p-6 rounded-2xl">
                                <h4 className="text-xs font-black text-rose-700 uppercase tracking-widest mb-4 flex items-center gap-2">
                                    <div className="w-2 h-2 bg-rose-500 rounded-full animate-pulse" />
                                    Security & Access Credentials
                                </h4>
                                <div className="space-y-4">
                                    <div>
                                        <label className="text-[10px] font-black text-slate-400 uppercase mb-2 block">Master API Key</label>
                                        <div className="flex items-center gap-2">
                                            <input 
                                                type="password" 
                                                value={user.api_key} 
                                                readOnly 
                                                className="flex-1 bg-white border border-slate-200 rounded-xl px-4 py-2 font-mono text-xs" 
                                            />
                                            <button className="text-[10px] font-black text-slate-900 uppercase tracking-widest bg-white border border-slate-200 px-4 py-2 rounded-xl hover:bg-slate-50">Revoke</button>
                                        </div>
                                    </div>
                                    <div>
                                        <label className="text-[10px] font-black text-slate-400 uppercase mb-2 block">Compliance Tier</label>
                                        <select 
                                            value={formData.tier}
                                            onChange={(e) => setFormData({...formData, tier: e.target.value})}
                                            className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3 text-xs font-bold"
                                        >
                                            <option value="FREE">FREE</option>
                                            <option value="STANDARD">STANDARD</option>
                                            <option value="ENTERPRISE">ENTERPRISE</option>
                                            <option value="STATUTORY">STATUTORY</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            
                            <div className="text-[10px] text-slate-400 font-bold leading-tight px-4 italic">
                                Changing the compliance tier may affect the stakeholder's ability to view authenticated kriging worksheets or file supported support letters.
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </Drawer>
    );
};
