import os

frontend_dir = r"c:\Users\harih\Zensec\frontend\src"

reports_tsx = """'use client';
import { FileText, CheckCircle2, XCircle, Activity, Download, ShieldCheck } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const resolvedIncidents = [
  { 
    id: 'INC-7842', 
    problem: 'Multiple Failed Root Logins Followed By Success & Suspicious Data Transfer',
    time: '2026-08-21 10:44:03 (Contained at 10:47:12)',
    resolution: 'Root account suspended, attacker IP (185.15.2.14) blocked globally, Prod-DB-01 isolated.',
    analyst: 'sec-admin-01'
  },
  { 
    id: 'INC-7839', 
    problem: 'Impossible Travel: login from RU and US context anomaly',
    time: '2026-08-21 09:12:33 (Contained at 09:15:00)',
    resolution: 'Forced MFA Verification invoked and Active Sessions revoked.',
    analyst: 'sec-admin-01'
  },
  { 
    id: 'INC-7822', 
    problem: 'Ransomware precursor malware signature detected on HR workstation',
    time: '2026-08-20 14:33:10 (Contained at 14:34:05)',
    resolution: 'Endpoint automatically quarantined via EDR policy. Process terminated.',
    analyst: 'System AI'
  }
];

const loginMonitors = [
  { target: 'App-Server-Web', user: 'j.smith', status: 'Positive', ip: '10.0.1.4', time: '10:45:11' },
  { target: 'Admin-Portal', user: 'root', status: 'Negative', ip: '185.15.2.14', time: '10:43:10' },
  { target: 'Admin-Portal', user: 'root', status: 'Negative', ip: '185.15.2.14', time: '10:43:11' },
  { target: 'Prod-DB-01', user: 'svc_backup', status: 'Positive', ip: '10.0.1.8', time: '10:42:05' },
  { target: 'App-Server-Web', user: 'm.johnson', status: 'Positive', ip: '91.12.33.1', time: '10:40:22' },
  { target: 'Mail-Server', user: 'admin', status: 'Negative', ip: '45.33.22.1', time: '10:35:14' },
];

export default function ReportsPage() {
  return (
    <div className="max-w-[1600px] mx-auto pb-10 space-y-6 flex flex-col h-[calc(100vh-6rem)]">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-white mb-1">Compliance & Audit Reports</h1>
          <p className="text-zinc-400 text-sm">Archived incident workflows and monitored system authentication telemetry.</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-[#18181b] border border-[#27272a] hover:bg-[#27272a] transition-colors rounded-lg text-sm text-zinc-200 font-medium">
          <Download className="w-4 h-4" /> Export CSV
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-1 overflow-hidden">
        
        {/* Incident Reports Panel */}
        <div className="glass-panel border border-[#27272a] rounded-xl flex flex-col overflow-hidden">
          <div className="p-4 border-b border-[#27272a] bg-[#18181b]/50 flex items-center gap-2">
            <FileText className="w-5 h-5 text-indigo-400" />
            <h2 className="text-lg font-semibold text-white">Resolved Incident Reports</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {resolvedIncidents.map((rep) => (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} key={rep.id} className="bg-[#09090b] border border-[#27272a] rounded-lg p-5">
                <div className="flex justify-between items-start mb-3">
                  <span className="font-mono text-zinc-500 text-xs">{rep.id}</span>
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                    <ShieldCheck className="w-3 h-3" /> Solved
                  </span>
                </div>
                
                {/* Highlighted Problem Text */}
                <div className="mb-4">
                  <span className="text-xs text-zinc-500 block mb-1">Incident Problem:</span>
                  <div className="bg-emerald-900/20 border border-emerald-500/30 px-3 py-2 rounded-md">
                     <p className="text-sm font-medium text-emerald-400 line-through decoration-emerald-500/50 decoration-2">
                        {rep.problem}
                     </p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div>
                    <span className="text-zinc-500 block mb-1">Time Profile:</span>
                    <span className="text-zinc-300 font-mono">{rep.time}</span>
                  </div>
                  <div>
                    <span className="text-zinc-500 block mb-1">How it was solved:</span>
                    <span className="text-zinc-300">{rep.resolution}</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Website Logins Monitor */}
        <div className="glass-panel border border-[#27272a] rounded-xl flex flex-col overflow-hidden">
          <div className="p-4 border-b border-[#27272a] bg-[#18181b]/50 flex items-center justify-between">
             <div className="flex items-center gap-2">
               <Activity className="w-5 h-5 text-blue-400" />
               <h2 className="text-lg font-semibold text-white">Live Website Logins Monitor</h2>
             </div>
             <div className="flex gap-2">
               <span className="flex items-center gap-1 text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded"><CheckCircle2 className="w-3 h-3"/> Positive</span>
               <span className="flex items-center gap-1 text-xs text-rose-400 bg-rose-500/10 px-2 py-1 rounded"><XCircle className="w-3 h-3"/> Negative</span>
             </div>
          </div>
          <div className="flex-1 overflow-y-auto p-0">
             <table className="w-full text-sm text-left">
               <thead className="text-xs text-zinc-500 bg-[#09090b] sticky top-0 border-b border-[#27272a] uppercase">
                 <tr>
                   <th className="px-5 py-3 font-medium">Time (24H)</th>
                   <th className="px-5 py-3 font-medium">Target Service</th>
                   <th className="px-5 py-3 font-medium">Username</th>
                   <th className="px-5 py-3 font-medium">Source IP</th>
                   <th className="px-5 py-3 font-medium text-right">Auth Result</th>
                 </tr>
               </thead>
               <tbody className="divide-y divide-[#27272a]">
                 {loginMonitors.map((log, idx) => (
                   <motion.div as="tr" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: idx * 0.1 }} key={idx} className="hover:bg-[#18181b]/50 transition-colors">
                     <td className="px-5 py-3 font-mono text-xs text-zinc-400">{log.time}</td>
                     <td className="px-5 py-3 text-zinc-200">{log.target}</td>
                     <td className="px-5 py-3 font-medium text-indigo-300">{log.user}</td>
                     <td className="px-5 py-3 font-mono text-zinc-500 text-xs">{log.ip}</td>
                     <td className="px-5 py-3 text-right">
                       <span className={cn(
                         "inline-flex items-center gap-1.5 px-2 py-1 rounded-[4px] text-xs font-bold uppercase",
                         log.status === 'Positive' ? "bg-emerald-500/10 text-emerald-500 border border-emerald-500/20" : "bg-rose-500/10 text-rose-500 border border-rose-500/20"
                       )}>
                         {log.status === 'Positive' ? <CheckCircle2 className="w-3 h-3"/> : <XCircle className="w-3 h-3"/>}
                         {log.status}
                       </span>
                     </td>
                   </motion.div>
                 ))}
               </tbody>
             </table>
          </div>
        </div>

      </div>
    </div>
  );
}
"""

with open(os.path.join(frontend_dir, "app", "reports", "page.tsx"), "w") as f:
    f.write(reports_tsx)

print("Reports Component generated.")
