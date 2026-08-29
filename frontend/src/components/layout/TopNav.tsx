'use client';
import { Search, Bell, User, Settings, AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';

export function TopNav({ className }: { className?: string }) {
  return (
    <header className={cn("flex items-center justify-between px-6", className)}>
      <div className="flex-1 max-w-xl hidden md:flex items-center relative">
        <Search className="w-4 h-4 text-zinc-500 absolute left-3" />
        <input 
          type="text" 
          placeholder="Search IPs, domains, incidents, or ask Copilot..." 
          className="w-full bg-[#18181b] border border-[#27272a] rounded-lg py-1.5 pl-9 pr-4 text-sm text-zinc-200 placeholder:text-zinc-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 transition-all"
        />
        <div className="absolute right-2 flex items-center gap-1">
          <kbd className="hidden sm:inline-flex items-center justify-center px-1.5 py-0.5 text-[10px] font-medium text-zinc-500 bg-[#27272a] rounded border border-[#3f3f46]">⌘</kbd>
          <kbd className="hidden sm:inline-flex items-center justify-center px-1.5 py-0.5 text-[10px] font-medium text-zinc-500 bg-[#27272a] rounded border border-[#3f3f46]">K</kbd>
        </div>
      </div>

      <div className="flex items-center space-x-4 ml-auto">
        <button className="relative p-2 text-zinc-400 hover:text-white transition-colors rounded-full hover:bg-[#18181b]">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500 border border-[#09090b]"></span>
        </button>
        <div className="w-px h-5 bg-[#27272a]"></div>
        <div className="flex items-center gap-2 cursor-pointer group">
          <div className="w-8 h-8 rounded-full bg-[#18181b] border border-[#27272a] flex items-center justify-center group-hover:border-zinc-500 transition-colors">
            <User className="w-4 h-4 text-zinc-400" />
          </div>
        </div>
      </div>
    </header>
  );
}
