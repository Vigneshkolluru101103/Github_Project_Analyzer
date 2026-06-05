import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import GitHubInput from '../components/GitHubInput';
import AnalyzeButton from '../components/AnalyzeButton';
import ResultCardPlaceholder from '../components/ResultCardPlaceholder';
import CTASection from '../components/CTASection';
import Footer from '../components/Footer';
import { Activity, ShieldCheck, Zap } from 'lucide-react';

export default function LandingPage() {
  const [repoUrl, setRepoUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showPlaceholder, setShowPlaceholder] = useState(false);

  const handleAnalyze = () => {
    if (!repoUrl) return;
    setIsAnalyzing(true);
    setShowPlaceholder(false);
    setTimeout(() => {
      setIsAnalyzing(false);
      setShowPlaceholder(true);
    }, 2500);
  };

  const features = [
    { icon: Activity, title: "Code Quality Metrics", desc: "Deep static analysis of your architecture." },
    { icon: Zap, title: "Performance Profiling", desc: "Identify bottlenecks in your frontend and backend." },
    { icon: ShieldCheck, title: "Security Audit", desc: "Detect vulnerabilities and bad practices." }
  ];

  return (
    <div className="min-h-screen flex flex-col items-center pt-32 overflow-x-hidden relative">
      
      {/* Background ambient light */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none"></div>

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: "easeOut" }}
        className="w-full max-w-4xl mx-auto text-center relative z-10 px-6"
      >
        {/* Pill Badge */}
        <div className="inline-flex items-center px-4 py-1.5 rounded-full premium-border bg-zinc-900/50 backdrop-blur-sm text-zinc-400 text-xs font-medium mb-8">
          <span className="flex h-1.5 w-1.5 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
          Recruiter-Ready Analysis Engine
        </div>

        {/* Hero Typography */}
        <h1 className="text-5xl md:text-7xl font-bold tracking-tighter text-white mb-6 leading-tight">
          Review your projects like a <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-b from-white to-zinc-500">
            Senior Engineer.
          </span>
        </h1>
        
        <p className="text-lg md:text-xl text-zinc-400 mb-12 max-w-2xl mx-auto font-light leading-relaxed">
          Drop your GitHub repository below. We analyze your architecture, score your practices, and generate resume-ready bullet points.
        </p>

        {/* Input Form */}
        <div className="mb-24">
          <GitHubInput value={repoUrl} onChange={(e) => setRepoUrl(e.target.value)} />
          <AnalyzeButton isLoading={isAnalyzing} onClick={handleAnalyze} />
        </div>

        {/* Conditional Layout Rendering */}
        <AnimatePresence mode="wait">
          {!showPlaceholder && !isAnalyzing ? (
            <motion.div 
              key="features"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto border-t border-zinc-800/50 pt-16"
            >
              {features.map((feat, i) => (
                <div key={i} className="text-left p-6 premium-border rounded-2xl bg-zinc-900/20 hover:bg-zinc-900/50 transition-colors group">
                  <feat.icon className="w-6 h-6 text-zinc-400 mb-4 group-hover:text-zinc-100 transition-colors" />
                  <h3 className="text-zinc-100 font-medium mb-2">{feat.title}</h3>
                  <p className="text-zinc-500 text-sm leading-relaxed">{feat.desc}</p>
                </div>
              ))}
            </motion.div>
          ) : showPlaceholder ? (
            <motion.div 
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="w-full pb-32 relative z-10"
            >
              <ResultCardPlaceholder />
            </motion.div>
          ) : null}
        </AnimatePresence>
      </motion.div>

      {/* CTA and Footer Section (Fades in if not analyzing) */}
      <AnimatePresence>
        {!showPlaceholder && !isAnalyzing && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="w-full mt-32 relative z-10"
          >
            <CTASection />
            <Footer />
          </motion.div>
        )}
      </AnimatePresence>

    </div>
  );
}
