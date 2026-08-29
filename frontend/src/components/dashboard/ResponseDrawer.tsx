'use client';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, X, AlertTriangle, Shield, Terminal, Send, CheckCircle2, XCircle, RotateCcw } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ActionItem {
  id: string;
  name: string;
  description: string;
  target: string;
  severity: 'high' | 'medium' | 'low';
}

const recommendedActions: ActionItem[] = [
  { id: 'restrict_account', name: 'Restrict Account', description: 'Suspend user account in Active Directory', target: 'Inv_User', severity: 'high' },
  { id: 'revoke_sessions', name: 'Revoke Active Sessions', description: 'Terminate all active SSO tokens', target: 'Inv_User', severity: 'medium' },
  { id: 'block_ip', name: 'Block Suspicious IP', description: 'Add rule to edge firewall to drop traffic', target: 'Source_IP', severity: 'high' },
  { id: 'force_mfa', name: 'Force MFA Verification', description: 'Require MFA on next login attempt', target: 'Inv_User', severity: 'low' },
  { id: 'isolate_endpoint', name: 'Isolate Affected Endpoint', description: 'Quarantine host via EDR, allow only management traffic', target: 'Affected_Asset', severity: 'high' },
  { id: 'investigate_data', name: 'Investigate Data Transfer', description: 'Trigger deep inspection on recent outbound payloads', target: 'App-Server-Web', severity: 'low' },
];

