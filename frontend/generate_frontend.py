import os

base_dir = r"c:\Users\harih\Zensec\frontend\src"

files = {
    "app/globals.css": """@import "tailwindcss";

@theme {
  --color-background: #09090b;
  --color-foreground: #fafafa;
  --color-card: #09090b;
  --color-card-foreground: #fafafa;
  --color-popover: #09090b;
  --color-popover-foreground: #fafafa;
  --color-primary: #fafafa;
  --color-primary-foreground: #18181b;
  --color-secondary: #27272a;
  --color-secondary-foreground: #fafafa;
  --color-muted: #27272a;
  --color-muted-foreground: #a1a1aa;
  --color-accent: #27272a;
  --color-accent-foreground: #fafafa;
  --color-destructive: #7f1d1d;
  --color-destructive-foreground: #fafafa;
  --color-border: #27272a;
  --color-input: #27272a;
  --color-ring: #d4d4d8;
  
  --radius-lg: 0.5rem;
  --radius-md: calc(0.5rem - 2px);
  --radius-sm: calc(0.5rem - 4px);
  
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

:root {
  color-scheme: dark;
}

body {
  background-color: var(--color-background);
  color: var(--color-foreground);
  font-family: var(--font-sans);
}

.glass-panel {
  background: rgba(24, 24, 27, 0.4);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
}

.glow-text {
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #3f3f46;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #52525b;
}

@layer base {
  * {
    @apply border-border;
  }
}
""",
    "app/layout.tsx": """import type { Metadata } from 'next';
import './globals.css';
import { Sidebar } from '@/components/layout/Sidebar';
import { TopNav } from '@/components/layout/TopNav';

export const metadata: Metadata = {
  title: 'ZentraSec AI | Cybersecurity Posture',
  description: 'AI-Powered Cybersecurity Incident Response & Threat Intelligence Platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex h-screen overflow-hidden bg-background">
        <Sidebar className="w-64 flex-none border-r border-[#27272a] bg-[#09090b] shadow-2xl z-10" />
        <div className="flex flex-col flex-1 overflow-hidden relative">
          {/* Subtle gradient background element */}
          <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-blue-900/10 blur-[120px] pointer-events-none" />
          <div className="absolute bottom-[-20%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-900/10 blur-[120px] pointer-events-none" />
          
          <TopNav className="h-16 flex-none border-b border-[#27272a] bg-[#09090b]/80 backdrop-blur-md z-10" />
          <main className="flex-1 overflow-y-auto p-6 z-10 relative">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
""",
    "app/page.tsx": """import { DashboardStats } from '@/components/dashboard/DashboardStats';
import { ThreatDistribution } from '@/components/dashboard/ThreatDistribution';
import { IncidentTrends } from '@/components/dashboard/IncidentTrends';
import { RecentIncidents } from '@/components/dashboard/RecentIncidents';
import { CopilotPanel } from '@/components/dashboard/CopilotPanel';

export default function Dashboard() {
  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-10">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-white mb-1">SOC Overview</h1>
          <p className="text-zinc-400 text-sm">Real-time threat monitoring and AI correlation.</p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="flex items-center px-3 py-1.5 rounded-full bg-[#18181b] border border-[#27272a]">
            <span className="w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
            <span className="text-xs text-zinc-300 font-medium">System Active</span>
          </div>
          <span className="text-xs text-zinc-500">Last updated: Just now</span>
        </div>
      </div>

      <DashboardStats />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ThreatDistribution />
            <IncidentTrends />
          </div>
          <RecentIncidents />
        </div>
        
        <div className="lg:col-span-1 h-full">
          <CopilotPanel />
        </div>
      </div>
    </div>
  );
}
""",
    "components/layout/Sidebar.tsx": """'use client';
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
""",
    "components/layout/TopNav.tsx": """'use client';
import { Search, Bell, User, Settings, AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';

export function TopNav({ className }: { className?: string }) {
  return (
    <header className={cn("flex items-center justify-between px-6", className)}>
      <div className="flex-1 max-w-xl hidden md:flex items-center relative">
        <Search className="w-4 h-4 text-zinc-500 absolute left-3" />
        <input 
          type="text" 
          placeholder="Search IPs, domains, incidents, or ask Copilot..." 
          className="w-full bg-[#18181b] border border-[#27272a] rounded-lg py-1.5 pl-9 pr-4 text-sm text-zinc-200 placeholder:text-zinc-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
        />
        <div className="absolute right-2 flex items-center gap-1">
          <kbd className="hidden sm:inline-flex items-center justify-center px-1.5 py-0.5 text-[10px] font-medium text-zinc-500 bg-[#27272a] rounded border border-[#3f3f46]">⌘</kbd>
          <kbd className="hidden sm:inline-flex items-center justify-center px-1.5 py-0.5 text-[10px] font-medium text-zinc-500 bg-[#27272a] rounded border border-[#3f3f46]">K</kbd>
        </div>
      </div>

      <div className="flex items-center space-x-4 ml-auto">
        <button className="relative p-2 text-zinc-400 hover:text-white transition-colors rounded-full hover:bg-[#18181b]">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500 border border-[#09090b]"></span>
        </button>
        <div className="w-px h-5 bg-[#27272a]"></div>
        <div className="flex items-center gap-2 cursor-pointer group">
          <div className="w-8 h-8 rounded-full bg-[#18181b] border border-[#27272a] flex items-center justify-center group-hover:border-zinc-500 transition-colors">
            <User className="w-4 h-4 text-zinc-400" />
          </div>
        </div>
      </div>
    </header>
  );
}
""",
    "components/dashboard/DashboardStats.tsx": """'use client';
import { motion } from 'framer-motion';
import { AlertCircle, Target, ShieldAlert, Cpu, Activity, AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';

const stats = [
  { name: 'Threat Score', value: '92', trend: '+5', trendUp: false, icon: Activity, color: 'text-red-400', bg: 'bg-red-400/10', border: 'border-red-500/20' },
  { name: 'Critical Incidents', value: '3', trend: '+1', trendUp: false, icon: AlertCircle, color: 'text-rose-500', bg: 'bg-rose-500/10', border: 'border-rose-500/20' },
  { name: 'Active Threats', value: '14', trend: '-2', trendUp: true, icon: Target, color: 'text-orange-400', bg: 'bg-orange-400/10', border: 'border-orange-500/20' },
  { name: 'Anomalies Detected', value: '1,284', trend: '+12%', trendUp: false, icon: ShieldAlert, color: 'text-amber-400', bg: 'bg-amber-400/10', border: 'border-amber-500/20' },
  { name: 'High-Risk Users', value: '8', trend: '0', trendUp: true, icon: AlertTriangle, color: 'text-purple-400', bg: 'bg-purple-400/10', border: 'border-purple-500/20' },
  { name: 'Total Events (24h)', value: '2.4M', trend: '+5%', trendUp: true, icon: Cpu, color: 'text-blue-400', bg: 'bg-blue-400/10', border: 'border-blue-500/20' },
];

export function DashboardStats() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      {stats.map((stat, i) => (
        <motion.div
          key={stat.name}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          className={cn(
            "glass-panel rounded-xl p-4 flex flex-col relative overflow-hidden group",
            stat.border
          )}
        >
          <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-white/5 to-transparent rounded-bl-full pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity"></div>
          
          <div className="flex items-center justify-between mb-3">
            <div className={cn("p-2 rounded-lg", stat.bg)}>
              <stat.icon className={cn("w-4 h-4", stat.color)} />
            </div>
            <span className={cn("text-xs font-medium", stat.trendUp ? "text-emerald-400" : "text-red-400")}>
              {stat.trend}
            </span>
          </div>
          
          <h3 className="text-2xl font-bold text-white mb-1 tracking-tight">{stat.value}</h3>
          <p className="text-xs text-zinc-400 font-medium">{stat.name}</p>
        </motion.div>
      ))}
    </div>
  );
}
""",
    "components/dashboard/ThreatDistribution.tsx": """'use client';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { motion } from 'framer-motion';

const data = [
  { name: 'Malware', value: 35, color: '#f43f5e' },
  { name: 'Phishing', value: 25, color: '#f59e0b' },
  { name: 'DDoS', value: 20, color: '#3b82f6' },
  { name: 'Data Exfil', value: 15, color: '#a855f7' },
  { name: 'Insider', value: 5, color: '#10b981' },
];

export function ThreatDistribution() {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-panel p-5 rounded-xl border border-[#27272a] h-[350px] flex flex-col"
    >
      <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
        <div className="w-1.5 h-1.5 rounded-full bg-indigo-500"></div>
        Threat Category Distribution
      </h3>
      <div className="flex-1 min-h-0 w-full relative">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="45%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
              stroke="none"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
              itemStyle={{ color: '#fff' }}
            />
            <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px', color: '#a1a1aa' }} />
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none pb-8">
          <div className="text-center">
            <span className="block text-2xl font-bold text-white">412</span>
            <span className="block text-[10px] text-zinc-500 uppercase tracking-widest">Total</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
""",
    "components/dashboard/IncidentTrends.tsx": """'use client';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';

const data = [
  { time: '00:00', critical: 0, high: 2, medium: 5 },
  { time: '04:00', critical: 1, high: 3, medium: 8 },
  { time: '08:00', critical: 0, high: 5, medium: 15 },
  { time: '12:00', critical: 3, high: 8, medium: 22 },
  { time: '16:00', critical: 2, high: 4, medium: 18 },
  { time: '20:00', critical: 0, high: 2, medium: 7 },
  { time: '24:00', critical: 0, high: 1, medium: 4 },
];

export function IncidentTrends() {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.1 }}
      className="glass-panel p-5 rounded-xl border border-[#27272a] h-[350px] flex flex-col"
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-sm font-semibold text-white flex items-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-rose-500"></div>
          Incident Volume (24h)
        </h3>
        <select className="bg-[#18181b] border border-[#27272a] text-xs text-zinc-400 rounded-md px-2 py-1 outline-none">
          <option>Last 24 Hours</option>
          <option>Last 7 Days</option>
        </select>
      </div>
      <div className="flex-1 min-h-0 w-full ml-[-15px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorCritical" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorHigh" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
            <XAxis dataKey="time" stroke="#52525b" fontSize={10} tickLine={false} axisLine={false} />
            <YAxis stroke="#52525b" fontSize={10} tickLine={false} axisLine={false} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
              itemStyle={{ fontSize: '12px' }}
            />
            <Area type="monotone" dataKey="critical" stroke="#f43f5e" fillOpacity={1} fill="url(#colorCritical)" strokeWidth={2} />
            <Area type="monotone" dataKey="high" stroke="#f59e0b" fillOpacity={1} fill="url(#colorHigh)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
}
""",
    "components/dashboard/RecentIncidents.tsx": """'use client';
import { motion } from 'framer-motion';
import { AlertCircle, Target, Shield, ArrowRight } from 'lucide-react';
import { cn } from '@/lib/utils';

const incidents = [
  { id: 'INC-7842', title: 'Multiple Failed Root Logins Followed By Success', target: 'Prod-DB-01', risk: 94, severity: 'Critical', time: '2m ago', status: 'Investigating' },
  { id: 'INC-7841', title: 'Suspicious Powershell Download Cradle', target: 'DESKTOP-JSmith', risk: 88, severity: 'High', time: '15m ago', status: 'New' },
  { id: 'INC-7840', title: 'Unusual Data Exfiltration Volume', target: 'App-Server-Web', risk: 72, severity: 'High', time: '41m ago', status: 'Open' },
  { id: 'INC-7839', title: 'Impossible Travel: login from RU and US', target: 'm.johnson@corp.com', risk: 65, severity: 'Medium', time: '1h ago', status: 'Resolved' },
];

export function RecentIncidents() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="glass-panel rounded-xl border border-[#27272a] overflow-hidden"
    >
      <div className="p-5 border-b border-[#27272a] flex justify-between items-center bg-[#18181b]/50">
        <h3 className="text-sm font-semibold text-white">Recent Prioritized Incidents</h3>
        <button className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 transition-colors">
          View All <ArrowRight className="w-3 h-3" />
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-zinc-500 bg-[#09090b]/50 border-b border-[#27272a] uppercase">
            <tr>
              <th className="px-5 py-3 font-medium">Incident</th>
              <th className="px-5 py-3 font-medium">Risk Score</th>
              <th className="px-5 py-3 font-medium">Severity</th>
              <th className="px-5 py-3 font-medium">Asset / User</th>
              <th className="px-5 py-3 font-medium">Status</th>
              <th className="px-5 py-3 font-medium">Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#27272a]">
            {incidents.map((incident) => (
              <tr key={incident.id} className="hover:bg-[#18181b]/80 transition-colors group cursor-pointer">
                <td className="px-5 py-4">
                  <div className="flex flex-col">
                    <span className="font-medium text-white group-hover:text-indigo-400 transition-colors">{incident.title}</span>
                    <span className="text-xs text-zinc-500 mt-0.5">{incident.id}</span>
                  </div>
                </td>
                <td className="px-5 py-4">
                  <div className="flex items-center gap-2">
                    <div className="w-full bg-[#27272a] rounded-full h-1.5 max-w-[60px]">
                      <div 
                        className={cn("h-1.5 rounded-full", incident.risk > 90 ? "bg-red-500" : incident.risk > 70 ? "bg-orange-500" : "bg-yellow-500")}
                        style={{ width: `${incident.risk}%` }}
                      ></div>
                    </div>
                    <span className="text-xs font-medium text-zinc-300">{incident.risk}</span>
                  </div>
                </td>
                <td className="px-5 py-4">
                  <span className={cn(
                    "px-2 py-1 text-[10px] font-bold rounded-sm uppercase tracking-wider",
                    incident.severity === 'Critical' ? "bg-red-500/10 text-red-500 border border-red-500/20" : 
                    incident.severity === 'High' ? "bg-orange-500/10 text-orange-500 border border-orange-500/20" :
                    "bg-yellow-500/10 text-yellow-500 border border-yellow-500/20"
                  )}>
                    {incident.severity}
                  </span>
                </td>
                <td className="px-5 py-4 text-zinc-400 text-xs font-medium">{incident.target}</td>
                <td className="px-5 py-4">
                  <span className="text-xs text-zinc-300 flex items-center gap-1.5">
                    <div className={cn("w-1.5 h-1.5 rounded-full", incident.status === 'Resolved' ? 'bg-zinc-600' : 'bg-emerald-500')}></div>
                    {incident.status}
                  </span>
                </td>
                <td className="px-5 py-4 text-zinc-500 text-xs">{incident.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
}
""",
    "components/dashboard/CopilotPanel.tsx": """'use client';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, ShieldAlert, CheckCircle2, ChevronRight, Lock, UserX } from 'lucide-react';
import { cn } from '@/lib/utils';

export function CopilotPanel() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'ZentraSec Copilot deployed. I detect a critical anomaly on Prod-DB-01: Multiple failed root logins followed by a successful login. A suspicious data transfer initiated 2 minutes later. How would you like to proceed?' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim()) return;
    
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      setIsTyping(false);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "Based on the RAG context from the event logs and MITRE ATT&CK base, this matches T1078 (Valid Accounts). I strongly recommend immediate quarantine of Prod-DB-01 and revoking all current sessions for the root user. Should I execute this action?"
      }]);
    }, 1500);
  };

  return (
    <div className="glass-panel border border-[#27272a] rounded-xl flex flex-col h-full overflow-hidden max-h-[800px]">
      <div className="p-4 border-b border-[#27272a] bg-gradient-to-r from-indigo-900/20 to-purple-900/20 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/50 flex items-center justify-center relative">
            <Bot className="w-4 h-4 text-indigo-400" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-500 rounded-full border border-[#09090b]"></span>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">AI Incident Copilot</h3>
            <p className="text-[10px] text-zinc-400">Context-Aware SOC Assistant</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-[300px]">
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              key={i}
              className={cn("flex gap-3 max-w-[90%]", msg.role === 'user' ? "ml-auto flex-row-reverse" : "")}
            >
              <div className={cn("w-6 h-6 rounded-md flex items-center justify-center shrink-0 mt-1", 
                msg.role === 'user' ? "bg-zinc-800" : "bg-indigo-500/20 text-indigo-400")}>
                {msg.role === 'user' ? <div className="w-3 h-3 rounded-full bg-zinc-500" /> : <Bot className="w-3 h-3" />}
              </div>
              <div className={cn("px-3 py-2 rounded-lg text-sm", 
                msg.role === 'user' ? "bg-[#27272a] text-white" : "bg-indigo-500/10 border border-indigo-500/20 text-zinc-200"
              )}>
                {msg.content}
                
                {msg.role === 'assistant' && i === 0 && (
                  <div className="mt-3 space-y-2">
                    <button className="w-full text-left bg-[#18181b] border border-[#27272a] hover:border-indigo-500/50 p-2 rounded text-xs text-zinc-300 transition-colors flex items-center justify-between group">
                      <span className="flex items-center gap-2"><Lock className="w-3 h-3 text-red-400" /> Isolate App-Server-Web</span>
                      <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                    <button className="w-full text-left bg-[#18181b] border border-[#27272a] hover:border-indigo-500/50 p-2 rounded text-xs text-zinc-300 transition-colors flex items-center justify-between group">
                      <span className="flex items-center gap-2"><UserX className="w-3 h-3 text-orange-400" /> Suspend root account</span>
                      <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                    <button className="w-full text-left bg-[#18181b] border border-[#27272a] hover:border-indigo-500/50 p-2 rounded text-xs text-zinc-300 transition-colors flex items-center justify-between group">
                      <span className="flex items-center gap-2"><ShieldAlert className="w-3 h-3 text-blue-400" /> Show attack timeline</span>
                      <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
          {isTyping && (
             <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
               <div className="w-6 h-6 rounded-md bg-indigo-500/20 flex items-center justify-center">
                 <Bot className="w-3 h-3 text-indigo-400" />
               </div>
               <div className="px-3 py-2 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-zinc-400 text-sm flex gap-1 items-center">
                 <span className="animate-bounce">.</span><span className="animate-bounce delay-75">.</span><span className="animate-bounce delay-150">.</span>
               </div>
             </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div className="p-3 border-t border-[#27272a] bg-[#0c0c0e]">
        <form onSubmit={handleSend} className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Copilot about this incident..."
            className="w-full bg-[#18181b] border border-[#27272a] rounded-lg py-2.5 pl-3 pr-10 text-sm text-zinc-200 placeholder:text-zinc-500 focus:outline-none focus:border-indigo-500 transition-colors"
          />
          <button 
            type="submit"
            disabled={!input.trim()}
            className="absolute right-2 top-2 p-1 text-zinc-400 hover:text-indigo-400 disabled:opacity-50 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <div className="mt-2 text-center">
          <span className="text-[9px] text-zinc-600">AI responses are strictly based on RAG security context. Verify actions before execution.</span>
        </div>
      </div>
    </div>
  );
}
""",
    "lib/utils.ts": """import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Files generated successfully.")
