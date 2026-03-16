import React from 'react';
import { Phone, Building2, User as UserIcon, CheckCircle, AlertCircle, FileText } from 'lucide-react';
import { Input } from '../../../../components/ui/Input';
import { Button } from '../../../../components/ui/Button';

interface UserEditFormProps {
    formData: {
        name: string;
        organization: string;
        phone: string;
        notes: string;
        is_active: boolean;
    };
    onFormChange: (data: any) => void;
}

export const UserEditForm: React.FC<UserEditFormProps> = ({ formData, onFormChange }) => {
    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                    label="Full Name"
                    value={formData.name}
                    onChange={(e) => onFormChange({ ...formData, name: e.target.value })}
                    placeholder="John Doe"
                />
                <Input
                    label="Organization"
                    value={formData.organization}
                    onChange={(e) => onFormChange({ ...formData, organization: e.target.value })}
                    placeholder="Farm / Entity Name"
                />
                <Input
                    label="Phone Number"
                    value={formData.phone}
                    onChange={(e) => onFormChange({ ...formData, phone: e.target.value })}
                    placeholder="+1 (555) 000-0000"
                />
                <div className="flex flex-col justify-end">
                    <label className="block text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-1.5 ml-1">Account Status</label>
                    <Button
                        variant={formData.is_active ? 'success' : 'danger'}
                        onClick={() => onFormChange({ ...formData, is_active: !formData.is_active })}
                        className="w-full"
                    >
                        {formData.is_active ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                        {formData.is_active ? 'Active Account' : 'Deactivated'}
                    </Button>
                </div>
            </div>

            <div className="space-y-1">
                <label className="block text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-1.5 ml-1">CRM Notes & Internal Briefing</label>
                <div className="relative">
                    <textarea
                        rows={6}
                        value={formData.notes}
                        onChange={(e) => onFormChange({ ...formData, notes: e.target.value })}
                        className="w-full p-4 bg-black/40 border border-slate-800 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none resize-none text-sm text-slate-200"
                        placeholder="Add internal notes about this client's field requirements, grant status, or logistics..."
                    />
                    <FileText className="absolute right-3 bottom-3 w-5 h-5 text-slate-700 pointer-events-none" />
                </div>
            </div>
        </div>
    );
};
