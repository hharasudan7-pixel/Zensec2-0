'use client';
import { motion } from 'framer-motion';
import { Activity, Server, Users, ShieldAlert, Cpu, AlertTriangle } from 'lucide-react';

export default function TimelinePage() {
  return (
    <div className="max-w-[1600px] mx-auto pb-10 space-y-6 flex flex-col h-[calc(100vh-6rem)]">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-white mb-1">Attack Timeline Analysis</h1>
          <p className="text-zinc-400 text-sm">Visualizing correlated events across the network kill chain.</p>
        </div>
      </div>

      <div className="flex-1 glass-panel border border-[#27272a] rounded-xl flex items-center justify-center relative overflow-hidden bg-gradient-to-br from-[#09090b] to-[#18181b]">
        {/* Background Network Graph Placeholder */}
        <div className="absolute inset-0 z-0 opacity-20" style={{
          backgroundImage: 'radial-gradient(circle at 50% 50%, rgba(79, 70, 229, 0.4) 0%, transparent 50%)'
        }}></div>

        <div className="z-10 w-full max-w-5xl p-8">
           <h3 className="text-xl text-white font-medium mb-12 text-center">Correlated Sequence: APT-29 Campaign</h3>
           
           <div className="relative">
             {/* Path Connection */}
             <div className="absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-orange-500 to-red-500 -translate-y-1/2 z-0 rounded-full"></div>

             <div className="relative z-10 flex justify-between">
               
               <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="flex flex-col items-center group">
                 <div className="w-16 h-16 rounded-2xl bg-[#09090b] border-2 border-blue-500 flex items-center justify-center shadow-[0_0_15px_rgba(59,130,246,0.3)] mb-4 group-hover:scale-110 transition-transform">
                   <Activity className="w-8 h-8 text-blue-400" />
                 </div>
                 <span className="text-sm font-bold text-white">Reconnaissance</span>
                 <span className="text-xs text-zinc-500 mt-1">Port Scanning</span>
               </motion.div>

               <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.2 }} className="flex flex-col items-center group">
                 <div className="w-16 h-16 rounded-2xl bg-[#09090b] border-2 border-blue-400 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                   <Users className="w-8 h-8 text-blue-300" />
                 </div>
                 <span className="text-sm font-bold text-white">Initial Access</span>
                 <span className="text-xs text-zinc-500 mt-1">Spearphishing Link</span>
               </motion.div>

               <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.4 }} className="flex flex-col items-center group">
                 <div className="w-16 h-16 rounded-2xl bg-[#09090b] border-2 border-yellow-500 flex items-center justify-center shadow-[0_0_15px_rgba(234,179,8,0.3)] mb-4 group-hover:scale-110 transition-transform">
                   <Cpu className="w-8 h-8 text-yellow-400" />
                 </div>
                 <span className="text-sm font-bold text-white">Execution</span>
                 <span className="text-xs text-zinc-500 mt-1">Powershell Payload</span>
               </motion.div>

               <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.6 }} className="flex flex-col items-center group">
                 <div className="w-16 h-16 rounded-2xl bg-[#09090b] border-2 border-orange-500 flex items-center justify-center shadow-[0_0_15px_rgba(249,115,22,0.3)] mb-4 group-hover:scale-110 transition-transform">
                   <AlertTriangle className="w-8 h-8 text-orange-400" />
                 </div>
                 <span className="text-sm font-bold text-white">Privilege Esc.</span>
                 <span className="text-xs text-zinc-500 mt-1">Token Manipulation</span>
               </motion.div>

               <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: 0.8 }} className="flex flex-col items-center group">
                 <div className="w-16 h-16 rounded-2xl bg-[#09090b] border-2 border-red-500 flex items-center justify-center shadow-[0_0_20px_rgba(239,68,68,0.5)] mb-4 group-hover:scale-110 transition-transform">
                   <ShieldAlert className="w-8 h-8 text-red-500" />
                 </div>
                 <span className="text-sm font-bold text-red-400">Exfiltration</span>
                 <span className="text-xs text-zinc-500 mt-1">Data Encrypted</span>
               </motion.div>

             </div>
           </div>

           <div className="mt-16 bg-[#18181b] border border-[#27272a] rounded-lg p-6 max-w-2xl mx-auto shadow-xl">
             <h4 className="text-white font-medium mb-2 flex items-center gap-2"><Server className="w-4 h-4 text-indigo-400"/> AI Correlation Summary</h4>
             <p className="text-sm text-zinc-400 leading-relaxed">
               ZentraSec AI successfully correlated 43 disparate logs across IIS Web Server, Windows Event Logs (Endpoint), and Palo Alto Firewall into a single unified attack sequence. Anomaly score jumped from <strong className="text-green-400">12 (Benign)</strong> to <strong className="text-red-400">98 (Critical)</strong> during the Privilege Escalation phase.
             </p>
           </div>
        </div>
      </div>
    </div>
  );
}
