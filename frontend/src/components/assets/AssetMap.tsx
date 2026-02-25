import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { mockAssets, formatCurrency } from '@/data/mockData';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { MapPin, ZoomIn, ZoomOut, Layers, Filter } from 'lucide-react';
import { useState, useMemo } from 'react';
import { cn } from '@/lib/utils';

// Simple SVG-based map visualization
export function AssetMap() {
  const [zoom, setZoom] = useState(1);
  const [selectedType, setSelectedType] = useState<string | 'all'>('all');
  const [selectedAsset, setSelectedAsset] = useState<typeof mockAssets[0] | null>(null);

  // Calculate map bounds from asset locations
  const bounds = useMemo(() => {
    const lats = mockAssets.map(a => a.location.lat);
    const lngs = mockAssets.map(a => a.location.lng);
    return {
      minLat: Math.min(...lats) - 0.01,
      maxLat: Math.max(...lats) + 0.01,
      minLng: Math.min(...lngs) - 0.01,
      maxLng: Math.max(...lngs) + 0.01,
    };
  }, []);

  // Convert lat/lng to SVG coordinates
  const toSvgCoords = (lat: number, lng: number) => {
    const x = ((lng - bounds.minLng) / (bounds.maxLng - bounds.minLng)) * 800;
    const y = 600 - ((lat - bounds.minLat) / (bounds.maxLat - bounds.minLat)) * 600;
    return { x, y };
  };

  const filteredAssets = useMemo(() => {
    return selectedType === 'all' 
      ? mockAssets 
      : mockAssets.filter(a => a.type === selectedType);
  }, [selectedType]);

  const getAssetColor = (asset: typeof mockAssets[0]) => {
    if (asset.failureProbability >= 0.4) return '#ef4444';
    if (asset.failureProbability >= 0.2) return '#f97316';
    if (asset.failureProbability >= 0.1) return '#eab308';
    return '#22c55e';
  };

  const getAssetIcon = (type: string) => {
    switch (type) {
      case 'transformer': return '⚡';
      case 'breaker': return '⭕';
      case 'line': return '━';
      case 'switch': return '🔌';
      case 'substation': return '🏭';
      default: return '📍';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Asset Map</h1>
          <p className="text-muted-foreground">
            Geographic view of T&D assets and network connectivity
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => setZoom(z => Math.min(2, z + 0.2))}>
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={() => setZoom(z => Math.max(0.5, z - 0.2))}>
            <ZoomOut className="h-4 w-4" />
          </Button>
        </div>      </div>

      {/* Filter Bar */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center gap-4">
            <Filter className="h-4 w-4 text-muted-foreground" />
            <div className="flex gap-2">
              {['all', 'transformer', 'breaker', 'line', 'switch', 'substation'].map((type) => (
                <Button
                  key={type}
                  variant={selectedType === type ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedType(type)}
                >
                  {type === 'all' ? 'All Types' : type.charAt(0).toUpperCase() + type.slice(1) + 's'}
                </Button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 lg:grid-cols-4">
        {/* Map */}
        <Card className="lg:col-span-3">
          <CardContent className="p-0">
            <div className="relative overflow-hidden rounded-lg bg-slate-100"
            >
              <svg
                viewBox="0 0 800 600"
                className="w-full h-[600px]"
                style={{ transform: `scale(${zoom})`, transformOrigin: 'center' }}
              >
                {/* Background grid */}
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#e2e8f0" strokeWidth="1"/>
                </pattern>
                <rect width="800" height="600" fill="url(#grid)" />

                {/* Connection lines */}
                {filteredAssets.map(asset => 
                  asset.connectedAssets.map(connectedId => {
                    const connected = mockAssets.find(a => a.id === connectedId);
                    if (!connected) return null;
                    const start = toSvgCoords(asset.location.lat, asset.location.lng);
                    const end = toSvgCoords(connected.location.lat, connected.location.lng);
                    return (
                      <line
                        key={`${asset.id}-${connectedId}`}
                        x1={start.x}
                        y1={start.y}
                        x2={end.x}
                        y2={end.y}
                        stroke="#94a3b8"
                        strokeWidth="2"
                        strokeDasharray="5,5"
                      />
                    );
                  })
                )}

                {/* Assets */}
                {filteredAssets.map(asset => {
                  const coords = toSvgCoords(asset.location.lat, asset.location.lng);
                  const isSelected = selectedAsset?.id === asset.id;
                  return (
                    <g
                      key={asset.id}
                      transform={`translate(${coords.x}, ${coords.y})`}
                      className="cursor-pointer"
                      onClick={() => setSelectedAsset(asset)}
                    >
                      <circle
                        r={isSelected ? 20 : 12}
                        fill={getAssetColor(asset)}
                        stroke={isSelected ? '#1e293b' : 'white'}
                        strokeWidth={isSelected ? 3 : 2}
                        className="transition-all duration-200"
                      />
                      <text
                        y={-18}
                        textAnchor="middle"
                        className="text-xs font-medium fill-slate-700"
                        style={{ fontSize: '11px' }}
                      >
                        {asset.id}
                      </text>
                    </g>
                  );
                })}
              </svg>

              {/* Legend */}
              <div className="absolute bottom-4 left-4 rounded-lg bg-white p-3 shadow-lg">
                <p className="text-xs font-semibold mb-2">Risk Level</p>
                <div className="space-y-1">
                  {[
                    { label: 'Critical', color: '#ef4444' },
                    { label: 'High', color: '#f97316' },
                    { label: 'Medium', color: '#eab308' },
                    { label: 'Low', color: '#22c55e' },
                  ].map(item => (
                    <div key={item.label} className="flex items-center gap-2">
                      <div 
                        className="h-3 w-3 rounded-full" 
                        style={{ backgroundColor: item.color }}
                      />
                      <span className="text-xs">{item.label}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Asset Details Panel */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Asset Details</CardTitle>
          </CardHeader>
          <CardContent>
            {selectedAsset ? (
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-muted-foreground">Asset ID</p>
                  <p className="font-medium">{selectedAsset.id}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Name</p>
                  <p className="font-medium">{selectedAsset.name}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Type</p>
                  <Badge variant="outline">{selectedAsset.type}</Badge>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Status</p>
                  <Badge 
                    variant={selectedAsset.status === 'critical' ? 'destructive' : 'secondary'}
                  >
                    {selectedAsset.status}
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Condition Score</p>
                  <div className="flex items-center gap-2">
                    <div className="h-2 flex-1 rounded-full bg-gray-200">
                      <div
                        className={cn(
                          "h-full rounded-full",
                          selectedAsset.conditionScore >= 80 ? "bg-green-500" :
                          selectedAsset.conditionScore >= 60 ? "bg-yellow-500" :
                          selectedAsset.conditionScore >= 40 ? "bg-orange-500" : "bg-red-500"
                        )}
                        style={{ width: `${selectedAsset.conditionScore}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium">{selectedAsset.conditionScore}</span>
                  </div>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Dollar at Risk</p>
                  <p className="font-semibold text-lg">{formatCurrency(selectedAsset.dollarAtRisk)}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Location</p>
                  <div className="flex items-start gap-1">
                    <MapPin className="h-4 w-4 text-muted-foreground mt-0.5" />
                    <p className="text-sm">{selectedAsset.location.address}</p>
                  </div>
                </div>

                <Button className="w-full" onClick={() => window.location.href = `/assets/${selectedAsset.id}`}>
                  View Full Details
                </Button>
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <MapPin className="mx-auto h-12 w-12 mb-4 opacity-50" />
                <p>Click on an asset to view details</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
