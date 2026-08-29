'use client';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { motion } from 'framer-motion';

const data = [
  { name: 'Malware', value: 35, color: '#f43f5e' },
  { name: 'Phishing', value: 25, color: '#f59e0b' },
  { name: 'DDoS', value: 20, color: '#3b82f6' },
  { name: 'Data Exfil', value: 15, color: '#a855f7' },
  { name: 'Insider', value: 5, color: '#10b981' },
];

export function ThreatDistribution() {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-panel p-5 rounded-xl border border-[#27272a] h-[350px] flex flex-col"
    >
      <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
        <div className="w-1.5 h-1.5 rounded-full bg-indigo-500"></div>
        Threat Category Distribution
      </h3>
      <div className="flex-1 min-h-0 w-full relative">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="45%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
              stroke="none"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
              itemStyle={{ color: '#fff' }}
            />
            <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px', color: '#a1a1aa' }} />
          </PieChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none pb-8">
          <div className="text-center">
            <span className="block text-2xl font-bold text-white">412</span>
            <span className="block text-[10px] text-zinc-500 uppercase tracking-widest">Total</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
