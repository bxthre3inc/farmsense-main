import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './auth/AuthContext';
import { ROLE_HOME } from './auth/types';
import { PrivateRoute, RoleRoute } from './shell/RouteGuards';
import RoleShell from './shell/RoleShell';
import LoginPage from './shell/LoginPage';

// Views — Grant
import GrantReviewerView from './views/grants/GrantReviewerView';

// Admin Views
import AdminView from './views/admin/AdminView';
import UserList from './views/admin/UserList';
import AdminMetrics from './views/admin/AdminMetrics';
import InvestorManagement from './views/admin/InvestorManagement';

// Farmer Views
import FarmerView from './views/farmer/ARFieldVision';

// Research Views
import ResearchView from './views/research/FederatedExperimentConsole';

// Grants Management Views
import GrantDiscovery from './views/grants/GrantDiscovery';
import ApplicationManager from './views/grants/ApplicationManager';
import AwardTracker from './views/grants/AwardTracker';

// Compliance Views
import ComplianceView from './views/compliance/ComplianceDashboard';

// Regulatory Views
import RegulatoryView from './views/regulatory/ComplianceList';
import BasinAnalytics from './views/research/BasinAnalytics';

// Investor Views
import InvestorView from './views/investor/InvestorLanding';

// Docs & Marketing
import DocsView from './views/docs/DocsPlaceholder';
import MarketingView from './views/investor/InvestorLanding';

function RootRedirect() {
  const { isAuthenticated, activeRole } = useAuth();
  if (!isAuthenticated) return <Navigate to="/marketing" replace />;
  if (activeRole) return <Navigate to={ROLE_HOME[activeRole]} replace />;
  return <Navigate to="/login" replace />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public routes — no shell */}
          <Route path="/" element={<RootRedirect />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/marketing" element={<MarketingView />} />
          <Route path="/docs" element={<DocsView />} />

          {/* Protected routes — inside RoleShell */}
          <Route path="/admin/*" element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN']}>
                <RoleShell><AdminView /></RoleShell>
              </RoleRoute>
            </PrivateRoute>
          } />

          <Route path="/grants/review*" element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN', 'GRANT_REVIEWER']}>
                <RoleShell><GrantReviewerView /></RoleShell>
              </RoleRoute>
            </PrivateRoute>
          } />

          <Route path="/grants/*" element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN', 'GRANT_MANAGER']}>
                <RoleShell><ApplicationManager /></RoleShell>
              </RoleRoute>
            </PrivateRoute>
          } />

          <Route path="/farmer/*" element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN', 'FARMER']}>
                <RoleShell><FarmerView /></RoleShell>
              </RoleRoute>
            </PrivateRoute>
          } />

          <Route path="/research/*" element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN', 'RESEARCHER']}>
                <RoleShell><ResearchView /></RoleShell>
              </RoleRoute>
            </PrivateRoute>
          } />

          <Route path="/compliance/*" element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN', 'AUDITOR']}>
                <RoleShell><ComplianceView /></RoleShell>
              </RoleRoute>
            </PrivateRoute>
          } />

          <Route path="/regulatory/*" element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN', 'REGULATOR']}>
                <RoleShell><RegulatoryView /></RoleShell>
              </RoleRoute>
            </PrivateRoute>
          } />

          <Route path="/investor/*" element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN', 'INVESTOR']}>
                <RoleShell><InvestorView /></RoleShell>
              </RoleRoute>
            </PrivateRoute>
          } />

          {/* Catch-all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
