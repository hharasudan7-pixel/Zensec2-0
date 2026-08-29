'use client';
import { Shield, LayoutDashboard, Activity, AlertOctagon, Crosshair, Network, Cpu, FileText, Settings, Bot } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const routes = [
  { href: '/', label: 'Overview', icon: LayoutDashboard },
  { href: '/events', label: 'Live Events', icon: Activity },
  { href: '/incidents', label: 'Incidents', icon: AlertOctagon, badge: 3 },
  { href: '/threats', label: 'Threat Intel', icon: Crosshair },
  { href: '/timeline', label: 'Attack Timeline', icon: Network },
  { href: '/analytics', label: 'Analytics', icon: Bot },
  { href: '/assets', label: 'Assets', icon: Cpu },
  { href: '/reports', label: 'Reports', icon: FileText },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export function Sidebar({ className }: { className?: string }) {
  const pathname = usePathname();

  return (
    <aside className={cn("flex flex-col h-full", className)}>
      <div className="h-16 flex items-center px-6 border-b border-[#27272a]">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="relative flex items-center justify-center w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 group-hover:shadow-[0_0_15px_rgba(79,70,229,0.5)] transition-shadow">
            <Shield className="w-4 h-4 text-white" />
          </div>
          <span className="font-bold text-lg tracking-tight text-white glow-text">ZentraSec AI</span>
        </Link>
      </div>

      <div className="flex-1 overflow-y-auto py-6 px-4 space-y-1">
        <div className="mb-4 px-2 text-xs font-semibold text-zinc-500 uppercase tracking-wider">Navigation</div>
        {routes.map((route) => {
          const isActive = pathname === route.href;
          return (
            <Link 
              key={route.href} 
              href={route.href}
              className={cn(
                "group relative flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium transition-colors",
                isActive 
                  ? "text-white" 
                  : "text-zinc-400 hover:text-white hover:bg-[#18181b]"
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="sidebar-active"
                  className="absolute inset-0 bg-[#18181b] rounded-md -z-10"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              {isActive && (
                <div className="absolute left-0 top-1.5 bottom-1.5 w-1 bg-indigo-500 rounded-r-md" />
              )}
              <div className="flex items-center gap-3">
                <route.icon className={cn("w-4 h-4", isActive ? "text-indigo-400" : "text-zinc-500 group-hover:text-zinc-300")} />
                {route.label}
              </div>
              {route.badge && (
                <span className="inline-flex items-center justify-center w-5 h-5 text-[10px] font-bold text-white bg-destructive rounded-full">
                  {route.badge}
                </span>
              )}
            </Link>
          );
        })}
      </div>
      
      <div className="p-4 border-t border-[#27272a] bg-[#0c0c0e]">
        <div className="glass-panel p-3 rounded-lg border border-[#27272a]">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 flex items-center justify-center text-xs font-bold text-white">
              AI
            </div>
            <div>
              <p className="text-xs font-medium text-white">Copilot Active</p>
              <p className="text-[10px] text-zinc-400">Monitoring 24/7</p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
