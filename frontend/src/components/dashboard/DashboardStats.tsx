'use client';
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
