import os

frontend_dir = r"c:\Users\harih\Zensec\frontend\src"

copilot_incident_tsx = """'use client';
import { Bot, Clock, ShieldAlert, Crosshair, ListChecks } from 'lucide-react';
import { motion } from 'framer-motion';

export function IncidentCopilotCard({ incident }: { incident: any }) {
  return (
    <div className="bg-[#0c0c0e] border border-[#27272a] rounded-xl overflow-hidden shadow-xl mt-6">
      <div className="p-4 border-b border-[#27272a] bg-gradient-to-r from-indigo-900/20 to-purple-900/20 flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/50 flex items-center justify-center relative shadow-[0_0_15px_rgba(99,102,241,0.2)]">
          <Bot className="w-4 h-4 text-indigo-400" />
          <span className="absolute -top-1 -right-1 w-2 h-2 bg-emerald-500 rounded-full border border-[#09090b] animate-pulse"></span>
        </div>
        <div>
          <h3 className="text-sm font-semibold text-white">AI Copilot Investigation Report</h3>
          <p className="text-[10px] text-zinc-400">RAG Context Analyzed for {incident.id}</p>
        </div>
      </div>

      <div className="p-5 space-y-6">
        {/* Detail and Problem */}
        <div>
          <h4 className="text-xs font-semibold text-indigo-400 uppercase tracking-widest mb-3 flex items-center gap-2">
            <ShieldAlert className="w-4 h-4" /> The Problem
          </h4>
          <p className="text-sm text-zinc-300 leading-relaxed bg-[#18181b] p-4 rounded-lg border border-[#27272a]">
            Based on network telemetry and active directory logs, an adversary has executed a brute-force attack successfully bypassing initial defenses. 
            The system detected non-standard access behavior originating from <strong>{incident.ip}</strong> targeting the <strong>{incident.user}</strong> account on <strong>{incident.asset}</strong>. 
            This matches MITRE ATT&CK T1078 (Valid Accounts). The immediate risk is persistent access and potential lateral movement across the internal subnet.
          </p>
        </div>

        {/* Timeline Details */}
        <div>
          <h4 className="text-xs font-semibold text-emerald-400 uppercase tracking-widest mb-3 flex items-center gap-2">
            <Clock className="w-4 h-4" /> Timeline of Events
          </h4>
          <div className="bg-[#18181b] p-4 rounded-lg border border-[#27272a] space-y-3 relative">
            <div className="absolute left-10 top-6 bottom-6 w-px bg-[#27272a]"></div>
            
            <div className="flex gap-4 relative z-10">
              <span className="text-xs font-mono text-zinc-500 w-12 text-right pt-0.5">T-15m</span>
              <div className="w-3 h-3 rounded-full bg-zinc-700 mt-1 shadow-md"></div>
              <div className="text-sm">
                 <span className="text-zinc-200 font-medium">Reconnaissance Detected</span>
                 <p className="text-xs text-zinc-400 mt-0.5">Automated port scan originating from {incident.ip} targeted {incident.asset}.</p>
              </div>
            </div>

            <div className="flex gap-4 relative z-10">
              <span className="text-xs font-mono text-zinc-500 w-12 text-right pt-0.5">T-3m</span>
              <div className="w-3 h-3 rounded-full bg-orange-500 mt-1 shadow-[0_0_10px_rgba(249,115,22,0.5)]"></div>
              <div className="text-sm">
                 <span className="text-orange-400 font-medium">Brute Force Authentication</span>
                 <p className="text-xs text-zinc-400 mt-0.5">Over 50 failed login attempts logged within a 120-second window.</p>
              </div>
            </div>

            <div className="flex gap-4 relative z-10">
              <span className="text-xs font-mono text-red-500 w-12 text-right pt-0.5">Now</span>
              <div className="w-3 h-3 rounded-full bg-red-500 mt-1 shadow-[0_0_10px_rgba(239,68,68,0.5)]"></div>
              <div className="text-sm">
                 <span className="text-red-400 font-medium">Successful Login & Anomaly</span>
                 <p className="text-xs text-zinc-400 mt-0.5">Login successful tracking to an offshore proxy. High-volume outbound connection initiated.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Step-by-Step Response Guide */}
        <div>
          <h4 className="text-xs font-semibold text-blue-400 uppercase tracking-widest mb-3 flex items-center gap-2">
            <ListChecks className="w-4 h-4" /> Recommended Step-by-Step Mitigation
          </h4>
          <div className="space-y-2">
            <motion.div initial={{ x: -10, opacity: 0 }} animate={{ x: 0, opacity: 1 }} className="flex gap-3 bg-[#18181b] p-3 rounded-lg border border-[#27272a]">
              <div className="w-6 h-6 rounded bg-blue-500/20 text-blue-400 flex items-center justify-center text-xs font-bold shrink-0">1</div>
              <div>
                <h5 className="text-sm font-medium text-white mb-1">Halt Active Exploitation</h5>
                <p className="text-xs text-zinc-400">Click <strong className="text-zinc-200">Take Action</strong> above and execute <strong className="text-red-400">Restrict Account</strong> and <strong className="text-red-400">Revoke Active Sessions</strong> to immediately kick the adversary out of the environment.</p>
              </div>
            </motion.div>
            
            <motion.div initial={{ x: -10, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: 0.1 }} className="flex gap-3 bg-[#18181b] p-3 rounded-lg border border-[#27272a]">
              <div className="w-6 h-6 rounded bg-blue-500/20 text-blue-400 flex items-center justify-center text-xs font-bold shrink-0">2</div>
              <div>
                <h5 className="text-sm font-medium text-white mb-1">Prevent Re-entry</h5>
                <p className="text-xs text-zinc-400">Deploy <strong className="text-orange-400">Block Suspicious IP</strong> to your edge firewall to prevent automated callback attempts from {incident.ip}.</p>
              </div>
            </motion.div>

            <motion.div initial={{ x: -10, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ delay: 0.2 }} className="flex gap-3 bg-[#18181b] p-3 rounded-lg border border-[#27272a]">
              <div className="w-6 h-6 rounded bg-blue-500/20 text-blue-400 flex items-center justify-center text-xs font-bold shrink-0">3</div>
              <div>
                <h5 className="text-sm font-medium text-white mb-1">Evidence Preservation</h5>
                <p className="text-xs text-zinc-400">Engage <strong className="text-blue-400">Isolate Affected Endpoint</strong> for {incident.asset} via your EDR platform to preserve memory forensics while containing lateral threat spread.</p>
              </div>
            </motion.div>
          </div>
        </div>

      </div>
    </div>
  );
}
"""

with open(os.path.join(frontend_dir, "components", "dashboard", "IncidentCopilotCard.tsx"), "w") as f:
    f.write(copilot_incident_tsx)

print("IncidentCopilotCard component generated.")
