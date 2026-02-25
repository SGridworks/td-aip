import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { mockAssets } from '@/data/mockData';
import { Button } from '@/components/ui/button';
import { 
  ReactFlow, 
  Background, 
  Controls, 
  MiniMap,
  Node,
  Edge,
  useNodesState,
  useEdgesState,
  NodeProps
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { useMemo, useState } from 'react';
import { cn } from '@/lib/utils';
import { AlertTriangle, Activity, Download, Filter } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';

// Custom node component
function AssetNode({ data }: { data: { id: string; name: string; type: string; status: string; failureProbability: number } }) {
  const getRiskColor = () => {
    const fp = data.failureProbability;
    if (fp >= 0.4) return '#ef4444';
    if (fp >= 0.2) return '#f97316';
    if (fp >= 0.1) return '#eab308';
    return '#22c55e';
  };

  const getIcon = () => {
    switch (data.type) {
      case 'transformer': return '⚡';
      case 'breaker': return '⭕';
      case 'line': return '━';
      case 'switch': return '🔌';
      case 'substation': return '🏭';
      default: return '📍';
    }
  };

  return (
    <div 
      className={cn(
        "px-4 py-2 rounded-lg border-2 bg-white shadow-md min-w-[140px]",
        data.status === 'critical' && "border-red-500 ring-2 ring-red-200"
      )}
      style={{ borderColor: data.status === 'critical' ? undefined : getRiskColor() }}
    >
      <div className="flex items-center gap-2">
        <span className="text-xl">{getIcon()}</span>
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-sm truncate">{data.name}</p>
          <p className="text-xs text-gray-500">{data.id}</p>
        </div>
      </div>
      <div className="mt-2 flex items-center gap-2">
        <div 
          className="h-2 w-2 rounded-full"
          style={{ backgroundColor: getRiskColor() }}
        />
        <span className="text-xs text-gray-600">
          {(data.failureProbability * 100).toFixed(0)}% risk
        </span>
      </div>
      {data.status === 'critical' && (
        <div className="mt-1 flex items-center gap-1 text-red-600">
          <AlertTriangle className="h-3 w-3" />
          <span className="text-xs font-medium">Critical</span>
        </div>
      )}
    </div>
  );
}

const nodeTypes = {
  asset: AssetNode,
};

export function RiskNetwork() {
  const [selectedSubstation, setSelectedSubstation] = useState<string | 'all'>('all');
  const [showRiskPropagation, setShowRiskPropagation] = useState(false);

  // Get substations for filter
  const substations = useMemo(() => 
    mockAssets.filter(a => a.type === 'substation'),
    []
  );

  // Filter assets
  const filteredAssets = useMemo(() => {
    if (selectedSubstation === 'all') return mockAssets;
    const substation = mockAssets.find(a => a.id === selectedSubstation);
    if (!substation) return mockAssets;
    return mockAssets.filter(a => 
      a.id === selectedSubstation || 
      a.substationId === selectedSubstation ||
      substation.connectedAssets.includes(a.id)
    );
  }, [selectedSubstation]);

  // Create nodes and edges for React Flow
  const initialNodes: Node[] = useMemo(() => {
    // Simple grid layout
    const nodesPerRow = 4;
    return filteredAssets.map((asset, index) => ({
      id: asset.id,
      type: 'asset',
      position: {
        x: (index % nodesPerRow) * 200 + 50,
        y: Math.floor(index / nodesPerRow) * 150 + 50,
      },
      data: {
        ...asset,
        label: asset.name,
      },
    }));
  }, [filteredAssets]);

  const initialEdges: Edge[] = useMemo(() => {
    const edges: Edge[] = [];
    filteredAssets.forEach(asset => {
      asset.connectedAssets.forEach(connectedId => {
        if (filteredAssets.find(a => a.id === connectedId)) {
          const sourceRisk = asset.failureProbability;
          const isHighRisk = sourceRisk >= 0.3;
          
          edges.push({
            id: `${asset.id}-${connectedId}`,
            source: asset.id,
            target: connectedId,
            animated: isHighRisk && showRiskPropagation,
            style: {
              stroke: isHighRisk ? '#ef4444' : '#94a3b8',
              strokeWidth: isHighRisk ? 3 : 1,
            },
            label: isHighRisk && showRiskPropagation ? 'Risk Propagation' : undefined,
            labelStyle: { fill: '#ef4444', fontSize: 10 },
          });
        }
      });
    });
    return edges;
  }, [filteredAssets, showRiskPropagation]);

  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Network Risk View</h1>
          <p className="text-muted-foreground">
            Visualize asset connectivity and risk propagation through the network
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
              <Filter className="h-4 w-4 text-muted-foreground" />
              <Label>Substation:</Label>
              <Select value={selectedSubstation} onValueChange={setSelectedSubstation}>
                <SelectTrigger className="w-[200px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Substations</SelectItem>
                  {substations.map(sub => (
                    <SelectItem key={sub.id} value={sub.id}>{sub.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="risk-prop"
                checked={showRiskPropagation}
                onChange={(e) => setShowRiskPropagation(e.target.checked)}
                className="rounded border-gray-300"
              />
              <Label htmlFor="risk-prop" className="cursor-pointer">
                Show Risk Propagation
              </Label>
            </div>

            <div className="flex items-center gap-4 ml-auto">
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-red-500" />
                <span className="text-sm">High Risk (&gt;=40%)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-orange-500" />
                <span className="text-sm">Medium Risk (20-39%)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-3 w-3 rounded-full bg-green-500" />
                <span className="text-sm">Low Risk (&lt;20%)</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Network Graph */}
      <Card className="h-[600px]">
        <CardContent className="p-0 h-full">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="bottom-right"
          >
            <Background />
            <Controls />
            <MiniMap 
              nodeStrokeWidth={3}
              zoomable
              pannable
            />
          </ReactFlow>
        </CardContent>
      </Card>

      {/* Risk Propagation Info */}
      {showRiskPropagation && (
        <Card className="border-orange-200 bg-orange-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-800">
              <Activity className="h-5 w-5" />
              Risk Propagation Analysis
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-orange-800">
              Red animated edges indicate potential risk propagation paths where high-risk assets 
              (&gt;=30% failure probability) could impact connected assets. Consider prioritizing 
              mitigation projects at these network junctions.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
