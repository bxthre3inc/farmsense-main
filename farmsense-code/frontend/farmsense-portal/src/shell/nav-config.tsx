import React from 'react';
import {
    LayoutDashboard, Users, BarChart2, Search, FileText,
    Trophy, FlaskConical, BookOpen, ShieldCheck, Settings,
    Globe
} from 'lucide-react';
import type { UserRole } from '../auth/types';

export interface NavItem {
    label: string;
    icon: React.ReactNode;
    path: string;
    roles: UserRole[];
}

export const NAV_ITEMS: NavItem[] = [
    // Admin
    {
        label: 'Dashboard',
        icon: <LayoutDashboard className="w-4 h-4" />,
        path: '/admin',
        roles: ['ADMIN']
    },
    {
        label: 'Users',
        icon: <Users className="w-4 h-4" />,
        path: '/admin/users',
        roles: ['ADMIN']
    },
    {
        label: 'Metrics',
        icon: <BarChart2 className="w-4 h-4" />,
        path: '/admin/metrics',
        roles: ['ADMIN']
    },
    {
        label: 'Settings',
        icon: <Settings className="w-4 h-4" />,
        path: '/admin/settings',
        roles: ['ADMIN']
    },

    // Grant Manager
    {
        label: 'Discover',
        icon: <Search className="w-4 h-4" />,
        path: '/grants',
        roles: ['ADMIN', 'GRANT_MANAGER']
    },
    {
        label: 'Applications',
        icon: <FileText className="w-4 h-4" />,
        path: '/grants/apply',
        roles: ['ADMIN', 'GRANT_MANAGER']
    },
    {
        label: 'Awards',
        icon: <Trophy className="w-4 h-4" />,
        path: '/grants/awards',
        roles: ['ADMIN', 'GRANT_MANAGER']
    },

    // Grant Reviewer
    {
        label: 'Review Queue',
        icon: <BookOpen className="w-4 h-4" />,
        path: '/grants/review',
        roles: ['ADMIN', 'GRANT_REVIEWER']
    },

    // Farmer
    {
        label: 'Field Analytics',
        icon: <LayoutDashboard className="w-4 h-4" />,
        path: '/farmer',
        roles: ['ADMIN', 'FARMER']
    },
    {
        label: 'Irrigation',
        icon: <Globe className="w-4 h-4" />,
        path: '/farmer/irrigation',
        roles: ['ADMIN', 'FARMER']
    },

    // Researcher
    {
        label: 'Experiments',
        icon: <FlaskConical className="w-4 h-4" />,
        path: '/research',
        roles: ['ADMIN', 'RESEARCHER']
    },
    {
        label: 'Open Data',
        icon: <BookOpen className="w-4 h-4" />,
        path: '/research/data',
        roles: ['ADMIN', 'RESEARCHER']
    },

    // Auditor
    {
        label: 'Compliance',
        icon: <ShieldCheck className="w-4 h-4" />,
        path: '/compliance',
        roles: ['ADMIN', 'AUDITOR']
    },
    {
        label: 'GLOBALG.A.P.',
        icon: <ShieldCheck className="w-4 h-4" />,
        path: '/compliance/gap',
        roles: ['ADMIN', 'AUDITOR']
    },

    // Regulator
    {
        label: 'Ledger',
        icon: <ShieldCheck className="w-4 h-4" />,
        path: '/regulatory',
        roles: ['ADMIN', 'REGULATOR']
    },
    {
        label: 'Basin Analytics',
        icon: <BarChart2 className="w-4 h-4" />,
        path: '/regulatory/basin',
        roles: ['ADMIN', 'REGULATOR']
    },
    {
        label: 'SLV Reporting',
        icon: <FileText className="w-4 h-4" />,
        path: '/regulatory/report',
        roles: ['ADMIN', 'REGULATOR']
    },

    // Investor
    {
        label: 'Impact',
        icon: <BarChart2 className="w-4 h-4" />,
        path: '/investor',
        roles: ['ADMIN', 'INVESTOR']
    },
    {
        label: 'Fleet Coverage',
        icon: <Globe className="w-4 h-4" />,
        path: '/investor/fleet',
        roles: ['ADMIN', 'INVESTOR']
    },
];

export const SECTION_LABELS: Partial<Record<UserRole, string>> = {
    ADMIN: 'Administration',
    GRANT_MANAGER: 'Grant Management',
    GRANT_REVIEWER: 'Review Queue',
    FARMER: 'Field Operations',
    RESEARCHER: 'Research Tools',
    AUDITOR: 'Compliance',
    REGULATOR: 'Regulatory Ledger',
    INVESTOR: 'Investor Dashboard',
};
