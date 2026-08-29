import type { Metadata } from 'next';
import './globals.css';
import { Sidebar } from '@/components/layout/Sidebar';
import { TopNav } from '@/components/layout/TopNav';

export const metadata: Metadata = {
  title: 'ZentraSec AI | Cybersecurity Posture',
  description: 'AI-Powered Cybersecurity Incident Response & Threat Intelligence Platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex h-screen overflow-hidden bg-background">
        <Sidebar className="w-64 flex-none border-r border-[#27272a] bg-[#09090b] shadow-2xl z-10" />
        <div className="flex flex-col flex-1 overflow-hidden relative">
          {/* Subtle gradient background element */}
          <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-blue-900/10 blur-[120px] pointer-events-none" />
          <div className="absolute bottom-[-20%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-900/10 blur-[120px] pointer-events-none" />
          
          <TopNav className="h-16 flex-none border-b border-[#27272a] bg-[#09090b]/80 backdrop-blur-md z-10" />
          <main className="flex-1 overflow-y-auto p-6 z-10 relative">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
