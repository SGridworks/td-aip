import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { 
  mockAssets, 
  mockProjects, 
  mockRiskMetrics,
  formatCurrency 
} from '@/data/mockData';
import { 
  Zap, 
  AlertTriangle, 
  DollarSign, 
  TrendingUp,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from 'recharts';

export function Dashboard() {
  const totalAssets = mockAssets.length;
  const criticalAssets = mockAssets.filter(a => a.status === 'critical').length;
  const totalDollarAtRisk = mockAssets.reduce((sum, a) => sum + a.dollarAtRisk, 0);
  const activeProjects = mockProjects.filter(p => p.status === 'in_progress' || p.status === 'approved').length;
  const avgCondition = Math.round(mockAssets.reduce((sum, a) => sum + a.conditionScore, 0) / totalAssets);

  // Asset type distribution
  const assetTypeData = [
    { name: 'Transformers', value: mockAssets.filter(a => a.type === 'transformer').length, color: '#3b82f6' },
    { name: 'Breakers', value: mockAssets.filter(a => a.type === 'breaker').length, color: '#22c55e' },
    { name: 'Lines', value: mockAssets.filter(a => a.type === 'line').length, color: '#f59e0b' },
    { name: 'Switches', value: mockAssets.filter(a => a.type === 'switch').length, color: '#8b5cf6' },
    { name: 'Substations', value: mockAssets.filter(a => a.type === 'substation').length, color: '#ef4444' },
  ];

  // Risk level distribution
  const riskData = [
    { name: 'Critical', value: mockAssets.filter(a => a.failureProbability >= 0.4).length, color: '#ef4444' },
    { name: 'High', value: mockAssets.filter(a => a.failureProbability >= 0.2 && a.failureProbability < 0.4).length, color: '#f97316' },
    { name: 'Medium', value: mockAssets.filter(a => a.failureProbability >= 0.1 && a.failureProbability < 0.2).length, color: '#eab308' },
    { name: 'Low', value: mockAssets.filter(a => a.failureProbability < 0.1).length, color: '#22c55e' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Overview of your T&D asset portfolio and risk exposure
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalAssets}</div>
            <p className="text-xs text-muted-foreground">
              Across 5 asset types
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Assets</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{criticalAssets}</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <ArrowUpRight className="mr-1 h-3 w-3 text-red-500" />
              <span>Requires immediate attention</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Dollar at Risk</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(totalDollarAtRisk)}</div>
            <div className="flex items-center text-xs text-muted-foreground">
              <ArrowDownRight className="mr-1 h-3 w-3 text-green-500" />
              <span>-12% from last quarter</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Projects</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeProjects}</div>
            <p className="text-xs text-muted-foreground">
              {mockProjects.filter(p => p.status === 'proposed').length} pending approval
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>Risk Trend (12 Months)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={mockRiskMetrics}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip 
                    formatter={(value: number, name: string) => {
                      if (name === 'totalDollarAtRisk') return [formatCurrency(value), 'Dollar at Risk'];
                      return [value, name];
                    }}
                  />
                  <Line 
                    yAxisId="left"
                    type="monotone" 
                    dataKey="totalDollarAtRisk" 
                    stroke="#ef4444" 
                    strokeWidth={2}
                    name="Dollar at Risk"
                  />
                  <Line 
                    yAxisId="right"
                    type="monotone" 
                    dataKey="avgConditionScore" 
                    stroke="#3b82f6" 
                    strokeWidth={2}
                    name="Avg Condition Score"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Asset Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={assetTypeData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {assetTypeData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
              {assetTypeData.map((item) => (
                <div key={item.name} className="flex items-center gap-2">
                  <div 
                    className="h-3 w-3 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  />
                  <span>{item.name}: {item.value}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Risk Distribution & Critical Assets */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Risk Level Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={riskData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" name="Asset Count">
                    {riskData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top Risk Assets</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockAssets
                .sort((a, b) => b.dollarAtRisk - a.dollarAtRisk)
                .slice(0, 5)
                .map((asset) => (
                  <div key={asset.id} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className={cn(
                        "h-2 w-2 rounded-full",
                        asset.failureProbability >= 0.4 ? "bg-red-500" :
                        asset.failureProbability >= 0.2 ? "bg-orange-500" :
                        asset.failureProbability >= 0.1 ? "bg-yellow-500" : "bg-green-500"
                      )} />
                      <div>
                        <p className="text-sm font-medium">{asset.name}</p>
                        <p className="text-xs text-muted-foreground">{asset.id}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-semibold">{formatCurrency(asset.dollarAtRisk)}</p>
                      <Badge 
                        variant={asset.status === 'critical' ? 'destructive' : 'secondary'}
                        className="text-xs"
                      >
                        {asset.status}
                      </Badge>
                    </div>
                  </div>
                ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
