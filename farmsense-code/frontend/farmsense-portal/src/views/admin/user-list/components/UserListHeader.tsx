import React from 'react';
import { Users, RefreshCw, UserPlus } from 'lucide-react';
import { Button } from '../../../../components/ui/Button';

interface UserListHeaderProps {
    loading: boolean;
    onRefresh: () => void;
}

export const UserListHeader: React.FC<UserListHeaderProps> = ({ loading, onRefresh }) => {
    return (
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
            <div>
                <h2 className="text-3xl font-extrabold text-slate-900 flex items-center gap-3">
                    <div className="p-2 bg-indigo-100 rounded-lg text-indigo-600">
                        <Users className="w-8 h-8" />
                    </div>
                    User Relationship Management
                </h2>
                <p className="text-slate-500 mt-2 font-medium">Manage stakeholder access, tiers, and regional coordination.</p>
            </div>

            <div className="flex items-center gap-3">
                <Button
                    variant="outline"
                    onClick={onRefresh}
                    className="group"
                    title="Refresh Synchronized Data"
                >
                    <RefreshCw className={`w-5 h-5 group-hover:rotate-180 transition-transform duration-500 ${loading ? 'animate-spin' : ''}`} />
                    Sync
                </Button>
                <Button variant="primary" className="shadow-lg shadow-indigo-200">
                    <UserPlus className="w-5 h-5" />
                    Add Node User
                </Button>
            </div>
        </div>
    );
};
