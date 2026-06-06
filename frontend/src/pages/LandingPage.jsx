import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import ProjectTypeSelect from '../components/ProjectTypeSelect';
import GitHubInput from '../components/GitHubInput';
import AnalyzeButton from '../components/AnalyzeButton';
import ResultCardPlaceholder from '../components/ResultCardPlaceholder';
import FeatureDetectionCard from '../components/FeatureDetectionCard';
import AnalysisReportDashboard from '../components/AnalysisReportDashboard';
import HowItWorksSection from '../components/HowItWorksSection';
import Footer from '../components/Footer';
import { FolderTree, Blocks, BarChart, Route } from 'lucide-react';
import { analyzeRepository } from '../services/api';

export default function LandingPage() {
  const { user } = useAuth();
  const [repoUrl, setRepoUrl] = useState('');
  const [projectType, setProjectType] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showPlaceholder, setShowPlaceholder] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!repoUrl || !projectType) return;
    
    console.log("Analyzing GitHub Repository:", repoUrl, "Type:", projectType);
    
    setIsAnalyzing(true);
    setShowPlaceholder(false);
    setResult(null);
    setError(null);

    try {
      const data = await analyzeRepository(repoUrl, projectType);
      setResult(data);
    } catch (err) {
      console.error(err);
      if (!err.response) {
        setError("Network error: Is the backend running?");
      } else {
        setError(err.response.data.detail || "Invalid request or server error");
      }
    } finally {
      setIsAnalyzing(false);
      setShowPlaceholder(true);
    }
  };

  const features = [
    { icon: FolderTree, title: "Repository Analysis", desc: "Analyze repository structure and architecture." },
    { icon: Blocks, title: "Feature Detection", desc: "Detect technologies and implemented features." },
    { icon: BarChart, title: "Project Evaluation", desc: "Evaluate engineering practices and project maturity." },
    { icon: Route, title: "Improvement Roadmap", desc: "Receive actionable recommendations and next steps." }
  ];

  return (
    <div className="min-h-screen flex flex-col items-center pt-32 overflow-x-hidden relative">
      <Navbar />

      {/* Background ambient light */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none"></div>

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: "easeOut" }}
        className="w-full max-w-4xl mx-auto text-center relative z-10 px-6"
      >
        {user && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-3 px-4 py-2 rounded-full premium-border bg-zinc-900/50 backdrop-blur-sm mb-6"
          >
            <img
              src={user.picture}
              alt={user.name}
              className="w-8 h-8 rounded-full ring-1 ring-zinc-700"
              referrerPolicy="no-referrer"
            />
            <div className="text-left">
              <p className="text-sm font-medium text-zinc-100">{user.name}</p>
              <p className="text-xs text-zinc-500">{user.email}</p>
            </div>
          </motion.div>
        )}

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
          <ProjectTypeSelect
            value={projectType}
            onChange={(e) => setProjectType(e.target.value)}
            disabled={isAnalyzing}
          />
          <GitHubInput value={repoUrl} onChange={(e) => setRepoUrl(e.target.value)} />
          <AnalyzeButton
            isLoading={isAnalyzing}
            onClick={handleAnalyze}
            disabled={!projectType || !repoUrl}
          />
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
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto border-t border-zinc-800/50 pt-16"
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
              {error ? (
                <div className="max-w-2xl mx-auto p-6 bg-red-500/10 border border-red-500/50 rounded-2xl text-red-400 mt-16 text-left">
                  <h3 className="font-semibold text-lg mb-2 flex items-center">
                    <span className="mr-2 text-2xl">⚠️</span> Error Analyzing Repository
                  </h3>
                  <p className="text-red-300/80">{error}</p>
                </div>
              ) : result && result.data ? (
                <div className="max-w-4xl mx-auto p-8 bg-zinc-900/50 premium-border rounded-3xl text-left mt-16 shadow-2xl backdrop-blur-xl">
                  <div className="flex items-start justify-between border-b border-zinc-800/50 pb-6 mb-6">
                    <div>
                      <h2 className="text-3xl font-bold text-white mb-2 flex items-center">
                        <FolderTree className="w-8 h-8 mr-3 text-emerald-400" />
                        {result.data.name}
                        <span className="ml-4 px-3 py-1 rounded-full border border-zinc-700 bg-zinc-800/50 text-xs font-medium text-zinc-400">
                          {result.data.visibility}
                        </span>
                      </h2>
                      <p className="text-zinc-400 text-lg leading-relaxed max-w-2xl">
                        {result.data.description}
                      </p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    <div className="bg-black/40 p-4 rounded-2xl border border-zinc-800/80">
                      <p className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1">Primary Language</p>
                      <p className="text-xl font-semibold text-zinc-200">{result.data.language}</p>
                    </div>
                    <div className="bg-black/40 p-4 rounded-2xl border border-zinc-800/80">
                      <p className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1">Stars</p>
                      <p className="text-xl font-semibold text-amber-400">{result.data.stars.toLocaleString()}</p>
                    </div>
                    <div className="bg-black/40 p-4 rounded-2xl border border-zinc-800/80">
                      <p className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1">Forks</p>
                      <p className="text-xl font-semibold text-blue-400">{result.data.forks.toLocaleString()}</p>
                    </div>
                    <div className="bg-black/40 p-4 rounded-2xl border border-zinc-800/80">
                      <p className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1">Status</p>
                      <p className="text-xl font-semibold text-emerald-400">Found</p>
                    </div>
                  </div>

                  <AnalysisReportDashboard
                    evaluation={result.data.evaluation}
                    recommendations={result.data.recommendations}
                    projectType={result.data.project_type}
                  />
                  
                  {result.data.technologies && result.data.technologies.length > 0 && (
                    <div className="mb-8">
                      <p className="text-xs font-medium text-zinc-500 mb-3 uppercase tracking-wider">Technology Stack (Informational)</p>
                      <div className="flex flex-wrap gap-2">
                        {result.data.technologies.map((tech, idx) => (
                          <span key={idx} className="px-3 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded-lg text-sm text-zinc-300 flex items-center shadow-sm">
                            <Blocks className="w-3.5 h-3.5 mr-2 text-indigo-400" />
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <FeatureDetectionCard
                    capabilities={result.data.capabilities || result.data.features}
                    projectType={result.data.project_type}
                  />

                  <div className="p-5 bg-black/40 rounded-2xl border border-zinc-800/80 shadow-inner group transition-all hover:bg-black/60">
                    <p className="text-xs font-medium text-zinc-500 mb-2 uppercase tracking-wider">Repository URL</p>
                    <div className="flex items-center">
                      <a href={result.data.repo_url} target="_blank" rel="noreferrer" className="text-emerald-400 hover:text-emerald-300 transition-colors text-lg break-all">
                        {result.data.repo_url}
                      </a>
                    </div>
                  </div>
                </div>
              ) : (
                <ResultCardPlaceholder />
              )}
            </motion.div>
          ) : null}
        </AnimatePresence>
      </motion.div>

      {/* How It Works and Footer Section (Fades in if not analyzing) */}
      <AnimatePresence>
        {!showPlaceholder && !isAnalyzing && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="w-full mt-16 relative z-10"
          >
            <HowItWorksSection />
            <Footer />
          </motion.div>
        )}
      </AnimatePresence>

    </div>
  );
}
