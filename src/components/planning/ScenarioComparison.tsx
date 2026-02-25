import { useState } from 'react';
import { 
  mockScenarios, 
  mockProjects,
  formatCurrency 
} from '@/data/mockData';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { 
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { 
  Plus, 
  Copy, 
  Trash2, 
  Check,
  DollarSign,
  TrendingDown,
  TrendingUp,
  Target,
  BarChart3,
  ArrowRight
} from 'lucide-react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  Legend
} from 'recharts';
import { cn } from '@/lib/utils';

export function ScenarioComparison() {
  const [selectedScenarios, setSelectedScenarios] = useState<string[]>(
    mockScenarios.slice(0, 2).map(s => s.id)
  );
  const [isCreateOpen, setIsCreateOpen] = useState(false);

  const scenariosToCompare = mockScenarios.filter(s => 
    selectedScenarios.includes(s.id)
  );

  // Comparison chart data
  const comparisonData = scenariosToCompare.map(s => ({
    name: s.name,
    budget: s.budget / 1000000,
    riskReduction: s.totalRiskReduction / 1000000,
    dollarAtRisk: s.totalDollarAtRisk / 1000000,
    roi: s.roi,
  }));

  // Project count by type for each scenario
  const projectTypeData = ['replacement', 'upgrade', 'maintenance', 'expansion'].map(type => {
    const data: Record<string, number | string> = { type };
    scenariosToCompare.forEach(s => {
      data[s.name] = s.projects.filter(p => p.type === type).length;
    });
    return data;
  });

  const toggleScenario = (id: string) => {
    setSelectedScenarios(prev => 
      prev.includes(id)
        ? prev.filter(s => s !== id)
        : [...prev, id]
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Scenario Comparison</h1>
          <p className="text-muted-foreground">
            Compare different investment scenarios and their impact on risk
          </p>
        </div>
        <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="mr-2 h-4 w-4" />
              New Scenario
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Create New Scenario</DialogTitle>
            </DialogHeader>
            <div className="py-4">
              <p className="text-muted-foreground">
                Scenario creation form would go here. Select projects and set budget constraints.
              </p>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Scenario Selector */}
      <Card>
        <CardHeader>
          <CardTitle>Select Scenarios to Compare</CardTitle>
          <CardDescription>Choose up to 3 scenarios to compare side by side</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            {mockScenarios.map(scenario => (
              <button
                key={scenario.id}
                onClick={() => toggleScenario(scenario.id)}
                className={cn(
                  "flex items-center gap-2 px-4 py-2 rounded-lg border transition-all",
                  selectedScenarios.includes(scenario.id)
                    ? "border-blue-500 bg-blue-50 text-blue-700"
                    : "border-gray-200 hover:border-gray-300"
                )}
              >
                {selectedScenarios.includes(scenario.id) && (
                  <Check className="h-4 w-4" />
                )}
                <span className="font-medium">{scenario.name}</span>
                {scenario.isBaseline && (
                  <Badge variant="outline" className="ml-2">Baseline</Badge>
                )}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Comparison Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        {scenariosToCompare.map(scenario => (
          <Card key={scenario.id} className={cn(
            scenario.isBaseline && "border-blue-200"
          )}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle>{scenario.name}</CardTitle>
                  <CardDescription>{scenario.description}</CardDescription>
                </div>
                {scenario.isBaseline && (
                  <Badge>Baseline</Badge>
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground">Budget</p>
                  <p className="text-xl font-bold">{formatCurrency(scenario.budget)}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Projects</p>
                  <p className="text-xl font-bold">{scenario.projects.length}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Risk Reduction</p>
                  <p className="text-xl font-bold text-green-600">
                    {formatCurrency(scenario.totalRiskReduction)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">ROI</p>
                  <p className="text-xl font-bold">{scenario.roi.toFixed(2)}x</p>
                </div>
              </div>

              <div>
                <p className="text-sm text-muted-foreground mb-1">Budget Utilization</p>
                <Progress 
                  value={(scenario.totalRiskReduction / scenario.budget) * 100} 
                  className="h-2"
                />
                <p className="text-xs text-muted-foreground mt-1">
                  {((scenario.totalRiskReduction / scenario.budget) * 100).toFixed(0)}% of budget returned as risk reduction
                </p>
              </div>

              <div className="flex gap-2 pt-2">
                <Button variant="outline" size="sm" className="flex-1">
                  <Copy className="mr-1 h-3 w-3" />
                  Duplicate
                </Button>
                <Button variant="outline" size="sm" className="flex-1">
                  View Details
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Comparison Charts */}
      {scenariosToCompare.length > 1 && (
        <Tabs defaultValue="metrics" className="space-y-4">
          <TabsList>
            <TabsTrigger value="metrics">Key Metrics</TabsTrigger>
            <TabsTrigger value="projects">Project Mix</TabsTrigger>
            <TabsTrigger value="timeline">Timeline</TabsTrigger>
          </TabsList>

          <TabsContent value="metrics">
            <Card>
              <CardHeader>
                <CardTitle>Budget vs Risk Reduction</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-[350px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={comparisonData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis tickFormatter={(v) => `$${v}M`} />
                      <Tooltip formatter={(v: number) => `$${v}M`} />
                      <Legend />
                      <Bar dataKey="budget" name="Budget ($M)" fill="#3b82f6" />
                      <Bar dataKey="riskReduction" name="Risk Reduction ($M)" fill="#22c55e" />
                      <Bar dataKey="dollarAtRisk" name="Remaining Risk ($M)" fill="#ef4444" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="projects">
            <Card>
              <CardHeader>
                <CardTitle>Project Type Distribution</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-[350px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={projectTypeData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="type" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      {scenariosToCompare.map((scenario, index) => (
                        <Bar 
                          key={scenario.id}
                          dataKey={scenario.name} 
                          name={scenario.name}
                          fill={['#3b82f6', '#22c55e', '#f59e0b'][index % 3]} 
                        />
                      ))}
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="timeline">
            <Card>
              <CardHeader>
                <CardTitle>Implementation Timeline</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {scenariosToCompare.map(scenario => (
                    <div key={scenario.id} className="border rounded-lg p-4">
                      <h4 className="font-semibold mb-3">{scenario.name}</h4>
                      <div className="space-y-2">
                        {scenario.projects.map(project => (
                          <div 
                            key={project.id} 
                            className="flex items-center gap-4 text-sm"
                          >
                            <div className="w-24 font-medium truncate">{project.name}</div>
                            <div className="flex-1 h-6 bg-gray-100 rounded relative">
                              <div 
                                className="absolute h-full bg-blue-500 rounded"
                                style={{
                                  left: '10%',
                                  width: '30%',
                                }}
                              />
                            </div>
                            <div className="w-20 text-right text-muted-foreground">
                              {project.startDate ? new Date(project.startDate).toLocaleDateString() : 'TBD'}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
}
