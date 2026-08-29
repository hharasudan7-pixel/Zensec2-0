"use client";

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Lock, User, Clock, AlertTriangle, ShieldAlert, CheckCircle2, ChevronRight, Server, Globe, PowerOff } from 'lucide-react';

export default function AnalyticsPage() {
  const [connections, setConnections] = useState<any[]>([]);
  const [selectedConnection, setSelectedConnection] = useState<string>('');
  const [isConnected, setIsConnected] = useState(false);
  
  const [flowEvents, setFlowEvents] = useState<any[]>([]);
  const [metrics, setMetrics] = useState({ active_sessions: 0, traffic_rate: '0 req/s', threat_level: 'Low' });
  const [hasAnomalies, setHasAnomalies] = useState(false);
  
  const [blockTimer, setBlockTimer] = useState<number | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Fetch connections
    fetch('http://localhost:8000/api/v1/connections')
      .then(res => res.json())
      .then(data => setConnections(data))
      .catch(err => console.error("Failed to load connections", err));
  }, []);

  useEffect(() => {
    let timerId: any;
    if (blockTimer !== null && blockTimer > 0) {
      timerId = setInterval(() => {
        setBlockTimer(prev => (prev && prev > 0 ? prev - 1 : 0));
      }, 1000);
    }
    return () => clearInterval(timerId);
  }, [blockTimer]);

  const handleConnect = () => {
    if (!selectedConnection) return;
    
    setIsConnected(true);
    setFlowEvents([]);
    
    if (wsRef.current) wsRef.current.close();
    
    const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/security-flow/${selectedConnection}`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'FLOW_UPDATE') {
        setMetrics(data.metrics);
        setFlowEvents(prev => [...data.events, ...prev].slice(0, 10)); // Keep last 10
        
        if (data.metrics.threat_level === 'Critical' || data.metrics.threat_level === 'High') {
          setHasAnomalies(true);
        } else {
          setHasAnomalies(false);
        }
      }
    };
    
    wsRef.current = ws;
  };
  
  const disconnect = () => {
    if (wsRef.current) wsRef.current.close();
    setIsConnected(false);
  };

  const handleBlockAccount = () => {
    // Simulate hitting the suspend API
    setBlockTimer(420); // 7 minutes
    
    fetch(`http://localhost:8000/api/v1/incidents/SIMULATED/suspend-7min`, {
        method: 'POST'
    }).catch(console.error);
  };

  const formatTimer = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="p-6 md:p-8 space-y-8 min-h-full bg-zinc-950 text-white">
      {/* Header section */}
      <div className="flex flex-col space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
          <Activity className="text-emerald-400 w-8 h-8" />
          Real-Time Security Flow Mapping
        </h1>
        <p className="text-zinc-400 text-lg">
          Live Connection Monitoring & Threat Resolution
        </p>
      </div>

      {/* Connection Section */}
      <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6 shadow-xl backdrop-blur-sm">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Globe className="text-emerald-400" />
          Customer Website Connection ID
        </h2>
        <div className="flex flex-col sm:flex-row gap-4">
          <select 
            className="flex-1 bg-zinc-950 border border-zinc-800 rounded-lg py-3 px-4 focus:outline-none focus:border-emerald-500 transition-colors"
            value={selectedConnection}
            onChange={(e) => setSelectedConnection(e.target.value)}
            disabled={isConnected}
          >
            <option value="">-- Select Connection ID --</option>
            {connections.map(c => (
              <option key={c.connection_id} value={c.connection_id}>
                {c.customer_name} ({c.connection_id}) - {c.website_url}
              </option>
            ))}
          </select>
          
          {!isConnected ? (
            <button 
              onClick={handleConnect}
              disabled={!selectedConnection}
              className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 rounded-lg font-medium transition-colors"
            >
              Start Monitoring
            </button>
          ) : (
            <button 
              onClick={disconnect}
              className="px-6 py-3 bg-red-600 hover:bg-red-500 rounded-lg font-medium transition-colors flex items-center gap-2"
            >
              <PowerOff size={18} /> Stop
            </button>
          )}
        </div>
      </div>

      {/* Security Flow Chart */}
      <AnimatePresence>
        {isConnected && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              
              {/* Metrics */}
              <div className="lg:col-span-1 space-y-4">
                <div className="bg-zinc-900/60 border border-zinc-800 p-5 rounded-xl">
                  <h3 className="text-zinc-400 text-sm mb-1">Active Sessions</h3>
                  <p className="text-2xl font-bold">{metrics.active_sessions}</p>
                </div>
                <div className="bg-zinc-900/60 border border-zinc-800 p-5 rounded-xl">
                  <h3 className="text-zinc-400 text-sm mb-1">Traffic Rate</h3>
                  <p className="text-2xl font-bold">{metrics.traffic_rate}</p>
                </div>
                <div className={`border p-5 rounded-xl ${hasAnomalies ? 'bg-red-900/20 border-red-800/50' : 'bg-emerald-900/20 border-emerald-800/50'}`}>
                  <h3 className="text-zinc-400 text-sm mb-1">Threat Level</h3>
                  <p className={`text-2xl font-bold ${hasAnomalies ? 'text-red-400' : 'text-emerald-400'}`}>{metrics.threat_level}</p>
                </div>
              </div>

              {/* Flow Visualization */}
              <div className="lg:col-span-3 bg-zinc-900/80 border border-zinc-800 rounded-xl p-6 shadow-xl relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 via-blue-500 to-emerald-500 opacity-50"></div>
                <h3 className="text-xl font-semibold mb-6 flex items-center gap-2">
                  <Activity className="w-5 h-5 text-emerald-400" />
                  Live Security Flow Function
                </h3>
                
                <div className="flex justify-between items-center px-4 mb-8">
                  <div className="text-center"><div className="w-12 h-12 rounded-full bg-blue-900/50 border border-blue-500 flex items-center justify-center mx-auto mb-2"><Globe size={20} className="text-blue-400"/></div><span className="text-xs">Ingress</span></div>
                  <div className="flex-1 h-px bg-zinc-800 mx-2 relative"><div className="absolute inset-0 bg-blue-500/50 w-full animate-pulse"></div></div>
                  <div className="text-center"><div className="w-12 h-12 rounded-full bg-indigo-900/50 border border-indigo-500 flex items-center justify-center mx-auto mb-2"><Server size={20} className="text-indigo-400"/></div><span className="text-xs">Detection</span></div>
                  <div className="flex-1 h-px bg-zinc-800 mx-2"></div>
                  <div className="text-center"><div className="w-12 h-12 rounded-full bg-purple-900/50 border border-purple-500 flex items-center justify-center mx-auto mb-2"><ShieldCheck size={20} className="text-purple-400"/></div><span className="text-xs">Asset Memory</span></div>
                  <div className="flex-1 h-px bg-zinc-800 mx-2"></div>
                  <div className="text-center"><div className="w-12 h-12 rounded-full bg-emerald-900/50 border border-emerald-500 flex items-center justify-center mx-auto mb-2"><CheckCircle2 size={20} className="text-emerald-400"/></div><span className="text-xs">Resolution</span></div>
                </div>

                <div className="space-y-3 h-[250px] overflow-y-auto pr-2 custom-scrollbar">
                  {flowEvents.map((evt, idx) => (
                    <div key={idx} className="bg-zinc-950/80 border border-zinc-800 rounded-lg p-3 flex justify-between items-center text-sm">
                      <div className="flex items-center gap-3">
                        <span className="text-zinc-500">{new Date().toLocaleTimeString()}</span>
                        <span className="text-emerald-400 font-medium">[{evt.source}]</span>
                        <span>{evt.event}</span>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${
                        evt.status === 'Blocked' ? 'bg-red-500/20 text-red-400' :
                        evt.status === 'Logged' ? 'bg-blue-500/20 text-blue-400' :
                        'bg-emerald-500/20 text-emerald-400'
                      }`}>
                        {evt.status}
                      </span>
                    </div>
                  ))}
                  {flowEvents.length === 0 && (
                    <div className="text-center text-zinc-500 py-10 flex flex-col items-center gap-2">
                       <div className="w-6 h-6 border-2 border-zinc-700 border-t-zinc-400 rounded-full animate-spin" />
                       Waiting for traffic...
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Incident Mitigation & Block Action */}
            <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-6 shadow-xl relative overflow-hidden">
               {blockTimer !== null && blockTimer > 0 && (
                 <div className="absolute inset-0 bg-red-950/20 backdrop-blur-[1px] pointer-events-none border border-red-500/30 rounded-xl z-10 flex items-center justify-center">
                    <div className="bg-red-950/90 border border-red-500/50 px-6 py-4 rounded-xl shadow-2xl flex items-center gap-4 animate-pulse">
                       <Lock className="text-red-500 w-8 h-8" />
                       <div>
                         <h3 className="text-red-400 font-bold text-lg">ACCOUNT BLOCKED</h3>
                         <p className="text-red-200 font-mono text-2xl">{formatTimer(blockTimer)}</p>
                       </div>
                    </div>
                 </div>
               )}
               
               <div className="flex justify-between items-center mb-6">
                 <h3 className="text-xl font-semibold flex items-center gap-2">
                   <ShieldAlert className="w-5 h-5 text-amber-400" />
                   Critical Mitigations (Asset Memory)
                 </h3>
               </div>
               
               <p className="text-zinc-400 text-sm mb-6">If critical or unsolved anomalous login activity is detected on the customer's asset memory, you can temporarily suspend their account to stop website operations.</p>
               
               <div className="flex items-center gap-6 p-4 bg-zinc-950 border border-zinc-800 rounded-lg">
                 <div className="flex-1">
                   <h4 className="font-semibold text-zinc-200 mb-1">Temporary User Block (7 Minutes)</h4>
                   <p className="text-xs text-zinc-500">Instantly drops all active sessions and blocks incoming authentication for 7 minutes to contain immediate threats.</p>
                 </div>
                 <button 
                   onClick={handleBlockAccount}
                   disabled={blockTimer !== null && blockTimer > 0}
                   className="px-5 py-2 bg-red-600 hover:bg-red-500 disabled:opacity-50 disabled:hover:bg-red-600 rounded text-sm font-medium transition-colors flex items-center gap-2 whitespace-nowrap"
                 >
                   <Lock size={16} />
                   {blockTimer !== null && blockTimer > 0 ? 'Blocked' : 'Block for 7 Mins'}
                 </button>
               </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      <style dangerouslySetInnerHTML={{__html: `
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(24, 24, 27, 0.5); 
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(82, 82, 91, 0.5); 
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(113, 113, 122, 0.8); 
        }
      `}} />
    </div>
  );
}