'use client';

import { Settings } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div className="max-w-[800px] mx-auto pb-10">
      <h1 className="text-3xl font-semibold tracking-tight text-white mb-1">Settings</h1>
      <p className="text-zinc-400 text-sm mb-8">Platform configuration and preferences.</p>
      <div className="glass-panel border border-[#27272a] rounded-xl p-8 text-center">
        <Settings className="w-12 h-12 text-zinc-600 mx-auto mb-4" />
        <p className="text-zinc-400 text-sm">Settings panel coming soon.</p>
      </div>
    </div>
  );
}