export function ResponseDrawer({ incident, isOpen, onClose, onContained }: { incident: any, isOpen: boolean, onClose: () => void, onContained: () => void }) {
  const [selectedActions, setSelectedActions] = useState<string[]>([]);
  const [step, setStep] = useState<'SELECT' | 'CONFIRM' | 'EXECUTING' | 'RESULT'>('SELECT');
  const [execResults, setExecResults] = useState<any[]>([]);
  const [auditLog, setAuditLog] = useState<any[]>([]);

  if (!isOpen) return null;

  const toggleAction = (id: string) => {
    setSelectedActions(prev => prev.includes(id) ? prev.filter(a => a !== id) : [...prev, id]);
  };

  const handleExecute = async () => {
    setStep('EXECUTING');
    
    // Simulate API call to backend
    try {
      const payload = {
        incident_id: incident.id,
        actions: selectedActions.map(id => ({
          action_id: id,
          target: recommendedActions.find(a => a.id === id)?.target.replace('Inv_User', incident.user).replace('Affected_Asset', incident.asset).replace('Source_IP', incident.ip)
        })),
        analyst_id: "sec-admin-01"
      };

      const res = await fetch('http://localhost:8000/api/v1/incidents/' + incident.id + '/response-actions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      const data = await res.json();
      setExecResults(data.results);
      
      const newLogs = data.results.map((r: any) => ({
        id: Math.random().toString(),
        incidentId: incident.id,
        action: recommendedActions.find(a => a.id === r.action_id)?.name,
        target: recommendedActions.find(a => a.id === r.action_id)?.target.replace('Inv_User', incident.user).replace('Affected_Asset', incident.asset).replace('Source_IP', incident.ip),
        analyst: 'sec-admin-01',
        timestamp: new Date().toISOString(),
        status: r.status,
        reason: r.reason
      }));
      setAuditLog(prev => [...prev, ...newLogs]);
      
      setStep('RESULT');
      if (data.status === 'Contained') {
        onContained();
      }
    } catch (err) {
      console.error(err);
      setStep('RESULT');
    }
  };

  const getActionDetails = (id: string) => recommendedActions.find(a => a.id === id);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
            onClick={onClose}
          />
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed top-0 right-0 h-full w-[600px] border-l border-[#27272a] shadow-2xl z-50 flex flex-col bg-[#09090b]"
          >
            <div className="p-6 border-b border-[#27272a] flex items-center justify-between bg-[#18181b]/50">
              <div>
                <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                  <ShieldAlert className="w-5 h-5 text-red-500" />
                  Take Action: {incident.id}
                </h2>
                <p className="text-sm text-zinc-400 mt-1">{incident.title}</p>
              </div>
              <button onClick={onClose} className="p-2 text-zinc-400 hover:text-white rounded-md hover:bg-[#27272a] transition">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="p-3 bg-[#18181b] border border-[#27272a] rounded-lg">
                  <div className="text-zinc-500 text-xs">Risk Score</div>
                  <div className="text-red-400 font-bold">{incident.risk}/100 ({incident.severity})</div>
                </div>
                <div className="p-3 bg-[#18181b] border border-[#27272a] rounded-lg">
                  <div className="text-zinc-500 text-xs">Affected Asset</div>
                  <div className="text-zinc-200">{incident.asset}</div>
                </div>
                <div className="p-3 bg-[#18181b] border border-[#27272a] rounded-lg">
                  <div className="text-zinc-500 text-xs">Involved User</div>
                  <div className="text-zinc-200">{incident.user}</div>
                </div>
                <div className="p-3 bg-[#18181b] border border-[#27272a] rounded-lg">
                  <div className="text-zinc-500 text-xs">Source IP</div>
                  <div className="text-indigo-400 font-mono">{incident.ip}</div>
                </div>
              </div>

              <div className="p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-lg">
                <h3 className="text-sm font-semibold text-indigo-400 mb-2 flex items-center gap-2">
                  <Terminal className="w-4 h-4" /> AI Incident Context
                </h3>
                <p className="text-xs text-zinc-300 leading-relaxed">
                  Based on behavioral anomalies, this incident requires immediate intervention. The sequence matches T1078 (Valid Accounts). Recommended actions focus on isolating the actor and revoking access before data exfiltration completes.
                </p>
              </div>

              {step === 'SELECT' && (
                <div>
                  <h3 className="text-md font-semibold text-white mb-3">Recommended Response Actions</h3>
                  <div className="space-y-3">
                    {recommendedActions.map(action => {
                      const isSelected = selectedActions.includes(action.id);
                      return (
                        <div 
                          key={action.id}
                          onClick={() => toggleAction(action.id)}
                          className={cn(
                            "p-3 rounded-lg border cursor-pointer flex gap-3 transition-colors items-start",
                            isSelected ? "bg-[#18181b] border-indigo-500/50" : "bg-[#09090b] border-[#27272a] hover:border-zinc-500"
                          )}
                        >
                          <div className={cn("w-4 h-4 mt-0.5 border rounded flex items-center justify-center transition-colors", 
                            isSelected ? "bg-indigo-500 border-indigo-500" : "border-zinc-500 bg-transparent"
                          )}>
                            {isSelected && <CheckCircle2 className="w-3 h-3 text-white" />}
                          </div>
                          <div className="flex-1">
                            <div className="flex justify-between items-center mb-1">
                              <span className="text-sm font-medium text-white">{action.name}</span>
                              <span className={cn("text-[10px] px-1.5 py-0.5 rounded uppercase font-bold", 
                                action.severity === 'high' ? "bg-red-500/20 text-red-500" :
                                action.severity === 'medium' ? "bg-orange-500/20 text-orange-500" :
                                "bg-zinc-800 text-zinc-400"
                              )}>{action.severity} Impact</span>
                            </div>
                            <p className="text-xs text-zinc-400">{action.description}</p>
                            <p className="text-[10px] text-zinc-500 mt-2 font-mono">Target: {action.target.replace('Inv_User', incident.user).replace('Affected_Asset', incident.asset).replace('Source_IP', incident.ip)}</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {step === 'CONFIRM' && (
                <div className="animate-in fade-in slide-in-from-right-4 duration-300">
                  <div className="p-4 bg-orange-500/10 border border-orange-500/20 rounded-lg mb-4">
                    <h3 className="text-sm font-semibold text-orange-400 flex items-center gap-2 mb-2">
                       <AlertTriangle className="w-4 h-4" /> Warning: Disruptive Actions
                    </h3>
                    <p className="text-xs text-orange-200">You are about to execute actions that will interrupt active sessions and block network traffic. This requires explicit confirmation.</p>
                  </div>
                  
                  <h4 className="text-sm font-medium text-white mb-2">Actions to Execute:</h4>
                  <ul className="space-y-2 mb-6">
                    {selectedActions.map(id => {
                      const details = getActionDetails(id);
                      return (
                        <li key={id} className="text-xs text-zinc-300 flex justify-between bg-[#18181b] p-2 rounded border border-[#27272a]">
                          <span>{details?.name}</span>
                          <span className="font-mono text-indigo-400">{details?.target.replace('Inv_User', incident.user).replace('Affected_Asset', incident.asset).replace('Source_IP', incident.ip)}</span>
                        </li>
                      );
                    })}
                  </ul>
                </div>
              )}

              {step === 'EXECUTING' && (
                <div className="flex flex-col items-center justify-center py-20 animate-in fade-in">
                  <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin mb-6"></div>
                  <h3 className="text-lg font-medium text-white mb-2">Executing Response Playbook</h3>
                  <p className="text-sm text-zinc-400 text-center max-w-xs">Connecting to identity providers and EDR APIs to orchestrate containment...</p>
                </div>
              )}

              {step === 'RESULT' && (
                <div className="animate-in fade-in slide-in-from-right-4 duration-300 space-y-6">
                  <div>
                    <h3 className="text-md font-semibold text-white mb-3">Execution Verification</h3>
                    <div className="space-y-2">
                      {execResults.map(r => {
                        const details = getActionDetails(r.action_id);
                        return (
                          <div key={r.action_id} className={cn("p-3 rounded-lg border flex items-center justify-between",
                            r.status === 'SUCCESS' ? "bg-emerald-500/10 border-emerald-500/20" : "bg-red-500/10 border-red-500/20"
                          )}>
                            <div className="flex items-center gap-3">
                                {r.status === 'SUCCESS' ? <CheckCircle2 className="w-5 h-5 text-emerald-500" /> : <XCircle className="w-5 h-5 text-red-500" />}
                                <div>
                                  <div className="text-sm font-medium text-white">{details?.name}</div>
                                  <div className="text-xs text-zinc-400">{r.reason}</div>
                                </div>
                            </div>
                            {r.status === 'FAILED' && (
                               <button className="text-xs text-red-400 hover:text-red-300 flex items-center gap-1"><RotateCcw className="w-3 h-3"/> Retry</button>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-md font-semibold text-white mb-3 flex items-center gap-2"><Shield className="w-4 h-4"/> Audit Log</h3>
                    <div className="bg-[#09090b] border border-[#27272a] rounded-lg overflow-hidden">
                      <table className="w-full text-xs text-left">
                        <thead className="text-zinc-500 bg-[#18181b] border-b border-[#27272a] uppercase">
                          <tr>
                            <th className="px-3 py-2 font-medium">Action</th>
                            <th className="px-3 py-2 font-medium">Target</th>
                            <th className="px-3 py-2 font-medium">Status</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-[#27272a]">
                          {auditLog.map(log => (
                            <tr key={log.id}>
                              <td className="px-3 py-2 text-zinc-300">{log.action}</td>
                              <td className="px-3 py-2 text-zinc-500 font-mono">{log.target}</td>
                              <td className={cn("px-3 py-2 font-medium", log.status === 'SUCCESS' ? "text-emerald-400" : "text-red-400")}>{log.status}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="p-6 border-t border-[#27272a] bg-[#18181b]/50 flex justify-end gap-3">
              {step !== 'EXECUTING' && (
                <button onClick={onClose} className="px-4 py-2 text-sm font-medium text-zinc-300 hover:text-white transition">
                  {step === 'RESULT' ? 'Close' : 'Cancel'}
                </button>
              )}
              
              {step === 'SELECT' && (
                <button 
                  onClick={() => setStep('CONFIRM')}
                  disabled={selectedActions.length === 0}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:hover:bg-indigo-600 text-white text-sm font-medium rounded-lg transition"
                >
                  Review Selected ({selectedActions.length})
                </button>
              )}
              
              {step === 'CONFIRM' && (
                <button 
                  onClick={handleExecute}
                  className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg transition flex items-center gap-2"
                >
                  <Send className="w-4 h-4" /> Conform & Execute
                </button>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
