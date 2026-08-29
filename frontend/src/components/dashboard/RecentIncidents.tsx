'use client';
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
