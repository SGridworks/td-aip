import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { mockAssets, formatCurrency } from '@/data/mockData';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { AlertTriangle, Filter, Download, Info } from 'lucide-react';
import { useState, useMemo } from 'react';
import { cn } from '@/lib/utils';
import type { AssetType } from '@/types';

export function RiskHeatmap() {
  const [colorBy, setColorBy] = useState<'dollarAtRisk' | 'conditionScore' | 'failureProbability'>('dollarAtRisk');
  const [typeFilter, setTypeFilter] = useState<AssetType | 'all'>('all');

  const filteredAssets = useMemo(() => {
    return typeFilter === 'all' 
      ? mockAssets 
      : mockAssets.filter(a => a.type === typeFilter);
  }, [typeFilter]);

  const getColor = (asset: typeof mockAssets[0]) => {
    switch (colorBy) {
      case 'dollarAtRisk':
        if (asset.dollarAtRisk >= 5000000) return 'bg-red-600';
        if (asset.dollarAtRisk >= 2000000) return 'bg-orange-500';
        if (asset.dollarAtRisk >= 500000) return 'bg-yellow-500';
        return 'bg-green-500';
      case 'conditionScore':
        if (asset.conditionScore < 50) return 'bg-red-600';
        if (asset.conditionScore < 70) return 'bg-orange-500';
        if (asset.conditionScore < 85) return 'bg-yellow-500';
        return 'bg-green-500';
      case 'failureProbability':
        if (asset.failureProbability >= 0.4) return 'bg-red-600';
        if (asset.failureProbability >= 0.2) return 'bg-orange-500';
        if (asset.failureProbability >= 0.1) return 'bg-yellow-500';
        return 'bg-green-500';
    }
  };

  const getValue = (asset: typeof mockAssets[0]) => {
    switch (colorBy) {
      case 'dollarAtRisk': return formatCurrency(asset.dollarAtRisk);
      case 'conditionScore': return `${asset.conditionScore}/100`;
      case 'failureProbability': return `${(asset.failureProbability * 100).toFixed(1)}%`;
    }
  };

  const getLegend = () => {
    switch (colorBy) {
      case 'dollarAtRisk':
        return [
          { label: '>$5M', color: 'bg-red-600' },
          { label: '$2M-$5M', color: 'bg-orange-500' },
          { label: '$500K-$2M', color: 'bg-yellow-500' },
          { label: '<$500K', color: 'bg-green-500' },
        ];
      case 'conditionScore':
        return [
          { label: '<50 (Critical)', color: 'bg-red-600' },
          { label: '50-69 (Poor)', color: 'bg-orange-500' },
          { label: '70-84 (Fair)', color: 'bg-yellow-500' },
          { label: '85+ (Good)', color: 'bg-green-500' },
        ];
      case 'failureProbability':
        return [
          { label: '>=40% (Critical)', color: 'bg-red-600' },
          { label: '20-39% (High)', color: 'bg-orange-500' },
          { label: '10-19% (Medium)', color: 'bg-yellow-500' },
          { label: '<10% (Low)', color: 'bg-green-500' },
        ];
    }
  };

  // Group assets by type for the heatmap
  const assetsByType = useMemo(() => {
    const groups: Record<string, typeof mockAssets> = {};
    filteredAssets.forEach(asset => {
      if (!groups[asset.type]) groups[asset.type] = [];
      groups[asset.type].push(asset);
    });
    return groups;
  }, [filteredAssets]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Risk Heatmap</h1>
          <p className="text-muted-foreground">
            Visual representation of asset risk across the portfolio
          </p>
        </div>
        <Button variant="outline">
          <Download className="mr-2 h-4 w-4" />
          Export
        </Button>
      </div>

      {/* Controls */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap items-center gap-6">
            <div className="flex items-center gap-2">
              <Label>Color By:</Label>
              <Select value={colorBy} onValueChange={(v) => setColorBy(v as typeof colorBy)}>
                <SelectTrigger className="w-[200px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="dollarAtRisk">Dollar at Risk</SelectItem>
                  <SelectItem value="conditionScore">Condition Score</SelectItem>
                  <SelectItem value="failureProbability">Failure Probability</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4 text-muted-foreground" />
              <Select value={typeFilter} onValueChange={(v) => setTypeFilter(v as AssetType | 'all')}>
                <SelectTrigger className="w-[160px]">
                  <SelectValue placeholder="Asset Type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Types</SelectItem>
                  <SelectItem value="transformer">Transformers</SelectItem>
                  <SelectItem value="breaker">Breakers</SelectItem>
                  <SelectItem value="line">Lines</SelectItem>
                  <SelectItem value="switch">Switches</SelectItem>
                  <SelectItem value="substation">Substations</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center gap-2 ml-auto">
              <Info className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">
                Click on any asset to view details
              </span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Legend */}
      <div className="flex items-center gap-4">
        <span className="text-sm font-medium">Legend:</span>
        <div className="flex gap-3">
          {getLegend().map((item) => (
            <div key={item.label} className="flex items-center gap-2">
              <div className={cn("h-4 w-4 rounded", item.color)} />
              <span className="text-sm">{item.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Heatmap Grid */}
      <TooltipProvider>
        <div className="space-y-6">
          {Object.entries(assetsByType).map(([type, assets]) => (
            <Card key={type}>
              <CardHeader>
                <CardTitle className="capitalize">{type}s ({assets.length})</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                  {assets.map((asset) => (
                    <Tooltip key={asset.id}>
                      <TooltipTrigger asChild>
                        <a 
                          href={`/assets/${asset.id}`}
                          className={cn(
                            "block p-3 rounded-lg text-white transition-all hover:scale-105 hover:shadow-lg",
                            getColor(asset)
                          )}
                        >
                          <div className="text-xs font-medium truncate">{asset.id}</div>
                          <div className="text-lg font-bold">{getValue(asset)}</div>
                          <div className="text-xs opacity-90 truncate">{asset.name}</div>
                        </a>
                      </TooltipTrigger>
                      <TooltipContent>
                        <div className="space-y-1">
                          <p className="font-semibold">{asset.name}</p>
                          <p className="text-xs">ID: {asset.id}</p>
                          <p className="text-xs">Status: {asset.status}</p>
                          <p className="text-xs">Dollar at Risk: {formatCurrency(asset.dollarAtRisk)}</p>
                          <p className="text-xs">Condition: {asset.conditionScore}/100</p>
                        </div>
                      </TooltipContent>
                    </Tooltip>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </TooltipProvider>

      {/* Summary Stats */}
      <Card>
        <CardHeader>
          <CardTitle>Heatmap Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 rounded-lg bg-red-50">
              <AlertTriangle className="mx-auto h-6 w-6 text-red-600 mb-2" />
              <p className="text-2xl font-bold text-red-600">
                {filteredAssets.filter(a => {
                  if (colorBy === 'dollarAtRisk') return a.dollarAtRisk >= 5000000;
                  if (colorBy === 'conditionScore') return a.conditionScore < 50;
                  return a.failureProbability >= 0.4;
                }).length}
              </p>
              <p className="text-sm text-red-700">Critical</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-orange-50">
              <p className="text-2xl font-bold text-orange-600">
                {filteredAssets.filter(a => {
                  if (colorBy === 'dollarAtRisk') return a.dollarAtRisk >= 2000000 && a.dollarAtRisk < 5000000;
                  if (colorBy === 'conditionScore') return a.conditionScore >= 50 && a.conditionScore < 70;
                  return a.failureProbability >= 0.2 && a.failureProbability < 0.4;
                }).length}
              </p>
              <p className="text-sm text-orange-700">High Risk</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-yellow-50">
              <p className="text-2xl font-bold text-yellow-600">
                {filteredAssets.filter(a => {
                  if (colorBy === 'dollarAtRisk') return a.dollarAtRisk >= 500000 && a.dollarAtRisk < 2000000;
                  if (colorBy === 'conditionScore') return a.conditionScore >= 70 && a.conditionScore < 85;
                  return a.failureProbability >= 0.1 && a.failureProbability < 0.2;
                }).length}
              </p>
              <p className="text-sm text-yellow-700">Medium Risk</p>
            </div>
            <div className="text-center p-4 rounded-lg bg-green-50">
              <p className="text-2xl font-bold text-green-600">
                {filteredAssets.filter(a => {
                  if (colorBy === 'dollarAtRisk') return a.dollarAtRisk < 500000;
                  if (colorBy === 'conditionScore') return a.conditionScore >= 85;
                  return a.failureProbability < 0.1;
                }).length}
              </p>
              <p className="text-sm text-green-700">Low Risk</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
