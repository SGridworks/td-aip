# T&D Asset Investment Planning (AIP) Frontend

A professional React frontend for Transmission & Distribution utility asset management, risk visualization, and investment planning.

## Features

### Asset Management
- **Asset Table**: Comprehensive listing of T&D assets (transformers, breakers, lines, switches, substations)
- **Asset Detail View**: Detailed information with failure modes and condition history
- **Map View**: Geographic visualization of assets and network connectivity

### Risk Visualization
- **Dollar-at-Risk Heatmap**: Color-coded risk visualization by asset
- **Risk Trend Charts**: Historical risk metrics over time
- **Network Risk Propagation**: Interactive network graph showing risk spread

### Investment Planning
- **Project Management**: Create and manage investment projects
- **Scenario Comparison**: Compare different budget scenarios side-by-side
- **Optimization Engine**: AI-powered project selection for optimal risk reduction

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI component library
- **Recharts** - Data visualization
- **React Flow** - Network graphs
- **React Router** - Navigation

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Install tailwindcss-animate (required for shadcn)
npm install -D tailwindcss-animate

# Run development server
npm run dev
```

### Build for Production

```bash
npm run build
```

## Project Structure

```
src/
├── components/
│   ├── ui/              # shadcn/ui components
│   ├── layout/          # Layout components (Sidebar)
│   ├── dashboard/       # Dashboard views
│   ├── assets/          # Asset management views
│   ├── risk/            # Risk visualization views
│   └── planning/        # Investment planning views
├── data/
│   └── mockData.ts      # Mock data for demo
├── types/
│   └── index.ts         # TypeScript types
├── lib/
│   └── utils.ts         # Utility functions
├── App.tsx              # Main app component
└── main.tsx             # Entry point
```

## Key Components

### Asset Management
- `AssetList` - Paginated, filterable asset table
- `AssetDetail` - Asset details with tabs for failure modes, condition history, projects
- `AssetMap` - SVG-based geographic asset visualization

### Risk Visualization
- `RiskOverview` - Risk metrics dashboard with trend charts
- `RiskHeatmap` - Color-coded asset risk grid
- `RiskNetwork` - Interactive network graph with React Flow

### Investment Planning
- `ProjectList` - Project management with creation dialog
- `ScenarioComparison` - Side-by-side scenario comparison
- `OptimizationResults` - AI optimization engine interface

## Mock Data

The application includes comprehensive mock data for demonstration:
- 12 T&D assets across 5 types
- Multiple failure modes and condition history records
- 5 sample projects across different types
- 3 planning scenarios with varying budgets
- 8 quarters of risk metrics for trend analysis

## License

MIT
