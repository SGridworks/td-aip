import { AssetType, AssetStatus, RiskLevel, Asset, FailureMode, ConditionHistory, Project, Scenario, RiskMetric } from '@/types';

// Mock Assets
export const mockAssets: Asset[] = [
  {
    id: 'T-001',
    name: 'Main Transformer T1',
    type: 'transformer',
    status: 'operational',
    location: { lat: 40.7128, lng: -74.0060, address: 'Substation A - Bay 1' },
    voltage: 138,
    capacity: 50,
    installDate: '2005-03-15',
    lastMaintenance: '2024-01-20',
    conditionScore: 78,
    healthIndex: 82,
    failureProbability: 0.08,
    dollarAtRisk: 2500000,
    criticality: 5,
    manufacturer: 'ABB',
    model: 'Powerformer 50MVA',
    serialNumber: 'ABB-2005-8842',
    substationId: 'SS-001',
    connectedAssets: ['B-001', 'B-002', 'L-001']
  },
  {
    id: 'T-002',
    name: 'Transformer T2',
    type: 'transformer',
    status: 'degraded',
    location: { lat: 40.7135, lng: -74.0055, address: 'Substation A - Bay 2' },
    voltage: 138,
    capacity: 30,
    installDate: '1998-07-22',
    lastMaintenance: '2023-11-10',
    conditionScore: 62,
    healthIndex: 58,
    failureProbability: 0.22,
    dollarAtRisk: 4200000,
    criticality: 4,
    manufacturer: 'Siemens',
    model: 'GT-30MVA',
    serialNumber: 'SI-1998-4451',
    substationId: 'SS-001',
    connectedAssets: ['B-003', 'L-002']
  },
  {
    id: 'T-003',
    name: 'Distribution Transformer DT1',
    type: 'transformer',
    status: 'critical',
    location: { lat: 40.7140, lng: -74.0070, address: 'Substation B - Bay 1' },
    voltage: 34.5,
    capacity: 10,
    installDate: '1985-11-05',
    lastMaintenance: '2023-06-15',
    conditionScore: 45,
    healthIndex: 42,
    failureProbability: 0.45,
    dollarAtRisk: 6800000,
    criticality: 3,
    manufacturer: 'Westinghouse',
    model: 'W-10MVA-85',
    serialNumber: 'WH-1985-9921',
    substationId: 'SS-002',
    connectedAssets: ['B-004', 'B-005']
  },
  {
    id: 'B-001',
    name: 'Circuit Breaker CB-138-1',
    type: 'breaker',
    status: 'operational',
    location: { lat: 40.7128, lng: -74.0060, address: 'Substation A - 138kV Yard' },
    voltage: 138,
    capacity: 2000,
    installDate: '2010-05-12',
    lastMaintenance: '2024-02-01',
    conditionScore: 88,
    healthIndex: 90,
    failureProbability: 0.03,
    dollarAtRisk: 450000,
    criticality: 5,
    manufacturer: 'GE',
    model: 'GL-314',
    serialNumber: 'GE-2010-2234',
    substationId: 'SS-001',
    connectedAssets: ['T-001', 'L-001']
  },
  {
    id: 'B-002',
    name: 'Circuit Breaker CB-138-2',
    type: 'breaker',
    status: 'operational',
    location: { lat: 40.7128, lng: -74.0060, address: 'Substation A - 138kV Yard' },
    voltage: 138,
    capacity: 2000,
    installDate: '2010-05-12',
    lastMaintenance: '2024-02-01',
    conditionScore: 86,
    healthIndex: 88,
    failureProbability: 0.04,
    dollarAtRisk: 450000,
    criticality: 5,
    manufacturer: 'GE',
    model: 'GL-314',
    serialNumber: 'GE-2010-2235',
    substationId: 'SS-001',
    connectedAssets: ['T-001', 'L-003']
  },
  {
    id: 'B-003',
    name: 'Circuit Breaker CB-138-3',
    type: 'breaker',
    status: 'degraded',
    location: { lat: 40.7135, lng: -74.0055, address: 'Substation A - 138kV Yard' },
    voltage: 138,
    capacity: 1200,
    installDate: '2002-09-18',
    lastMaintenance: '2023-08-20',
    conditionScore: 68,
    healthIndex: 65,
    failureProbability: 0.15,
    dollarAtRisk: 1200000,
    criticality: 4,
    manufacturer: 'ABB',
    model: 'HPL-550TB2',
    serialNumber: 'ABB-2002-7781',
    substationId: 'SS-001',
    connectedAssets: ['T-002', 'L-002']
  },
  {
    id: 'B-004',
    name: 'Breaker 34.5kV B1',
    type: 'breaker',
    status: 'critical',
    location: { lat: 40.7140, lng: -74.0070, address: 'Substation B - 34.5kV Yard' },
    voltage: 34.5,
    capacity: 600,
    installDate: '1995-04-30',
    lastMaintenance: '2023-05-10',
    conditionScore: 42,
    healthIndex: 40,
    failureProbability: 0.38,
    dollarAtRisk: 2100000,
    criticality: 3,
    manufacturer: 'S&C',
    model: 'PMH-9',
    serialNumber: 'SC-1995-1123',
    substationId: 'SS-002',
    connectedAssets: ['T-003', 'L-004']
  },
  {
    id: 'L-001',
    name: 'Transmission Line TL-138-1',
    type: 'line',
    status: 'operational',
    location: { lat: 40.7128, lng: -74.0060, address: 'Substation A to Substation C' },
    voltage: 138,
    capacity: 100,
    installDate: '2005-03-15',
    lastMaintenance: '2023-12-05',
    conditionScore: 75,
    healthIndex: 78,
    failureProbability: 0.10,
    dollarAtRisk: 1800000,
    criticality: 5,
    manufacturer: 'Generic',
    model: 'ACSR 477',
    serialNumber: 'LINE-2005-001',
    substationId: 'SS-001',
    connectedAssets: ['B-001', 'T-001', 'S-001']
  },
  {
    id: 'L-002',
    name: 'Transmission Line TL-138-2',
    type: 'line',
    status: 'degraded',
    location: { lat: 40.7135, lng: -74.0055, address: 'Substation A to Substation D' },
    voltage: 138,
    capacity: 80,
    installDate: '1998-07-22',
    lastMaintenance: '2023-09-15',
    conditionScore: 58,
    healthIndex: 55,
    failureProbability: 0.28,
    dollarAtRisk: 3200000,
    criticality: 4,
    manufacturer: 'Generic',
    model: 'ACSR 336',
    serialNumber: 'LINE-1998-002',
    substationId: 'SS-001',
    connectedAssets: ['B-003', 'T-002']
  },
  {
    id: 'S-001',
    name: 'Disconnect Switch DS-1',
    type: 'switch',
    status: 'operational',
    location: { lat: 40.7128, lng: -74.0060, address: 'Substation A - 138kV Yard' },
    voltage: 138,
    capacity: 2000,
    installDate: '2005-03-15',
    lastMaintenance: '2024-01-15',
    conditionScore: 80,
    healthIndex: 82,
    failureProbability: 0.06,
    dollarAtRisk: 180000,
    criticality: 3,
    manufacturer: 'Southern States',
    model: 'SER-1',
    serialNumber: 'SS-2005-441',
    substationId: 'SS-001',
    connectedAssets: ['L-001']
  },
  {
    id: 'S-002',
    name: 'Load Break Switch LBS-1',
    type: 'switch',
    status: 'maintenance',
    location: { lat: 40.7140, lng: -74.0070, address: 'Substation B - 34.5kV Yard' },
    voltage: 34.5,
    capacity: 600,
    installDate: '2008-02-14',
    lastMaintenance: '2024-02-20',
    conditionScore: 72,
    healthIndex: 75,
    failureProbability: 0.12,
    dollarAtRisk: 350000,
    criticality: 2,
    manufacturer: 'S&C',
    model: 'Omni-Rupter',
    serialNumber: 'SC-2008-882',
    substationId: 'SS-002',
    connectedAssets: ['B-005']
  },
  {
    id: 'SS-001',
    name: 'Substation Alpha',
    type: 'substation',
    status: 'operational',
    location: { lat: 40.7128, lng: -74.0060, address: '1234 Grid Street' },
    voltage: 138,
    capacity: 100,
    installDate: '2005-03-15',
    lastMaintenance: '2024-01-20',
    conditionScore: 82,
    healthIndex: 85,
    failureProbability: 0.05,
    dollarAtRisk: 8500000,
    criticality: 5,
    manufacturer: 'ABB',
    model: 'GIS-138kV',
    serialNumber: 'SS-2005-001',
    connectedAssets: ['T-001', 'T-002', 'B-001', 'B-002', 'B-003']
  },
  {
    id: 'SS-002',
    name: 'Substation Beta',
    type: 'substation',
    status: 'degraded',
    location: { lat: 40.7140, lng: -74.0070, address: '5678 Power Avenue' },
    voltage: 34.5,
    capacity: 30,
    installDate: '1985-11-05',
    lastMaintenance: '2023-06-15',
    conditionScore: 55,
    healthIndex: 52,
    failureProbability: 0.25,
    dollarAtRisk: 9500000,
    criticality: 4,
    manufacturer: 'Westinghouse',
    model: 'AIS-34.5kV',
    serialNumber: 'SS-1985-002',
    connectedAssets: ['T-003', 'B-004', 'S-002']
  }
];

