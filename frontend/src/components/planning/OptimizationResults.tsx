import { useState } from 'react';
import { 
  mockScenarios, 
  mockAssets,
  mockProjects,
  formatCurrency 
} from '@/data/mockData';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { 
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { 
  Play, 
  RotateCcw, 
  Save, 
  TrendingUp,
  DollarSign,
  Target,
  AlertTriangle,
  CheckCircle2,
  Lightbulb,
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
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { cn } from '@/lib/utils';

export function OptimizationResults() {
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [budgetConstraint, setBudgetConstraint] = useState(15000000);
  const [minRiskReduction, setMinRiskReduction] = useState(5000000);
  const [requiredProjects, setRequiredProjects] = useState<string[]>([]);

  // Simulate optimization
  const runOptimization = () => {
    setIsOptimizing(true);
    setTimeout(() => {
      setIsOptimizing(false);
      setShowResults(true);
    }, 2000);
  };

  // Mock optimized results
  const optimizedProjects = mockProjects
    .filter(p => p.status === 'proposed')
    .sort((a, b) => (b.riskReduction / b.budget) - (a.riskReduction / a.budget))
    .slice(0, 4);

  const totalOptimizedBudget = optimizedProjects.reduce((sum, p) => sum + p.budget, 0);
  const totalOptimizedRiskReduction = optimizedProjects.reduce((sum, p) => sum + p.riskReduction, 0);
  const optimizedROI = totalOptimizedRiskReduction / totalOptimizedBudget;

  const budgetUtilization = (totalOptimizedBudget / budgetConstraint) * 100;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Optimization Engine</h1>
        <p className="text-muted-foreground">
          AI-powered project selection to maximize risk reduction within budget constraints
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Constraints Panel */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Optimization Constraints</CardTitle>
            <CardDescription>Set your planning parameters</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div>
                <div className="flex justify-between mb-2">
                  <Label>Budget Constraint</Label>
                  <span className="font-semibold">{formatCurrency(budgetConstraint)}</span>
                </div>
                <Slider
                  value={[budgetConstraint]}
                  onValueChange={([v]) => setBudgetConstraint(v)}
                  min={5000000}
                  max={50000000}
                  step={1000000}
                />
                <div className="flex justify-between text-xs text-muted-foreground mt-1">
                  <span>$5M</span>
                  <span>$50M</span>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <Label>Min Risk Reduction</Label>
                  <span className="font-semibold">{formatCurrency(minRiskReduction)}</span>
                </div>
                <Slider
                  value={[minRiskReduction]}
                  onValueChange={([v]) => setMinRiskReduction(v)}
                  min={0}
                  max={20000000}
                  step={500000}
                />
              </div>
            </div>

            <div>
              <Label className="mb-2 block">Required Projects</Label>
              <div className="space-y-2 max-h-[200px] overflow-y-auto">
                {mockProjects.filter(p => p.status === 'proposed').map(project => (
                  <div key={project.id} className="flex items-center space-x-2">
                    <Checkbox
                      id={project.id}
                      checked={requiredProjects.includes(project.id)}
                      onCheckedChange={(checked) => {
                        setRequiredProjects(prev => 
                          checked 
                            ? [...prev, project.id]
                            : prev.filter(id => id !== project.id)
                        );
                      }}
                    />
                    <label 
                      htmlFor={project.id}
                      className="text-sm cursor-pointer"
                    >
                      {project.name}
                    </label>
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-4 space-y-2">
              <Button 
                className="w-full" 
                onClick={runOptimization}
                disabled={isOptimizing}
              >
                {isOptimizing ? (
                  <>
                    <RotateCcw className="mr-2 h-4 w-4 animate-spin" />
                    Optimizing...
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4" />
                    Run Optimization
                  </>
                )}
              </Button>
              
              {showResults && (
                <Button variant="outline" className="w-full">
                  <Save className="mr-2 h-4 w-4" />
                  Save as Scenario
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Results Panel */}
        <div className="lg:col-span-2 space-y-6">
          {!showResults ? (
            <Card className="h-full flex items-center justify-center">
              <CardContent className="text-center py-12">
                <Lightbulb className="mx-auto h-16 w-16 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">Ready to Optimize</h3>
                <p className="text-muted-foreground max-w-md">
                  Set your constraints and click "Run Optimization" to generate an 
                  optimal project portfolio that maximizes risk reduction within your budget.
                </p>
              </CardContent>
            </Card>
          ) : (
            <>
              {/* Summary Cards */}
              <div className="grid gap-4 md:grid-cols-3">
                <Card className="bg-green-50 border-green-200">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm text-green-800">Optimized Budget</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-green-700">
                      {formatCurrency(totalOptimizedBudget)}
                    </div>
                    <div className="mt-2">
                      <Progress value={budgetUtilization} className="h-2" />
                      <p className="text-xs text-green-600 mt-1">
                        {budgetUtilization.toFixed(1)}% of budget used
                      </p>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-blue-50 border-blue-200">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm text-blue-800">Risk Reduction</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-blue-700">
                      {formatCurrency(totalOptimizedRiskReduction)}
                    </div>
                    <div className="flex items-center mt-2 text-blue-600">
                      <TrendingUp className="h-4 w-4 mr-1" />
                      <span className="text-sm">
                        {(totalOptimizedRiskReduction / totalOptimizedBudget).toFixed(2)}x return
                      </span>
                    </div>
                  </CardContent>
                </Card>

                <Card className="bg-purple-50 border-purple-200">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm text-purple-800">Projects Selected</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-purple-700">
                      {optimizedProjects.length}
                    </div>
                    <p className="text-sm text-purple-600 mt-2">
                      of {mockProjects.filter(p => p.status === 'proposed').length} proposed
                    </p>
                  </CardContent>
                </Card>
              </div>

              {/* Recommended Projects */}
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>Recommended Project Portfolio</CardTitle>
                      <CardDescription>
                        AI-selected projects for optimal risk reduction
                      </CardDescription>
                    </div>
                    <Badge variant="success" className="bg-green-100 text-green-800">
                      <CheckCircle2 className="h-3 w-3 mr-1" />
                      Optimal
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {optimizedProjects.map((project, index) => (
                      <div 
                        key={project.id}
                        className="flex items-center justify-between p-4 rounded-lg border hover:bg-muted"
                      >
                        <div className="flex items-center gap-4">
                          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-700 font-bold">
                            {index + 1}
                          </div>
                          <div>
                            <p className="font-medium">{project.name}</p>
                            <p className="text-sm text-muted-foreground">{project.description}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-6">
                          <div className="text-right">
                            <p className="text-sm text-muted-foreground">Budget</p>
                            <p className="font-semibold">{formatCurrency(project.budget)}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-muted-foreground">Risk Reduction</p>
                            <p className="font-semibold text-green-600">
                              {formatCurrency(project.riskReduction)}
                            </p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-muted-foreground">ROI</p>
                            <p className="font-semibold">
                              {(project.riskReduction / project.budget).toFixed(2)}x
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Charts */}
              <div className="grid gap-4 md:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle>Budget Allocation</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-[250px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={optimizedProjects.map(p => ({
                              name: p.name,
                              value: p.budget
                            }))}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={80}
                            paddingAngle={5}
                            dataKey="value"
                          >
                            {optimizedProjects.map((_, index) => (
                              <Cell key={`cell-${index}`} fill={[
                                '#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6'
                              ][index % 5]} />
                            ))}
                          </Pie>
                          <Tooltip formatter={(v: number) => formatCurrency(v)} />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Cost-Benefit Analysis</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-[250px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart 
                          data={optimizedProjects.map(p => ({
                            name: p.name.split(' ').slice(0, 2).join(' '),
                            budget: p.budget / 1000000,
                            riskReduction: p.riskReduction / 1000000,
                          }))}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" tick={{ fontSize: 10 }} />
                          <YAxis tickFormatter={(v) => `$${v}M`} />
                          <Tooltip formatter={(v: number) => `$${v}M`} />
                          <Bar dataKey="budget" name="Budget" fill="#3b82f6" />
                          <Bar dataKey="riskReduction" name="Risk Reduction" fill="#22c55e" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
