'use client';

import { useState } from 'react';
import { FileText, CheckCircle2, XCircle, Activity, Download, ShieldCheck, Clock, ShieldAlert, ListChecks } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

type IncidentReport = {
  id: string;
  title: string;
  severity: string;
  riskScore: number;
  anomalyScore: number;
  status: string;
  detectedAt: string;
  containedAt: string;
  analyst: string;
  asset: string;
  user: string;
  sourceIp: string;
  problemSummary: string;
  processSteps: { step: number; phase: string; detail: string; time: string }[];
  actionsTaken: { action: string; target: string; status: string; time: string; actor: string }[];
  resolution: string;
};

const incidentReports: IncidentReport[] = [
  {
    id: 'INC-7842',
    title: 'Multiple Failed Root Logins Followed By Success',
    severity: 'Critical',
    riskScore: 94,
    anomalyScore: 91,
    status: 'Contained',
    detectedAt: '2026-08-21 10:44:03',
    containedAt: '2026-08-21 10:47:12',
    analyst: 'sec-admin-01',
    asset: 'Prod-DB-01',
    user: 'root',
    sourceIp: '185.15.2.14',
    problemSummary:
      'An adversary executed a brute-force attack against the root account on Prod-DB-01. After multiple failed authentication attempts, a successful login occurred from an unusual offshore IP. ML anomaly detection flagged escalating behavior (15 → 91/100). Threat intelligence marked the source IP as suspicious. Privilege escalation and sensitive document access followed, indicating a possible account compromise (MITRE T1078).',
    processSteps: [
      { step: 1, phase: 'Event Collection', detail: 'Failed login events ingested from Active Directory and firewall logs.', time: '10:41:00' },
      { step: 2, phase: 'ML Anomaly Detection', detail: 'Isolation Forest detected abnormal login frequency. Anomaly score rose from 22 to 78.', time: '10:42:15' },
      { step: 3, phase: 'Threat Intelligence', detail: 'Source IP 185.15.2.14 enriched — reputation: Suspicious (DEMO/SIMULATED TI).', time: '10:42:30' },
      { step: 4, phase: 'Event Correlation', detail: 'Seven related alerts grouped into single incident: Possible Account Compromise.', time: '10:43:00' },
      { step: 5, phase: 'Risk Scoring', detail: 'Final risk score calculated: 94/100 — CRITICAL (separate from ML anomaly score).', time: '10:43:45' },
      { step: 6, phase: 'AI Copilot Analysis', detail: 'Copilot recommended account restriction, session revocation, and IP blocking.', time: '10:44:03' },
      { step: 7, phase: 'Analyst Approval', detail: 'Analyst sec-admin-01 reviewed and approved response playbook.', time: '10:45:20' },
      { step: 8, phase: 'Response Execution', detail: 'Containment actions executed. Incident status updated to Contained.', time: '10:47:12' },
    ],
    actionsTaken: [
      { action: 'Restrict Account', target: 'root', status: 'SUCCESS', time: '10:45:45', actor: 'sec-admin-01' },
      { action: 'Revoke Active Sessions', target: 'root', status: 'SUCCESS', time: '10:46:02', actor: 'sec-admin-01' },
      { action: 'Block Suspicious IP', target: '185.15.2.14', status: 'SUCCESS', time: '10:46:18', actor: 'sec-admin-01' },
      { action: 'Isolate Affected Endpoint', target: 'Prod-DB-01', status: 'SUCCESS', time: '10:47:12', actor: 'sec-admin-01' },
    ],
    resolution: 'Root account suspended, attacker IP blocked globally, Prod-DB-01 isolated via EDR. No further unauthorized access detected post-containment.',
  },
  {
    id: 'INC-7839',
    title: 'Impossible Travel: Context Anomaly',
    severity: 'Medium',
    riskScore: 65,
    anomalyScore: 58,
    status: 'Resolved',
    detectedAt: '2026-08-21 09:12:33',
    containedAt: '2026-08-21 09:15:00',
    analyst: 'sec-admin-01',
    asset: 'm.johnson@corp.com',
    user: 'm.johnson',
    sourceIp: '91.12.33.1',
    problemSummary: 'Login activity detected from geographically impossible locations within a short time window, indicating possible credential misuse.',
    processSteps: [
      { step: 1, phase: 'Event Collection', detail: 'Authentication events collected from SSO provider.', time: '09:10:00' },
      { step: 2, phase: 'ML Anomaly Detection', detail: 'Location-change anomaly detected. Score: 58/100 — MEDIUM.', time: '09:11:20' },
      { step: 3, phase: 'Event Correlation', detail: 'Login events from RU and US correlated to single user session.', time: '09:12:00' },
      { step: 4, phase: 'Response Execution', detail: 'MFA forced and sessions revoked.', time: '09:15:00' },
    ],
    actionsTaken: [
      { action: 'Force MFA Verification', target: 'm.johnson', status: 'SUCCESS', time: '09:14:30', actor: 'sec-admin-01' },
      { action: 'Revoke Active Sessions', target: 'm.johnson', status: 'SUCCESS', time: '09:15:00', actor: 'sec-admin-01' },
    ],
    resolution: 'Forced MFA verification invoked and all active sessions revoked. User confirmed legitimate travel; incident closed.',
  },
];

