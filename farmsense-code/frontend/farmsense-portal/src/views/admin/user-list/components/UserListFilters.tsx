import React from 'react';
import { Search, Filter } from 'lucide-react';
import { Input } from '../../../../components/ui/Input';
import { Card } from '../../../../components/ui/Card';

interface UserListFiltersProps {
    searchQuery: string;
    setSearchQuery: (query: string) => void;
    roleFilter: string;
    setRoleFilter: (role: string) => void;
    foundCount: number;
}

export const UserListFilters: React.FC<UserListFiltersProps> = ({
    searchQuery,
    setSearchQuery,
    roleFilter,
    setRoleFilter,
    foundCount
}) => {
    return (
        <Card className="mb-6 flex flex-col md:flex-row gap-4 items-center">
            <div className="relative flex-1 w-full">
                <Search className="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
                <input
                    type="text"
                    placeholder="Search by email, name, or organization..."
                    className="w-full pl-12 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </div>

            <div className="flex items-center gap-2 w-full md:w-auto">
                <Filter className="w-5 h-5 text-slate-400 ml-2" />
                <select
                    className="bg-slate-50 border border-slate-200 text-slate-700 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-indigo-500 font-bold text-sm min-w-[140px]"
                    value={roleFilter}
                    onChange={(e) => setRoleFilter(e.target.value)}
                >
                    <option value="ALL">All Roles</option>
                    <option value="ADMIN">Administrators</option>
                    <option value="FARMER">Farmers</option>
                    <option value="RESEARCHER">Researchers</option>
                    <option value="INVESTOR">Investors</option>
                    <option value="AUDITOR">Auditors</option>
                </select>
            </div>

            <div className="text-sm font-bold text-slate-400 px-4 border-l border-slate-100 hidden md:block whitespace-nowrap">
                {foundCount} Users Found
            </div>
        </Card>
    );
};
