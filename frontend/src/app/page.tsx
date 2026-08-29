import { DashboardStats } from '@/components/dashboard/DashboardStats';
import { ThreatDistribution } from '@/components/dashboard/ThreatDistribution';
import { IncidentTrends } from '@/components/dashboard/IncidentTrends';
import { RecentIncidents } from '@/components/dashboard/RecentIncidents';
import { CopilotPanel } from '@/components/dashboard/CopilotPanel';

export default function Dashboard() {
  return (
    <div className="space-y-6 max-w-[1600px] mx-auto pb-10">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight text-white mb-1">SOC Overview</h1>
          <p className="text-zinc-400 text-sm">Real-time threat monitoring and AI correlation.</p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="flex items-center px-3 py-1.5 rounded-full bg-[#18181b] border border-[#27272a]">
            <span className="w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
            <span className="text-xs text-zinc-300 font-medium">System Active</span>
          </div>
          <span className="text-xs text-zinc-500">Last updated: Just now</span>
        </div>
      </div>

      <DashboardStats />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ThreatDistribution />
            <IncidentTrends />
          </div>
          <RecentIncidents />
        </div>
        
        <div className="lg:col-span-1 h-full">
          <CopilotPanel />
        </div>
      </div>
    </div>
  );
}
