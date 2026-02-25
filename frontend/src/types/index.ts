// Types for T&D Asset Investment Planning

export type AssetType = 'transformer' | 'breaker' | 'line' | 'switch' | 'substation';
export type AssetStatus = 'operational' | 'degraded' | 'critical' | 'failed' | 'maintenance';
export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

export interface Asset {
  id: string;
  name: string;
  type: AssetType;
  status: AssetStatus;
  location: {
    lat: number;
    lng: number;
    address: string;
  };
  voltage: number; // kV
  capacity: number; // MVA for transformers, MW for lines
  installDate: string;
  lastMaintenance: string;
  conditionScore: number; // 0-100
  healthIndex: number; // 0-100
  failureProbability: number; // 0-1
  dollarAtRisk: number;
  criticality: number; // 1-5
  manufacturer: string;
  model: string;
  serialNumber: string;
  substationId?: string;
  connectedAssets: string[];
}

export interface FailureMode {
  id: string;
  assetId: string;
  name: string;
  description: string;
  probability: number;
  consequence: number;
  riskScore: number;
  mitigationCost: number;
  lastUpdated: string;
}

export interface ConditionHistory {
  id: string;
  assetId: string;
  date: string;
  conditionScore: number;
  healthIndex: number;
  notes: string;
  inspector: string;
  testResults?: Record<string, number>;
}

export interface RiskMetric {
  date: string;
  totalDollarAtRisk: number;
  criticalAssets: number;
  highRiskAssets: number;
  mediumRiskAssets: number;
  lowRiskAssets: number;
  avgConditionScore: number;
}

export type ProjectType = 'replacement' | 'upgrade' | 'maintenance' | 'expansion';
export type ProjectStatus = 'proposed' | 'approved' | 'in_progress' | 'completed' | 'cancelled';

export interface Project {
  id: string;
  name: string;
  description: string;
  type: ProjectType;
  status: ProjectStatus;
  priority: number;
  budget: number;
  actualCost?: number;
  startDate?: string;
  endDate?: string;
  targetAssets: string[];
  riskReduction: number;
  expectedBenefit: number;
  scenarioId?: string;
}

export interface Scenario {
  id: string;
  name: string;
  description: string;
  budget: number;
  projects: Project[];
  totalRiskReduction: number;
  totalDollarAtRisk: number;
  roi: number;
  isBaseline: boolean;
  createdAt: string;
}

export interface OptimizationResult {
  scenarioId: string;
  recommendedProjects: Project[];
  budgetUtilization: number;
  riskReduction: number;
  costBenefitRatio: number;
  constraints: {
    maxBudget: number;
    minRiskReduction: number;
    requiredProjects: string[];
  };
}

export interface NetworkNode {
  id: string;
  type: AssetType;
  position: { x: number; y: number };
  data: Asset;
}

export interface NetworkEdge {
  id: string;
  source: string;
  target: string;
  type: 'electrical' | 'communication' | 'physical';
  capacity?: number;
}

export interface DashboardStats {
  totalAssets: number;
  criticalAssets: number;
  totalDollarAtRisk: number;
  activeProjects: number;
  avgConditionScore: number;
  assetsByType: Record<AssetType, number>;
  riskTrend: RiskMetric[];
}
