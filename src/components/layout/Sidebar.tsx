import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Database, 
  AlertTriangle, 
  Lightbulb, 
  Map,
  Settings,
  Zap,
  ChevronDown,
  Menu,
  X
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

interface NavItem {
  label: string;
  path: string;
  icon: React.ReactNode;
  children?: { label: string; path: string }[];
}

const navItems: NavItem[] = [
  { label: 'Dashboard', path: '/', icon: <LayoutDashboard className="h-5 w-5" /> },
  { 
    label: 'Assets', 
    path: '/assets', 
    icon: <Database className="h-5 w-5" />,
    children: [
      { label: 'Asset List', path: '/assets' },
      { label: 'Map View', path: '/assets/map' },
    ]
  },
  { 
    label: 'Risk', 
    path: '/risk', 
    icon: <AlertTriangle className="h-5 w-5" />,
    children: [
      { label: 'Risk Overview', path: '/risk' },
      { label: 'Heatmap', path: '/risk/heatmap' },
      { label: 'Network View', path: '/risk/network' },
    ]
  },
  { 
    label: 'Planning', 
    path: '/planning', 
    icon: <Lightbulb className="h-5 w-5" />,
    children: [
      { label: 'Projects', path: '/planning' },
      { label: 'Scenarios', path: '/planning/scenarios' },
      { label: 'Optimization', path: '/planning/optimization' },
    ]
  },
];

export function Sidebar() {
  const location = useLocation();
  const [expanded, setExpanded] = useState<string[]>(['Assets', 'Risk', 'Planning']);
  const [mobileOpen, setMobileOpen] = useState(false);

  const toggleExpand = (label: string) => {
    setExpanded(prev => 
      prev.includes(label) 
        ? prev.filter(l => l !== label)
        : [...prev, label]
    );
  };

  const isActive = (path: string) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  return (
    <>
      {/* Mobile Menu Button */}
      <Button
        variant="ghost"
        size="icon"
        className="fixed top-4 left-4 z-50 lg:hidden"
        onClick={() => setMobileOpen(!mobileOpen)}
      >
        {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
      </Button>

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed left-0 top-0 z-40 h-screen w-64 bg-slate-900 text-white transition-transform duration-300 ease-in-out lg:translate-x-0",
          mobileOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-16 items-center border-b border-slate-800 px-6">
            <Zap className="h-8 w-8 text-blue-400" />
            <div className="ml-3">
              <h1 className="text-lg font-bold">T&D AIP</h1>
              <p className="text-xs text-slate-400">Asset Investment Planning</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto px-4 py-4">
            <ul className="space-y-1">
              {navItems.map((item) => (
                <li key={item.label}>
                  {item.children ? (
                    <div>
                      <button
                        onClick={() => toggleExpand(item.label)}
                        className={cn(
                          "flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                          isActive(item.path)
                            ? "bg-blue-600 text-white"
                            : "text-slate-300 hover:bg-slate-800 hover:text-white"
                        )}
                      >
                        <div className="flex items-center">
                          {item.icon}
                          <span className="ml-3">{item.label}</span>
                        </div>
                        <ChevronDown 
                          className={cn(
                            "h-4 w-4 transition-transform",
                            expanded.includes(item.label) && "rotate-180"
                          )} 
                        />
                      </button>
                      {expanded.includes(item.label) && (
                        <ul className="mt-1 space-y-1 pl-10">
                          {item.children.map((child) => (
                            <li key={child.path}>
                              <Link
                                to={child.path}
                                onClick={() => setMobileOpen(false)}
                                className={cn(
                                  "block rounded-lg px-3 py-2 text-sm transition-colors",
                                  isActive(child.path) && location.pathname === child.path
                                    ? "bg-blue-700 text-white"
                                    : "text-slate-400 hover:bg-slate-800 hover:text-white"
                                )}
                              >
                                {child.label}
                              </Link>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ) : (
                    <Link
                      to={item.path}
                      onClick={() => setMobileOpen(false)}
                      className={cn(
                        "flex items-center rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                        isActive(item.path)
                          ? "bg-blue-600 text-white"
                          : "text-slate-300 hover:bg-slate-800 hover:text-white"
                      )}
                    >
                      {item.icon}
                      <span className="ml-3">{item.label}</span>
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </nav>

          {/* Footer */}
          <div className="border-t border-slate-800 p-4">
            <div className="flex items-center gap-3 rounded-lg bg-slate-800 px-3 py-2">
              <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center text-sm font-bold">
                EN
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">Engineer User</p>
                <p className="text-xs text-slate-400 truncate">Senior T&D Planner</p>
              </div>
              <Settings className="h-4 w-4 text-slate-400" />
            </div>
          </div>
        </div>
      </aside>

      {/* Mobile Overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}
    </>
  );
}
