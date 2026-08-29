'use client';
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, Server, Users, ShieldAlert, Cpu, AlertTriangle, Loader2 } from 'lucide-react';

interface TimelineEvent {
  sequence: number;
  timestamp: string;
  description: string;
  stage: string;
  event_name: string;
  source: string | null;
  anomaly_score: number | null;
  severity: string | null;
  risk_contribution: number | null;
}

interface IncidentTimeline {
  incident_id: string;
  title: string;
  severity: string;
  risk_score: number;
  description: string;
  stages: string[];
  timeline: TimelineEvent[];
}

export default function TimelinePage() {
  const [data, setData] = useState<IncidentTimeline | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        // 1. Run simulation
        const simRes = await fetch('http://localhost:8000/api/v1/simulate/timeline', {
          method: 'POST'
        });
        if (!simRes.ok) throw new Error('Failed to run simulation');
        const simData = await simRes.json();
        
        if (!simData.incident_id) {
          throw new Error('No incident generated');
        }

        // 2. Fetch timeline
        const tlRes = await fetch(`http://localhost:8000/api/v1/incidents/${simData.incident_id}/timeline`);
        if (!tlRes.ok) throw new Error('Failed to fetch timeline');
        const tlData = await tlRes.json();
        
        setData(tlData);
      } catch (err: any) {
        setError(err.message || 'An error occurred connecting to the backend. Is it running?');
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const getStageIcon = (stage: string) => {
    switch(stage.toLowerCase()) {
      case 'reconnaissance': return <Activity className="w-8 h-8 text-blue-400" />;
      case 'initial access': return <Users className="w-8 h-8 text-blue-300" />;
      case 'execution': return <Cpu className="w-8 h-8 text-yellow-400" />;
      case 'privilege escalation': return <AlertTriangle className="w-8 h-8 text-orange-400" />;
      case 'exfiltration': return <ShieldAlert className="w-8 h-8 text-red-500" />;
      case 'collection': return <Server className="w-8 h-8 text-indigo-400" />;
      default: return <Activity className="w-8 h-8 text-gray-400" />;
    }
  };

  const getStageColorClass = (stage: string) => {
    switch(stage.toLowerCase()) {
      case 'reconnaissance': return 'border-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.3)] text-blue-400';
      case 'initial access': return 'border-blue-400 text-blue-300';
      case 'execution': return 'border-yellow-500 shadow-[0_0_15px_rgba(234,179,8,0.3)] text-yellow-400';
      case 'privilege escalation': return 'border-orange-500 shadow-[0_0_15px_rgba(249,115,22,0.3)] text-orange-400';
      case 'exfiltration': return 'border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.5)] text-red-500';
      case 'collection': return 'border-indigo-500 shadow-[0_0_15px_rgba(99,102,241,0.3)] text-indigo-400';
      default: return 'border-gray-500 text-gray-400';
    }
  };

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
          {loading ? (
            <div className="flex flex-col items-center justify-center text-white py-12">
               <Loader2 className="w-8 h-8 animate-spin mb-4 text-indigo-500" />
               <p>Simulating Attack Sequence & Correlating Events...</p>
            </div>
          ) : error ? (
             <div className="text-red-400 text-center py-12">Error: {error}</div>
          ) : data ? (
            <>
               <h3 className="text-xl text-white font-medium mb-12 text-center">Correlated Sequence: {data.title}</h3>
               
               <div className="relative">
                 {/* Path Connection */}
                 <div className="absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-orange-500 to-red-500 -translate-y-1/2 z-0 rounded-full"></div>

                 <div className="relative z-10 flex justify-between">
                   {data.stages.map((stage, index) => {
                     const colorClass = getStageColorClass(stage);
                     
                     // Find a representative event for this stage to show as description
                     const stageEvents = data.timeline.filter(t => t.stage === stage);
                     const desc = stageEvents.length > 0 ? stageEvents[0].event_name : "Detected Activity";
                     const isLast = index === data.stages.length - 1;
                     const textColor = isLast ? "text-red-400" : "text-white";

                     return (
                       <motion.div key={index} initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay: index * 0.2 }} className="flex flex-col items-center group">
                         <div className={`w-16 h-16 rounded-2xl bg-[#09090b] border-2 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform ${colorClass}`}>
                           {getStageIcon(stage)}
                         </div>
                         <span className={`text-sm font-bold ${textColor}`}>{stage}</span>
                         <span className="text-xs text-zinc-500 mt-1">{desc}</span>
                       </motion.div>
                     );
                   })}
                 </div>
               </div>

               <div className="mt-16 bg-[#18181b] border border-[#27272a] rounded-lg p-6 max-w-2xl mx-auto shadow-xl">
                 <h4 className="text-white font-medium mb-2 flex items-center gap-2">
                   <Server className="w-4 h-4 text-indigo-400"/> AI Correlation Summary
                 </h4>
                 <p className="text-sm text-zinc-400 leading-relaxed">
                   {data.description}
                   <br/><br/>
                   Risk Score: <strong className={data.risk_score > 75 ? "text-red-400" : "text-orange-400"}>{data.risk_score}/100 ({data.severity})</strong> 
                   {" "}| Total Correlated Logs: <strong className="text-white">{data.timeline.length}</strong>
                 </p>
               </div>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