// Mock Failure Modes
export const mockFailureModes: FailureMode[] = [
  {
    id: 'FM-001',
    assetId: 'T-002',
    name: 'Insulation Deterioration',
    description: 'Paper insulation showing signs of aging and moisture ingress',
    probability: 0.35,
    consequence: 4,
    riskScore: 1.4,
    mitigationCost: 450000,
    lastUpdated: '2024-01-15'
  },
  {
    id: 'FM-002',
    assetId: 'T-002',
    name: 'Bushing Failure',
    description: 'Oil-filled bushings showing elevated DGA levels',
    probability: 0.25,
    consequence: 3,
    riskScore: 0.75,
    mitigationCost: 120000,
    lastUpdated: '2024-01-15'
  },
  {
    id: 'FM-003',
    assetId: 'T-003',
    name: 'Tank Integrity',
    description: 'Corrosion on transformer tank, potential oil leak risk',
    probability: 0.55,
    consequence: 3,
    riskScore: 1.65,
    mitigationCost: 85000,
    lastUpdated: '2023-12-10'
  },
  {
    id: 'FM-004',
    assetId: 'T-003',
    name: 'Winding Deformation',
    description: 'FRA test indicates possible winding movement',
    probability: 0.40,
    consequence: 5,
    riskScore: 2.0,
    mitigationCost: 650000,
    lastUpdated: '2023-12-10'
  },
  {
    id: 'FM-005',
    assetId: 'B-003',
    name: 'Mechanical Wear',
    description: 'Operating mechanism showing signs of wear',
    probability: 0.30,
    consequence: 3,
    riskScore: 0.9,
    mitigationCost: 75000,
    lastUpdated: '2023-11-20'
  },
  {
    id: 'FM-006',
    assetId: 'B-004',
    name: 'Contact Erosion',
    description: 'Main contacts showing significant erosion',
    probability: 0.60,
    consequence: 4,
    riskScore: 2.4,
    mitigationCost: 95000,
    lastUpdated: '2023-10-05'
  }
];

