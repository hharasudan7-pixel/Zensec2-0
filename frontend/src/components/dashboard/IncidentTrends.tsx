'use client';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';

const data = [
  { time: '00:00', critical: 0, high: 2, medium: 5 },
  { time: '04:00', critical: 1, high: 3, medium: 8 },
  { time: '08:00', critical: 0, high: 5, medium: 15 },
  { time: '12:00', critical: 3, high: 8, medium: 22 },
  { time: '16:00', critical: 2, high: 4, medium: 18 },
  { time: '20:00', critical: 0, high: 2, medium: 7 },
  { time: '24:00', critical: 0, high: 1, medium: 4 },
];

export function IncidentTrends() {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.1 }}
      className="glass-panel p-5 rounded-xl border border-[#27272a] h-[350px] flex flex-col"
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-sm font-semibold text-white flex items-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-rose-500"></div>
          Incident Volume (24h)
        </h3>
        <select className="bg-[#18181b] border border-[#27272a] text-xs text-zinc-400 rounded-md px-2 py-1 outline-none">
          <option>Last 24 Hours</option>
          <option>Last 7 Days</option>
        </select>
      </div>
      <div className="flex-1 min-h-0 w-full ml-[-15px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorCritical" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorHigh" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
            <XAxis dataKey="time" stroke="#52525b" fontSize={10} tickLine={false} axisLine={false} />
            <YAxis stroke="#52525b" fontSize={10} tickLine={false} axisLine={false} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
              itemStyle={{ fontSize: '12px' }}
            />
            <Area type="monotone" dataKey="critical" stroke="#f43f5e" fillOpacity={1} fill="url(#colorCritical)" strokeWidth={2} />
            <Area type="monotone" dataKey="high" stroke="#f59e0b" fillOpacity={1} fill="url(#colorHigh)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </motion.div>
  );
}