const loginMonitors = [
  { target: 'App-Server-Web', user: 'j.smith', status: 'Positive', ip: '10.0.1.4', time: '10:45:11' },
  { target: 'Admin-Portal', user: 'root', status: 'Negative', ip: '185.15.2.14', time: '10:43:10' },
  { target: 'Admin-Portal', user: 'root', status: 'Negative', ip: '185.15.2.14', time: '10:43:11' },
  { target: 'Prod-DB-01', user: 'svc_backup', status: 'Positive', ip: '10.0.1.8', time: '10:42:05' },
  { target: 'App-Server-Web', user: 'm.johnson', status: 'Positive', ip: '91.12.33.1', time: '10:40:22' },
  { target: 'Mail-Server', user: 'admin', status: 'Negative', ip: '45.33.22.1', time: '10:35:14' },
];

function buildReportDocument(report: IncidentReport): string {
  const lines = [
    '================================================================',
    '           ZENTRASEC AI — INCIDENT RESPONSE REPORT',
    '================================================================',
    '',
    `Incident ID:       ${report.id}`,
    `Title:             ${report.title}`,
    `Severity:          ${report.severity}`,
    `Risk Score:        ${report.riskScore}/100`,
    `Anomaly Score:     ${report.anomalyScore}/100`,
    `Status:            ${report.status}`,
    `Detected:          ${report.detectedAt}`,
    `Contained:         ${report.containedAt}`,
    `Analyst:           ${report.analyst}`,
    '',
    '--- TARGET DETAILS ---',
    `Asset:             ${report.asset}`,
    `User:              ${report.user}`,
    `Source IP:         ${report.sourceIp}`,
    '',
    '--- PROBLEM SUMMARY ---',
    report.problemSummary,
    '',
    '--- INCIDENT PROCESS (WORKFLOW) ---',
    ...report.processSteps.map(
      (s) => `${s.step}. [${s.time}] ${s.phase}\n   ${s.detail}`
    ),
    '',
    '--- ACTIONS TAKEN ---',
    ...report.actionsTaken.map(
      (a) => `- [${a.time}] ${a.action} → ${a.target} | Status: ${a.status} | By: ${a.actor}`
    ),
    '',
    '--- RESOLUTION ---',
    report.resolution,
    '',
    '--- AUDIT TRAIL ---',
    'DETECTED    → System',
    'RECOMMENDED → AI Copilot',
    `APPROVED    → ${report.analyst}`,
    `EXECUTED    → ${report.analyst}`,
    `CLOSED      → ${report.status}`,
    '',
    '================================================================',
    'Generated by ZentraSec AI | Confidential',
    `Report generated: ${new Date().toISOString()}`,
    '================================================================',
  ];
  return lines.join('\n');
}