// Mock Condition History
export const mockConditionHistory: ConditionHistory[] = [
  { id: 'CH-001', assetId: 'T-002', date: '2024-01-15', conditionScore: 62, healthIndex: 58, notes: 'DGA shows elevated ethylene and methane', inspector: 'J. Smith' },
  { id: 'CH-002', assetId: 'T-002', date: '2023-07-20', conditionScore: 68, healthIndex: 65, notes: 'Oil sample normal, minor paper degradation', inspector: 'J. Smith' },
  { id: 'CH-003', assetId: 'T-002', date: '2023-01-10', conditionScore: 72, healthIndex: 70, notes: 'Routine inspection, all parameters normal', inspector: 'M. Johnson' },
  { id: 'CH-004', assetId: 'T-002', date: '2022-07-15', conditionScore: 75, healthIndex: 74, notes: 'Annual maintenance completed', inspector: 'J. Smith' },
  { id: 'CH-005', assetId: 'T-003', date: '2023-12-10', conditionScore: 45, healthIndex: 42, notes: 'Critical - FRA failure, tank corrosion', inspector: 'R. Williams' },
  { id: 'CH-006', assetId: 'T-003', date: '2023-06-15', conditionScore: 52, healthIndex: 50, notes: 'Condition deteriorating, recommend replacement planning', inspector: 'R. Williams' },
  { id: 'CH-007', assetId: 'T-003', date: '2022-12-05', conditionScore: 58, healthIndex: 56, notes: 'Oil processing performed', inspector: 'M. Johnson' },
  { id: 'CH-008', assetId: 'B-004', date: '2023-10-05', conditionScore: 42, healthIndex: 40, notes: 'Contact resistance high, timing off', inspector: 'A. Davis' },
  { id: 'CH-009', assetId: 'B-004', date: '2023-04-12', conditionScore: 55, healthIndex: 53, notes: 'Minor contact wear noted', inspector: 'A. Davis' }
];

