import { useParams, useNavigate } from 'react-router-dom';
import { 
  mockAssets, 
  mockFailureModes, 
  mockConditionHistory,
  mockProjects,
  assetTypeLabels,
  assetStatusLabels,
  formatCurrency,
  formatDate,
  getRiskLevel,
  getFailureModesByAsset,
  getConditionHistoryByAsset
} from '@/data/mockData';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';
import { 
  ArrowLeft, 
  MapPin, 
  Calendar, 
  Wrench, 
  AlertTriangle,
  TrendingDown,
  FileText,
  Zap,
  Activity,
  DollarSign,
  Link as LinkIcon
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { cn } from '@/lib/utils';

export function AssetDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const asset = mockAssets.find(a => a.id === id);
  const failureModes = asset ? getFailureModesByAsset(asset.id) : [];
  const conditionHistory = asset ? getConditionHistoryByAsset(asset.id) : [];
  const relatedProjects = mockProjects.filter(p => p.targetAssets.includes(id || ''));

  if (!asset) {
    return (
      <div className="flex h-[50vh] items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold">Asset Not Found</h2>
          <p className="text-muted-foreground">The asset you're looking for doesn't exist.</p>
          <Button className="mt-4" onClick={() => navigate('/assets')}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Assets
          </Button>
        </div>
      </div>
    );
  }

  const riskLevel = getRiskLevel(asset);
  const riskColor = {
    low: 'text-green-600 bg-green-50',
    medium: 'text-yellow-600 bg-yellow-50',
    high: 'text-orange-600 bg-orange-50',
    critical: 'text-red-600 bg-red-50'
  }[riskLevel];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <Button variant="ghost" size="sm" onClick={() => navigate('/assets')} className="mb-2">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Assets
          </Button>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold">{asset.name}</h1>
            <Badge variant="outline" className={riskColor}>
              {riskLevel.toUpperCase()} RISK
            </Badge>
          </div>
          <p className="text-muted-foreground">
            {asset.id} • {assetTypeLabels[asset.type]} • {asset.manufacturer} {asset.model}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">
            <FileText className="mr-2 h-4 w-4" />
            Reports
          </Button>
          <Button>
            <Wrench className="mr-2 h-4 w-4" />
            Schedule Maintenance
          </Button>
        </div>
      </div>

      {/* Alerts */}
      {asset.status === 'critical' && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Critical Asset Condition</AlertTitle>
          <AlertDescription>
            This asset is in critical condition with a {Math.round(asset.failureProbability * 100)}% failure probability. 
            Immediate action recommended.
          </AlertDescription>
        </Alert>
      )}

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Condition Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{asset.conditionScore}/100</div>
            <Progress value={asset.conditionScore} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Health Index</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{asset.healthIndex}/100</div>
            <Progress value={asset.healthIndex} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Failure Probability</CardTitle>
          </CardHeader>
          <CardContent>
            <div className={cn(
              "text-2xl font-bold",
              asset.failureProbability > 0.3 ? "text-red-600" :
              asset.failureProbability > 0.15 ? "text-orange-600" : "text-green-600"
            )}>
              {(asset.failureProbability * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-muted-foreground">Next 12 months</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Dollar at Risk</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(asset.dollarAtRisk)}</div>
            <p className="text-xs text-muted-foreground">Criticality: {asset.criticality}/5</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="failure-modes">Failure Modes ({failureModes.length})</TabsTrigger>
          <TabsTrigger value="condition-history">Condition History</TabsTrigger>
          <TabsTrigger value="projects">Projects ({relatedProjects.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Asset Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Asset Type</p>
                    <p className="font-medium">{assetTypeLabels[asset.type]}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Status</p>
                    <Badge variant={asset.status === 'critical' ? 'destructive' : 'secondary'}>
                      {assetStatusLabels[asset.status]}
                    </Badge>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Voltage Class</p>
                    <p className="font-medium">{asset.voltage} kV</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Capacity</p>
                    <p className="font-medium">{asset.capacity} {asset.type === 'transformer' ? 'MVA' : 'MW'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Manufacturer</p>
                    <p className="font-medium">{asset.manufacturer}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Model</p>
                    <p className="font-medium">{asset.model}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Serial Number</p>
                    <p className="font-medium">{asset.serialNumber}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Install Date</p>
                    <p className="font-medium">{formatDate(asset.installDate)}</p>
                  </div>
                </div>
                <Separator />
                <div>
                  <p className="text-sm text-muted-foreground">Location</p>
                  <div className="flex items-center gap-2 mt-1">
                    <MapPin className="h-4 w-4 text-muted-foreground" />
                    <p className="font-medium">{asset.location.address}</p>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">
                    Lat: {asset.location.lat}, Lng: {asset.location.lng}
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Connected Assets</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {asset.connectedAssets.map(connectedId => {
                    const connectedAsset = mockAssets.find(a => a.id === connectedId);
                    if (!connectedAsset) return null;
                    return (
                      <div 
                        key={connectedId}
                        className="flex items-center justify-between p-3 rounded-lg border hover:bg-muted cursor-pointer"
                        onClick={() => navigate(`/assets/${connectedId}`)}
                      >
                        <div className="flex items-center gap-3">
                          <LinkIcon className="h-4 w-4 text-muted-foreground" />
                          <div>
                            <p className="font-medium">{connectedAsset.name}</p>
                            <p className="text-sm text-muted-foreground">{connectedId}</p>
                          </div>
                        </div>
                        <Badge variant="outline">{assetTypeLabels[connectedAsset.type]}</Badge>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="failure-modes">
          <div className="space-y-4">
            {failureModes.length === 0 ? (
              <Card>
                <CardContent className="py-8 text-center">
                  <Activity className="mx-auto h-12 w-12 text-muted-foreground" />
                  <p className="mt-4 text-muted-foreground">No failure modes identified for this asset.</p>
                </CardContent>
              </Card>
            ) : (
              failureModes.map((fm) => (
                <Card key={fm.id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle>{fm.name}</CardTitle>
                        <CardDescription>{fm.description}</CardDescription>
                      </div>
                      <Badge variant={fm.riskScore > 1.5 ? 'destructive' : fm.riskScore > 0.8 ? 'warning' : 'secondary'}>
                        Risk Score: {fm.riskScore.toFixed(2)}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <p className="text-sm text-muted-foreground">Probability</p>
                        <p className="text-lg font-semibold">{(fm.probability * 100).toFixed(0)}%</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Consequence</p>
                        <p className="text-lg font-semibold">{fm.consequence}/5</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Mitigation Cost</p>
                        <p className="text-lg font-semibold">{formatCurrency(fm.mitigationCost)}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>

        <TabsContent value="condition-history">
          <Card>
            <CardHeader>
              <CardTitle>Condition Score Trend</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={[...conditionHistory].reverse()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <ReferenceLine y={50} stroke="red" strokeDasharray="3 3" label="Critical" />
                    <ReferenceLine y={70} stroke="orange" strokeDasharray="3 3" label="Warning" />
                    <Line 
                      type="monotone" 
                      dataKey="conditionScore" 
                      stroke="#3b82f6" 
                      strokeWidth={2}
                      name="Condition Score"
                      dot={{ fill: '#3b82f6' }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="healthIndex" 
                      stroke="#22c55e" 
                      strokeWidth={2}
                      name="Health Index"
                      dot={{ fill: '#22c55e' }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <div className="mt-6 space-y-4">
            <h3 className="text-lg font-semibold">Inspection History</h3>
            {conditionHistory.map((record, index) => (
              <Card key={record.id}>
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-4">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
                        <Calendar className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <p className="font-medium">{formatDate(record.date)}</p>
                        <p className="text-sm text-muted-foreground">Inspector: {record.inspector}</p>
                        <p className="mt-2 text-sm">{record.notes}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="flex items-center gap-4">
                        <div>
                          <p className="text-xs text-muted-foreground">Condition</p>
                          <p className="text-lg font-semibold">{record.conditionScore}</p>
                        </div>
                        <div>
                          <p className="text-xs text-muted-foreground">Health</p>
                          <p className="text-lg font-semibold">{record.healthIndex}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="projects">
          <div className="space-y-4">
            {relatedProjects.length === 0 ? (
              <Card>
                <CardContent className="py-8 text-center">
                  <Zap className="mx-auto h-12 w-12 text-muted-foreground" />
                  <p className="mt-4 text-muted-foreground">No projects associated with this asset.</p>
                  <Button className="mt-4">Create Project</Button>
                </CardContent>
              </Card>
            ) : (
              relatedProjects.map((project) => (
                <Card key={project.id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle>{project.name}</CardTitle>
                        <CardDescription>{project.description}</CardDescription>
                      </div>
                      <Badge variant={project.status === 'approved' ? 'success' : project.status === 'in_progress' ? 'default' : 'secondary'}>
                        {project.status.replace('_', ' ')}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-4 gap-4">
                      <div>
                        <p className="text-sm text-muted-foreground">Budget</p>
                        <p className="font-semibold">{formatCurrency(project.budget)}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Risk Reduction</p>
                        <p className="font-semibold text-green-600">{formatCurrency(project.riskReduction)}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Expected Benefit</p>
                        <p className="font-semibold">{formatCurrency(project.expectedBenefit)}</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Priority</p>
                        <p className="font-semibold">#{project.priority}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