function downloadReport(report: IncidentReport) {
  const content = buildReportDocument(report);
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `ZentraSec_Report_${report.id}.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export default function ReportsPage() {
  const [selectedReport, setSelectedReport] = useState<IncidentReport>(incidentReports[0]);

  return (
    <div className="max-w-[1600px] mx-auto pb-10 space-y-6">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-white mb-1">Compliance & Audit Reports</h1>
          <p className="text-zinc-400 text-sm">Incident problem details, workflow process, and actions taken.</p>
        </div>
        <button
          onClick={() => downloadReport(selectedReport)}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 transition-colors rounded-lg text-sm text-white font-medium"
        >
          <Download className="w-4 h-4" /> Download Report Document
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Incident list */}
        <div className="glass-panel border border-[#27272a] rounded-xl overflow-hidden">
          <div className="p-4 border-b border-[#27272a] bg-[#18181b]/50 flex items-center gap-2">
            <FileText className="w-5 h-5 text-indigo-400" />
            <h2 className="text-lg font-semibold text-white">Incident Reports</h2>
          </div>
          <div className="p-3 space-y-2">
            {incidentReports.map((rep) => (
              <button
                key={rep.id}
                onClick={() => setSelectedReport(rep)}
                className={cn(
                  'w-full text-left p-3 rounded-lg border transition-colors',
                  selectedReport.id === rep.id
                    ? 'bg-[#18181b] border-indigo-500/50'
                    : 'bg-[#09090b]/50 border-[#27272a] hover:border-zinc-600'
                )}
              >
                <div className="flex justify-between items-start mb-1">
                  <span className="font-mono text-zinc-500 text-xs">{rep.id}</span>
                  <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400">
                    {rep.status}
                  </span>
                </div>
                <p className="text-sm text-white font-medium line-clamp-2">{rep.title}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Full report detail */}
        <div className="lg:col-span-2 space-y-6">
          <div className="glass-panel border border-[#27272a] rounded-xl p-6">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-xl font-bold text-white mb-1">{selectedReport.title}</h2>
                <p className="text-sm text-zinc-400 font-mono">{selectedReport.id}</p>
              </div>
              <span className={cn(
                'text-xs font-bold uppercase px-3 py-1 rounded',
                selectedReport.severity === 'Critical' ? 'bg-red-500/10 text-red-400' : 'bg-yellow-500/10 text-yellow-400'
              )}>
                {selectedReport.severity}
              </span>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="p-3 bg-[#09090b] rounded-lg border border-[#27272a]">
                <div className="text-xs text-zinc-500 mb-1">Risk Score</div>
                <div className="text-lg font-bold text-red-400">{selectedReport.riskScore}/100</div>
              </div>
              <div className="p-3 bg-[#09090b] rounded-lg border border-[#27272a]">
                <div className="text-xs text-zinc-500 mb-1">Anomaly Score</div>
                <div className="text-lg font-bold text-orange-400">{selectedReport.anomalyScore}/100</div>
              </div>
              <div className="p-3 bg-[#09090b] rounded-lg border border-[#27272a]">
                <div className="text-xs text-zinc-500 mb-1">Detected</div>
                <div className="text-xs text-zinc-300 font-mono">{selectedReport.detectedAt}</div>
              </div>
              <div className="p-3 bg-[#09090b] rounded-lg border border-[#27272a]">
                <div className="text-xs text-zinc-500 mb-1">Analyst</div>
                <div className="text-sm text-zinc-200">{selectedReport.analyst}</div>
              </div>
            </div>

            <div className="mb-6">
              <h3 className="text-xs font-semibold text-indigo-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                <ShieldAlert className="w-4 h-4" /> Problem Details
              </h3>
              <p className="text-sm text-zinc-300 leading-relaxed bg-[#18181b] p-4 rounded-lg border border-[#27272a]">
                {selectedReport.problemSummary}
              </p>
            </div>

            <div className="mb-6">
              <h3 className="text-xs font-semibold text-emerald-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                <Clock className="w-4 h-4" /> Incident Process Workflow
              </h3>
              <div className="space-y-3">
                {selectedReport.processSteps.map((step) => (
                  <div key={step.step} className="flex gap-4 bg-[#18181b] p-3 rounded-lg border border-[#27272a]">
                    <div className="w-8 h-8 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center text-sm font-bold shrink-0">
                      {step.step}
                    </div>
                    <div className="flex-1">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-sm font-medium text-white">{step.phase}</span>
                        <span className="text-xs font-mono text-zinc-500">{step.time}</span>
                      </div>
                      <p className="text-xs text-zinc-400">{step.detail}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-xs font-semibold text-blue-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                <ListChecks className="w-4 h-4" /> Actions Taken
              </h3>
              <div className="bg-[#09090b] border border-[#27272a] rounded-lg overflow-hidden">
                <table className="w-full text-sm text-left">
                  <thead className="text-xs text-zinc-500 bg-[#18181b] border-b border-[#27272a] uppercase">
                    <tr>
                      <th className="px-4 py-2 font-medium">Time</th>
                      <th className="px-4 py-2 font-medium">Action</th>
                      <th className="px-4 py-2 font-medium">Target</th>
                      <th className="px-4 py-2 font-medium">Actor</th>
                      <th className="px-4 py-2 font-medium text-right">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#27272a]">
                    {selectedReport.actionsTaken.map((action, idx) => (
                      <tr key={idx} className="hover:bg-[#18181b]/50">
                        <td className="px-4 py-3 font-mono text-xs text-zinc-400">{action.time}</td>
                        <td className="px-4 py-3 text-zinc-200">{action.action}</td>
                        <td className="px-4 py-3 font-mono text-xs text-indigo-400">{action.target}</td>
                        <td className="px-4 py-3 text-zinc-400 text-xs">{action.actor}</td>
                        <td className="px-4 py-3 text-right">
                          <span className="inline-flex items-center gap-1 text-xs font-bold text-emerald-400">
                            <CheckCircle2 className="w-3 h-3" /> {action.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="mt-6 p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg">
              <h4 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4" /> Resolution
              </h4>
              <p className="text-sm text-zinc-300">{selectedReport.resolution}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Login monitor */}
      <div className="glass-panel border border-[#27272a] rounded-xl overflow-hidden">
        <div className="p-4 border-b border-[#27272a] bg-[#18181b]/50 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-400" />
            <h2 className="text-lg font-semibold text-white">Authentication Telemetry</h2>
          </div>
          <div className="flex gap-2">
            <span className="flex items-center gap-1 text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded">
              <CheckCircle2 className="w-3 h-3" /> Positive
            </span>
            <span className="flex items-center gap-1 text-xs text-rose-400 bg-rose-500/10 px-2 py-1 rounded">
              <XCircle className="w-3 h-3" /> Negative
            </span>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-zinc-500 bg-[#09090b] border-b border-[#27272a] uppercase">
              <tr>
                <th className="px-5 py-3 font-medium">Time</th>
                <th className="px-5 py-3 font-medium">Target Service</th>
                <th className="px-5 py-3 font-medium">Username</th>
                <th className="px-5 py-3 font-medium">Source IP</th>
                <th className="px-5 py-3 font-medium text-right">Auth Result</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#27272a]">
              {loginMonitors.map((log, idx) => (
                <tr key={idx} className="hover:bg-[#18181b]/50 transition-colors">
                  <td className="px-5 py-3 font-mono text-xs text-zinc-400">{log.time}</td>
                  <td className="px-5 py-3 text-zinc-200">{log.target}</td>
                  <td className="px-5 py-3 font-medium text-indigo-300">{log.user}</td>
                  <td className="px-5 py-3 font-mono text-zinc-500 text-xs">{log.ip}</td>
                  <td className="px-5 py-3 text-right">
                    <span className={cn(
                      'inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs font-bold uppercase',
                      log.status === 'Positive'
                        ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20'
                        : 'bg-rose-500/10 text-rose-500 border border-rose-500/20'
                    )}>
                      {log.status === 'Positive' ? <CheckCircle2 className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
                      {log.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