// Mock Projects
export const mockProjects: Project[] = [
  {
    id: 'P-001',
    name: 'T2 Transformer Replacement',
    description: 'Replace aging 30MVA transformer at Substation A',
    type: 'replacement',
    status: 'approved',
    priority: 1,
    budget: 850000,
    startDate: '2024-06-01',
    endDate: '2024-08-15',
    targetAssets: ['T-002'],
    riskReduction: 3800000,
    expectedBenefit: 4200000,
    scenarioId: 'SC-001'
  },
  {
    id: 'P-002',
    name: 'Substation B Breaker Upgrade',
    description: 'Replace critical 34.5kV breaker and associated switchgear',
    type: 'upgrade',
    status: 'proposed',
    priority: 2,
    budget: 320000,
    targetAssets: ['B-004', 'S-002'],
    riskReduction: 2100000,
    expectedBenefit: 2450000,
    scenarioId: 'SC-001'
  },
  {
    id: 'P-003',
    name: 'TL-138-2 Line Rebuild',
    description: 'Rebuild 5-mile section of degraded transmission line',
    type: 'replacement',
    status: 'proposed',
    priority: 3,
    budget: 2800000,
    targetAssets: ['L-002'],
    riskReduction: 2800000,
    expectedBenefit: 3200000,
    scenarioId: 'SC-001'
  },
  {
    id: 'P-004',
    name: 'Substation B Modernization',
    description: 'Complete substation upgrade including transformer replacement',
    type: 'upgrade',
    status: 'proposed',
    priority: 1,
    budget: 4200000,
    targetAssets: ['T-003', 'B-004', 'S-002', 'SS-002'],
    riskReduction: 8500000,
    expectedBenefit: 9500000,
    scenarioId: 'SC-002'
  },
  {
    id: 'P-005',
    name: 'CB-138-3 Maintenance',
    description: 'Major maintenance on 138kV circuit breaker',
    type: 'maintenance',
    status: 'in_progress',
    priority: 4,
    budget: 85000,
    actualCost: 72000,
    startDate: '2024-02-01',
    endDate: '2024-02-28',
    targetAssets: ['B-003'],
    riskReduction: 850000,
    expectedBenefit: 950000,
    scenarioId: 'SC-001'
  }
];

// Mock Scenarios
export const mockScenarios: Scenario[] = [
  {
    id: 'SC-001',
    name: 'Baseline 2024-2025',
    description: 'Standard capital plan with $15M budget',
    budget: 15000000,
    projects: mockProjects.filter(p => p.scenarioId === 'SC-001'),
    totalRiskReduction: 9650000,
    totalDollarAtRisk: 18500000,
    roi: 1.64,
    isBaseline: true,
    createdAt: '2024-01-01'
  },
  {
    id: 'SC-002',
    name: 'Accelerated Replacement',
    description: 'Aggressive replacement program with $25M budget',
    budget: 25000000,
    projects: [mockProjects.find(p => p.id === 'P-004')!],
    totalRiskReduction: 18500000,
    totalDollarAtRisk: 12500000,
    roi: 1.74,
    isBaseline: false,
    createdAt: '2024-01-15'
  },
  {
    id: 'SC-003',
    name: 'Constrained Budget',
    description: 'Reduced capital plan with $8M budget',
    budget: 8000000,
    projects: [mockProjects.find(p => p.id === 'P-001')!],
    totalRiskReduction: 3800000,
    totalDollarAtRisk: 24200000,
    roi: 1.48,
    isBaseline: false,
    createdAt: '2024-01-20'
  }
];

