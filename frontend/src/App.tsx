import { Routes, Route, Navigate } from 'react-router-dom';
import { Sidebar } from '@/components/layout/Sidebar';
import { Dashboard } from '@/components/dashboard/Dashboard';
import { AssetList } from '@/components/assets/AssetList';
import { AssetDetail } from '@/components/assets/AssetDetail';
import { AssetMap } from '@/components/assets/AssetMap';
import { RiskOverview } from '@/components/risk/RiskOverview';
import { RiskHeatmap } from '@/components/risk/RiskHeatmap';
import { RiskNetwork } from '@/components/risk/RiskNetwork';
import { ProjectList } from '@/components/planning/ProjectList';
import { ScenarioComparison } from '@/components/planning/ScenarioComparison';
import { OptimizationResults } from '@/components/planning/OptimizationResults';

function App() {
  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <main className="lg:pl-64">
        <div className="container mx-auto p-6">
          <Routes>
            {/* Dashboard */}
            <Route path="/" element={<Dashboard />} />

            {/* Assets */}
            <Route path="/assets" element={<AssetList />} />
            <Route path="/assets/map" element={<AssetMap />} />
            <Route path="/assets/:id" element={<AssetDetail />} />

            {/* Risk */}
            <Route path="/risk" element={<RiskOverview />} />
            <Route path="/risk/heatmap" element={<RiskHeatmap />} />
            <Route path="/risk/network" element={<RiskNetwork />} />

            {/* Planning */}
            <Route path="/planning" element={<ProjectList />} />
            <Route path="/planning/scenarios" element={<ScenarioComparison />} />
            <Route path="/planning/optimization" element={<OptimizationResults />} />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
}

export default App;
