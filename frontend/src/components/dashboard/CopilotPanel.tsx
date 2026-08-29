'use client';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, ShieldAlert, CheckCircle2, ChevronRight, Lock, UserX, Volume2, VolumeX } from 'lucide-react';
import { cn } from '@/lib/utils';

export function CopilotPanel() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'ZentraSec Copilot deployed. I detect a critical anomaly on Prod-DB-01: Multiple failed root logins followed by a successful login. A suspicious data transfer initiated 2 minutes later. How would you like to proceed?' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);

  // Initialize Speech Synthesis
  const speakText = (text: string) => {
    if (!soundEnabled || typeof window === 'undefined' || !window.speechSynthesis) return;

    // Stop any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    // Try to find a good English voice
    const voices = window.speechSynthesis.getVoices();
    const englishVoice = voices.find(v => v.lang.startsWith('en-') && v.name.includes('Female')) || voices.find(v => v.lang.startsWith('en-'));
    if (englishVoice) {
      utterance.voice = englishVoice;
    }

    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    // Ensure voices are loaded for Chrome
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = () => {
        window.speechSynthesis.getVoices();
      };
    }
    // Speak first initial message if desired (User might have to interact first depending on browser policy)
  }, []);

  const handleSend = (textInput?: string, e?: React.FormEvent) => {
    e?.preventDefault();
    const query = typeof textInput === 'string' ? textInput : input;
    if (!query.trim()) return;

    // Unlock SpeechSynthesis unconditionally on user action
    if (typeof window !== 'undefined' && window.speechSynthesis) {
      const unlockUtterance = new SpeechSynthesisUtterance('');
      window.speechSynthesis.speak(unlockUtterance);
    }

    setMessages(prev => [...prev, { role: 'user', content: query }]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      setIsTyping(false);

      let detailedResponse = "Based on the RAG context from the event logs and MITRE ATT&CK database, this matches T1078, Valid Accounts. I strongly recommend immediate quarantine of Prod-DB-01, blocking the suspicious IP, and revoking all current sessions for the root user. Should I execute this action?";
      if (query.toLowerCase().includes('isolate')) {
        detailedResponse = "I have queued the isolation playbook for App-Server-Web. Please navigate to the Incident Management page to confirm the execution of this containment action.";
      } else if (query.toLowerCase().includes('timeline')) {
        detailedResponse = "The attack initiated 15 minutes ago with external reconnaissance. 3 minutes ago, brute force authentication began, resulting in a successful ingress and subsequent 4.2 Gigabyte data exfiltration.";
      }

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: detailedResponse
      }]);

      // Trigger speaking the response
      speakText(detailedResponse);
    }, 1200);
  };

  return (
    <div className="glass-panel border border-[#27272a] rounded-xl flex flex-col h-full overflow-hidden max-h-[800px]">
      <div className="p-4 border-b border-[#27272a] bg-gradient-to-r from-indigo-900/20 to-purple-900/20 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/20 border border-indigo-500/50 flex items-center justify-center relative">
            <Bot className="w-4 h-4 text-indigo-400" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-500 rounded-full border border-[#09090b]"></span>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">AI Incident Copilot</h3>
            <p className="text-[10px] text-zinc-400">Context-Aware SOC Assistant</p>
          </div>
        </div>
        <button
          onClick={() => {
            setSoundEnabled(!soundEnabled);
            if (soundEnabled && typeof window !== 'undefined') window.speechSynthesis.cancel();
          }}
          className={cn("p-1.5 rounded text-xs transition-colors", soundEnabled ? "text-indigo-400 bg-indigo-500/10" : "text-zinc-500 hover:text-zinc-300")}
          title="Toggle Voice Responses"
        >
          {soundEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-[300px]">
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              key={i}
              className={cn("flex gap-3 max-w-[90%]", msg.role === 'user' ? "ml-auto flex-row-reverse" : "")}
            >
              <div className={cn("w-6 h-6 rounded-md flex items-center justify-center shrink-0 mt-1",
                msg.role === 'user' ? "bg-zinc-800" : "bg-indigo-500/20 text-indigo-400")}>
                {msg.role === 'user' ? <div className="w-3 h-3 rounded-full bg-zinc-500" /> : <Bot className="w-3 h-3" />}
              </div>
              <div className={cn("px-3 py-2 rounded-lg text-sm",
                msg.role === 'user' ? "bg-[#27272a] text-white" : "bg-indigo-500/10 border border-indigo-500/20 text-zinc-200"
              )}>
                {msg.content}

                {msg.role === 'assistant' && i === 0 && (
                  <div className="mt-3 space-y-2">
                    <button onClick={(e) => handleSend('Isolate App-Server-Web', e as any)} className="w-full text-left bg-[#18181b] border border-[#27272a] hover:border-indigo-500/50 p-2 rounded text-xs text-zinc-300 transition-colors flex items-center justify-between group">
                      <span className="flex items-center gap-2"><Lock className="w-3 h-3 text-red-400" /> Isolate App-Server-Web</span>
                      <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                    <button onClick={(e) => handleSend('Suspend root account', e as any)} className="w-full text-left bg-[#18181b] border border-[#27272a] hover:border-indigo-500/50 p-2 rounded text-xs text-zinc-300 transition-colors flex items-center justify-between group">
                      <span className="flex items-center gap-2"><UserX className="w-3 h-3 text-orange-400" /> Suspend root account</span>
                      <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                    <button onClick={(e) => handleSend('Show attack timeline', e as any)} className="w-full text-left bg-[#18181b] border border-[#27272a] hover:border-indigo-500/50 p-2 rounded text-xs text-zinc-300 transition-colors flex items-center justify-between group">
                      <span className="flex items-center gap-2"><ShieldAlert className="w-3 h-3 text-blue-400" /> Show attack timeline</span>
                      <ChevronRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </button>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
          {isTyping && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-3">
              <div className="w-6 h-6 rounded-md bg-indigo-500/20 flex items-center justify-center">
                <Bot className="w-3 h-3 text-indigo-400" />
              </div>
              <div className="px-3 py-2 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-zinc-400 text-sm flex gap-1 items-center">
                <span className="animate-bounce">.</span><span className="animate-bounce delay-75">.</span><span className="animate-bounce delay-150">.</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div className="p-3 border-t border-[#27272a] bg-[#0c0c0e]">
        <form onSubmit={(e) => handleSend(undefined, e)} className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Copilot about this incident..."
            className="w-full bg-[#18181b] border border-[#27272a] rounded-lg py-2.5 pl-3 pr-10 text-sm text-zinc-200 placeholder:text-zinc-500 focus:outline-none focus:border-indigo-500 transition-colors"
          />
          <button
            type="submit"
            disabled={!input.trim()}
            className="absolute right-2 top-2 p-1 text-zinc-400 hover:text-indigo-400 disabled:opacity-50 transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
        <div className="mt-2 text-center flex items-center justify-center gap-2">
          <span className="text-[9px] text-zinc-600">AI responses are strictly based on RAG security context. Verify actions before execution.</span>
        </div>
      </div>
    </div>
  );
}