// Mock Risk Metrics (for trend charts)
export const mockRiskMetrics: RiskMetric[] = [
  { date: '2023-01', totalDollarAtRisk: 28500000, criticalAssets: 3, highRiskAssets: 8, mediumRiskAssets: 15, lowRiskAssets: 45, avgConditionScore: 72 },
  { date: '2023-04', totalDollarAtRisk: 29200000, criticalAssets: 4, highRiskAssets: 9, mediumRiskAssets: 14, lowRiskAssets: 44, avgConditionScore: 70 },
  { date: '2023-07', totalDollarAtRisk: 29800000, criticalAssets: 4, highRiskAssets: 10, mediumRiskAssets: 13, lowRiskAssets: 44, avgConditionScore: 69 },
  { date: '2023-10', totalDollarAtRisk: 30500000, criticalAssets: 5, highRiskAssets: 11, mediumRiskAssets: 12, lowRiskAssets: 43, avgConditionScore: 67 },
  { date: '2024-01', totalDollarAtRisk: 31200000, criticalAssets: 5, highRiskAssets: 12, mediumRiskAssets: 11, lowRiskAssets: 43, avgConditionScore: 65 },
  { date: '2024-04', totalDollarAtRisk: 29800000, criticalAssets: 4, highRiskAssets: 10, mediumRiskAssets: 13, lowRiskAssets: 44, avgConditionScore: 68 },
  { date: '2024-07', totalDollarAtRisk: 27500000, criticalAssets: 3, highRiskAssets: 8, mediumRiskAssets: 14, lowRiskAssets: 46, avgConditionScore: 72 },
  { date: '2024-10', totalDollarAtRisk: 25800000, criticalAssets: 2, highRiskAssets: 7, mediumRiskAssets: 15, lowRiskAssets: 47, avgConditionScore: 75 },
];

// Helper functions
export function getAssetsByType(type: AssetType): Asset[] {
  return mockAssets.filter(a => a.type === type);
}

export function getAssetById(id: string): Asset | undefined {
  return mockAssets.find(a => a.id === id);
}

export function getFailureModesByAsset(assetId: string): FailureMode[] {
  return mockFailureModes.filter(fm => fm.assetId === assetId);
}

export function getConditionHistoryByAsset(assetId: string): ConditionHistory[] {
  return mockConditionHistory.filter(ch => ch.assetId === assetId).sort((a, b) => 
    new Date(b.date).getTime() - new Date(a.date).getTime()
  );
}

export function getRiskLevel(asset: Asset): RiskLevel {
  if (asset.failureProbability >= 0.4 || asset.conditionScore < 50) return 'critical';
  if (asset.failureProbability >= 0.2 || asset.conditionScore < 70) return 'high';
  if (asset.failureProbability >= 0.1 || asset.conditionScore < 85) return 'medium';
  return 'low';
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    notation: 'compact',
    maximumFractionDigits: 1
  }).format(value);
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

export const assetTypeLabels: Record<AssetType, string> = {
  transformer: 'Transformer',
  breaker: 'Circuit Breaker',
  line: 'Transmission Line',
  switch: 'Switch',
  substation: 'Substation'
};

export const assetStatusLabels: Record<AssetStatus, string> = {
  operational: 'Operational',
  degraded: 'Degraded',
  critical: 'Critical',
  failed: 'Failed',
  maintenance: 'In Maintenance'
};

export const projectTypeLabels: Record<Project['type'], string> = {
  replacement: 'Replacement',
  upgrade: 'Upgrade',
  maintenance: 'Maintenance',
  expansion: 'Expansion'
};

export const projectStatusLabels: Record<Project['status'], string> = {
  proposed: 'Proposed',
  approved: 'Approved',
  in_progress: 'In Progress',
  completed: 'Completed',
  cancelled: 'Cancelled'
};
