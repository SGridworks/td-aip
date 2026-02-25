import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { mockAssets, mockRiskMetrics, formatCurrency } from '@/data/mockData';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  AlertTriangle, 
  TrendingUp, 
  TrendingDown, 
  DollarSign,
  Activity,
  ArrowRight,
  Download
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  Cell
} from 'recharts';
import { cn } from '@/lib/utils';
import { useNavigate } from 'react-router-dom';

export function RiskOverview() {
  const navigate = useNavigate();
  
  const totalDollarAtRisk = mockAssets.reduce((sum, a) => sum + a.dollarAtRisk, 0);
  const criticalAssets = mockAssets.filter(a => a.failureProbability >= 0.4);
  const highRiskAssets = mockAssets.filter(a => a.failureProbability >= 0.2 && a.failureProbability < 0.4);
  const avgCondition = Math.round(mockAssets.reduce((sum, a) => sum + a.conditionScore, 0) / mockAssets.length);

  // Risk trend data with breakdown
  const riskTrendData = mockRiskMetrics.map(m => ({
    ...m,
    criticalValue: m.criticalAssets * 2000000, // Approximate
    highValue: m.highRiskAssets * 1000000,
    mediumValue: m.mediumRiskAssets * 500000,
  }));

  // Top risk assets
  const topRiskAssets = [...mockAssets]
    .sort((a, b) => b.dollarAtRisk - a.dollarAtRisk)
    .slice(0, 10);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Risk Overview</h1>
          <p className="text-muted-foreground">
            Portfolio risk analysis and exposure metrics
          </p>        </div>
        <Button variant="outline">
          <Download className="mr-2 h-4 w-4" />
          Export Report
        </Button>
      </div>

      {/* Risk Summary Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="border-red-200 bg-red-50">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-red-800">Total Dollar at Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-red-700">{formatCurrency(totalDollarAtRisk)}</div>
            <div className="flex items-center mt-2 text-sm text-red-600">
              <TrendingUp className="mr-1 h-4 w-4" />
              <span>+8.5% from last year</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Critical Assets</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-red-600">{criticalAssets.length}</div>
            <p className="text-sm text-muted-foreground">Immediate action required</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">High Risk Assets</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-orange-600">{highRiskAssets.length}</div>
            <p className="text-sm text-muted-foreground">Planning recommended</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Avg Condition Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{avgCondition}</div>
            <div className="flex items-center mt-2 text-sm text-green-600">
              <TrendingDown className="mr-1 h-4 w-4" />
              <span>Improving trend</span>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Risk Trend Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Risk Trend Analysis</CardTitle>
          <CardDescription>Dollar at risk over time by risk category</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[350px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={riskTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis 
                  tickFormatter={(value) => `$${(value / 1000000).toFixed(0)}M`}
                />
                <Tooltip 
                  formatter={(value: number) => [formatCurrency(value), '']}
                />
                <Area
                  type="monotone"
                  dataKey="criticalValue"
                  stackId="1"
                  stroke="#ef4444"
                  fill="#ef4444"
                  name="Critical Risk"
                />
                <Area
                  type="monotone"
                  dataKey="highValue"
                  stackId="1"
                  stroke="#f97316"
                  fill="#f97316"
                  name="High Risk"
                />
                <Area
                  type="monotone"
                  dataKey="mediumValue"
                  stackId="1"
                  stroke="#eab308"
                  fill="#eab308"
                  name="Medium Risk"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Asset Condition Distribution */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Condition Score Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart 
                  data={[
                    { range: '90-100', count: mockAssets.filter(a => a.conditionScore >= 90).length, color: '#22c55e' },
                    { range: '80-89', count: mockAssets.filter(a => a.conditionScore >= 80 && a.conditionScore < 90).length, color: '#84cc16' },
                    { range: '70-79', count: mockAssets.filter(a => a.conditionScore >= 70 && a.conditionScore < 80).length, color: '#eab308' },
                    { range: '60-69', count: mockAssets.filter(a => a.conditionScore >= 60 && a.conditionScore < 70).length, color: '#f97316' },
                    { range: '50-59', count: mockAssets.filter(a => a.conditionScore >= 50 && a.conditionScore < 60).length, color: '#f97316' },
                    { range: '<50', count: mockAssets.filter(a => a.conditionScore < 50).length, color: '#ef4444' },
                  ]}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="range" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" name="Asset Count">
                    {[
                      { range: '90-100', count: mockAssets.filter(a => a.conditionScore >= 90).length, color: '#22c55e' },
                      { range: '80-89', count: mockAssets.filter(a => a.conditionScore >= 80 && a.conditionScore < 90).length, color: '#84cc16' },
                      { range: '70-79', count: mockAssets.filter(a => a.conditionScore >= 70 && a.conditionScore < 80).length, color: '#eab308' },
                      { range: '60-69', count: mockAssets.filter(a => a.conditionScore >= 60 && a.conditionScore < 70).length, color: '#f97316' },
                      { range: '50-59', count: mockAssets.filter(a => a.conditionScore >= 50 && a.conditionScore < 60).length, color: '#f97316' },
                      { range: '<50', count: mockAssets.filter(a => a.conditionScore < 50).length, color: '#ef4444' },
                    ].map((entry, index) => (
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
            <div className="space-y-3">
              {topRiskAssets.map((asset) => (
                <div 
                  key={asset.id} 
                  className="flex items-center justify-between p-3 rounded-lg border hover:bg-muted cursor-pointer"
                  onClick={() => navigate(`/assets/${asset.id}`)}
                >
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      "h-3 w-3 rounded-full",
                      asset.failureProbability >= 0.4 ? "bg-red-500" :
                      asset.failureProbability >= 0.2 ? "bg-orange-500" :
                      asset.failureProbability >= 0.1 ? "bg-yellow-500" : "bg-green-500"
                    )} />
                    <div>
                      <p className="font-medium">{asset.name}</p>
                      <p className="text-sm text-muted-foreground">{asset.id} • {asset.type}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold">{formatCurrency(asset.dollarAtRisk)}</p>
                    <p className="text-xs text-muted-foreground">
                      {(asset.failureProbability * 100).toFixed(0)}% failure prob
                    </p>
                  </div>
                </div>
              ))}
            </div>
            <Button 
              variant="ghost" 
              className="w-full mt-4"
              onClick={() => navigate('/assets')}
            >
              View All Assets
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
