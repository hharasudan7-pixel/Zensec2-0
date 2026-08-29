import os
import json

base_dir = r"c:\Users\harih\Zensec\frontend\src"

files = {
    "app/incidents/page.tsx": """'use client';
import { useState } from 'react';
import { Shield, ShieldAlert, AlertTriangle, Search, Filter } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const incidentsData = [
  { id: 'INC-7842', title: 'Multiple Failed Root Logins Followed By Success', risk: 94, severity: 'Critical', asset: 'Prod-DB-01', user: 'root', ip: '185.15.2.14', time: '2m ago', status: 'Investigating' },
  { id: 'INC-7841', title: 'Suspicious Powershell Download Cradle', risk: 88, severity: 'High', asset: 'DESKTOP-JSmith', user: 'JSmith', ip: '10.0.4.15', time: '15m ago', status: 'New' },
  { id: 'INC-7840', title: 'Unusual Data Exfiltration Volume', risk: 72, severity: 'High', asset: 'App-Server-Web', user: 'www-data', ip: '45.33.22.1', time: '41m ago', status: 'Open' },
  { id: 'INC-7839', title: 'Impossible Travel: context anomaly', risk: 65, severity: 'Medium', asset: 'm.johnson@corp.com', user: 'm.johnson', ip: '91.12.33.1', time: '1h ago', status: 'Resolved' },
  { id: 'INC-7838', title: 'Malware Signature Detected in Email Attachment', risk: 96, severity: 'Critical', asset: 'Mail-Server', user: 'system', ip: '10.0.1.5', time: '2h ago', status: 'In Progress' },
];

export default function IncidentsPage() {
  const [selectedIncident, setSelectedIncident] = useState(incidentsData[0]);

  return (
    <div className="h-[calc(100vh-6rem)] flex gap-6 max-w-[1600px] mx-auto">
      {/* List */}
      <div className="w-1/3 flex flex-col h-full glass-panel border border-[#27272a] rounded-xl overflow-hidden">
        <div className="p-4 border-b border-[#27272a] bg-[#18181b]/50">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">Incident Queue</h2>
            <div className="flex gap-2">
              <button className="p-1.5 text-zinc-400 hover:text-white bg-[#09090b] rounded border border-[#27272a]"><Filter className="w-4 h-4" /></button>
            </div>
          </div>
          <div className="relative">
            <Search className="w-4 h-4 text-zinc-500 absolute left-3 top-2.5" />
            <input type="text" placeholder="Search incidents..." className="w-full bg-[#09090b] border border-[#27272a] rounded-lg py-2 pl-9 pr-4 text-sm text-zinc-200 focus:border-indigo-500 outline-none" />
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-2">
          {incidentsData.map((inc) => (
            <div 
              key={inc.id}
              onClick={() => setSelectedIncident(inc)}
              className={cn(
                "p-3 rounded-lg border cursor-pointer transition-colors",
                selectedIncident.id === inc.id ? "bg-[#18181b] border-indigo-500/50" : "bg-[#09090b]/50 border-transparent hover:border-[#27272a]"
              )}
            >
              <div className="flex justify-between items-start mb-2">
                <span className="text-xs font-mono text-zinc-500">{inc.id}</span>
                <span className={cn(
                  "text-[10px] px-1.5 py-0.5 rounded uppercase font-bold",
                  inc.severity === 'Critical' ? "bg-red-500/10 text-red-500" : inc.severity === 'High' ? "bg-orange-500/10 text-orange-500" : "bg-yellow-500/10 text-yellow-500"
                )}>{inc.severity}</span>
              </div>
              <h4 className="text-sm font-medium text-white mb-2 line-clamp-2">{inc.title}</h4>
              <div className="flex justify-between items-center text-xs text-zinc-400">
                <span>{inc.asset}</span>
                <span>{inc.time}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Details */}
      <div className="w-2/3 glass-panel border border-[#27272a] rounded-xl overflow-hidden flex flex-col">
        <div className="p-6 border-b border-[#27272a] bg-[#18181b]/50">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-2xl font-bold text-white mb-2">{selectedIncident.title}</h1>
              <div className="flex gap-4 text-sm text-zinc-400">
                <span className="flex items-center gap-1"><ShieldAlert className="w-4 h-4 text-red-500" /> ID: {selectedIncident.id}</span>
                <span className="flex items-center gap-1"><AlertTriangle className="w-4 h-4 text-orange-500" /> Score: {selectedIncident.risk}/100</span>
              </div>
            </div>
            <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors">
              Take Action
            </button>
          </div>
          <div className="grid grid-cols-4 gap-4 mt-6">
            <div className="p-3 bg-[#09090b] rounded-lg border border-[#27272a]">
              <div className="text-xs text-zinc-500 mb-1">Target Asset</div>
              <div className="font-medium text-zinc-200">{selectedIncident.asset}</div>
            </div>
            <div className="p-3 bg-[#09090b] rounded-lg border border-[#27272a]">
              <div className="text-xs text-zinc-500 mb-1">Involved User</div>
              <div className="font-medium text-zinc-200">{selectedIncident.user}</div>
            </div>
            <div className="p-3 bg-[#09090b] rounded-lg border border-[#27272a]">
              <div className="text-xs text-zinc-500 mb-1">Source IP</div>
              <div className="font-mono text-xs text-indigo-400 mt-1">{selectedIncident.ip}</div>
            </div>
            <div className="p-3 bg-[#09090b] rounded-lg border border-[#27272a]">
              <div className="text-xs text-zinc-500 mb-1">Status</div>
              <div className="font-medium text-emerald-400">{selectedIncident.status}</div>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <div>
            <h3 className="text-lg font-semibold text-white mb-4">AI Copilot Analysis</h3>
            <div className="p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-lg text-sm text-zinc-300 leading-relaxed">
              <span className="font-semibold text-indigo-400 block mb-2">Why is this incident critical?</span>
              This sequence matches a known attack pattern (Initial Access → Privilege Escalation → Exfiltration).
              The adversary executed 50 failed login attempts on `root` over 2 minutes, then successfully authenticated. 
              Subsequent telemetry from the host agent indicates an unknown IP ({selectedIncident.ip}) initiated a large compressed data download 
              (4.2GB) out of the network immediately after. 
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Attack Sequence Timeline</h3>
            <div className="space-y-4">
              <div className="flex gap-4">
                <div className="w-12 text-right pt-1"><span className="text-xs text-zinc-500 font-mono">10:41:02</span></div>
                <div className="flex flex-col items-center">
                  <div className="w-3 h-3 rounded-full bg-zinc-600 shrink-0"></div>
                  <div className="w-0.5 h-full bg-[#27272a] my-1"></div>
                </div>
                <div className="pb-4">
                  <div className="bg-[#18181b] border border-[#27272a] p-3 rounded-lg w-full max-w-lg">
                    <h5 className="font-medium text-sm text-rose-400">50 Failed Logins</h5>
                    <p className="text-xs text-zinc-400 mt-1">Auth failures detected for user `root` matching brute-force signatures.</p>
                  </div>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-12 text-right pt-1"><span className="text-xs text-zinc-500 font-mono">10:43:15</span></div>
                <div className="flex flex-col items-center">
                  <div className="w-3 h-3 rounded-full bg-emerald-500 shrink-0 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></div>
                  <div className="w-0.5 h-full bg-[#27272a] my-1"></div>
                </div>
                <div className="pb-4">
                  <div className="bg-[#18181b] border border-[#27272a] p-3 rounded-lg w-full max-w-lg">
                    <h5 className="font-medium text-sm text-emerald-400">Successful Login</h5>
                    <p className="text-xs text-zinc-400 mt-1">Authentication successful from `{selectedIncident.ip}` (unrecognized source).</p>
                  </div>
                </div>
              </div>
              <div className="flex gap-4">
                <div className="w-12 text-right pt-1"><span className="text-xs text-zinc-500 font-mono">10:44:03</span></div>
                <div className="flex flex-col items-center">
                  <div className="w-3 h-3 rounded-full bg-orange-500 shrink-0 shadow-[0_0_10px_rgba(249,115,22,0.5)]"></div>
                  <div className="w-0.5 h-full bg-transparent my-1"></div>
                </div>
                <div className="pb-4">
                  <div className="bg-[#18181b] border border-[#27272a] p-3 rounded-lg w-full max-w-lg">
                    <h5 className="font-medium text-sm text-orange-400">Large Data Exfil Initiated</h5>
                    <p className="text-xs text-zinc-400 mt-1">Network traffic anomaly (4.2GB transferred outbound).</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Incidents page generated successfully.")
