import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSearchParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import ProjectTypeSelect from '../components/ProjectTypeSelect';
import GitHubInput from '../components/GitHubInput';
import AnalyzeButton from '../components/AnalyzeButton';
import ResultCardPlaceholder from '../components/ResultCardPlaceholder';
import FeatureDetectionCard from '../components/FeatureDetectionCard';
import AnalysisReportDashboard from '../components/AnalysisReportDashboard';
import HowItWorksSection from '../components/HowItWorksSection';
import Footer from '../components/Footer';
import { FolderTree, Blocks, Route, Download, Loader2 } from 'lucide-react';
import { analyzeRepository, downloadSavedReportPdf, downloadRawReportPdf } from '../services/api';
import { useAuth } from '../context/AuthContext';
import AuthModal from '../components/AuthModal';
import toast from 'react-hot-toast';

export default function LandingPage() {
  const [searchParams] = useSearchParams();
  const initialRepoUrl = searchParams.get('repoUrl') || '';

  const [repoUrl, setRepoUrl] = useState(initialRepoUrl);
  const [projectType, setProjectType] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showPlaceholder, setShowPlaceholder] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isDownloading, setIsDownloading] = useState(false);

  const { isAuthenticated } = useAuth();
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const handleAnalyzeClick = () => {
    if (!repoUrl || !projectType) return;
    if (!isAuthenticated) {
      setIsAuthModalOpen(true);
    } else {
      executeAnalysis();
    }
  };

  const handleGuestContinue = () => {
    executeAnalysis();
  };

  const executeAnalysis = async () => {
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

  const [downloadStatus, setDownloadStatus] = useState("Download PDF");

  const handleDownloadPdf = async () => {
    if (!result || !result.data) return;
    setIsDownloading(true);
    setDownloadStatus("Generating PDF...");
    console.log("Downloading PDF for analysis:", result.data.id || "raw");
    
    try {
      let response;
      if (result.data.id) {
        response = await downloadSavedReportPdf(result.data.id);
      } else {
        response = await downloadRawReportPdf(result.data);
      }
      
      setDownloadStatus("Downloading...");
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      const repoName = result.data.name || result.data.repo_name || 'project';
      const safeName = repoName.replace(/[^a-zA-Z0-9]/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
      link.setAttribute('download', `${safeName}-analysis-report.pdf`);
      
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("PDF Download failed", err);
      let errorMsg = "Failed to download PDF. Please try again.";
      if (err.response && err.response.data instanceof Blob) {
        try {
          const text = await err.response.data.text();
          const json = JSON.parse(text);
          if (json.detail) errorMsg = json.detail;
        } catch (e) {
          // ignore parsing error
        }
      } else if (err.response?.data?.detail) {
        errorMsg = err.response.data.detail;
      }
      toast.error(
        <div className="flex flex-col">
          <span className="font-semibold text-white">PDF Download Failed</span>
          <span className="text-zinc-400 text-sm">{errorMsg}</span>
        </div>
      );
    } finally {
      setIsDownloading(false);
      setDownloadStatus("Download PDF");
    }
  };


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
        {/* Pill Badge */}
        <div className="inline-flex items-center px-4 py-1.5 rounded-full premium-border bg-zinc-900/50 backdrop-blur-sm text-zinc-400 text-xs font-medium mb-8">
          <span className="flex h-1.5 w-1.5 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>
          Recruiter-Ready Analysis Engine
        </div>

        {/* Hero Typography */}
        <h1 className="text-5xl md:text-7xl font-bold tracking-tighter text-white mb-6 leading-tight">
          Analyze GitHub Projects <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-b from-white to-zinc-500">
            Like a Senior Engineer.
          </span>
        </h1>

        <p className="text-lg md:text-xl text-zinc-400 mb-12 max-w-2xl mx-auto font-light leading-relaxed">
          Get architecture insights, technology detection, project scoring, resume-ready achievements, and improvement recommendations.
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
            onClick={handleAnalyzeClick}
            disabled={!projectType || !repoUrl}
          />
        </div>

        {/* Conditional Layout Rendering */}
        <AnimatePresence mode="wait">
          {showPlaceholder ? (
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
                    <div className="flex items-center gap-2 mt-2">
                      {!isAuthenticated && (
                        <button
                          onClick={() => setIsAuthModalOpen(true)}
                          className="flex items-center gap-1.5 px-3 py-1.5 bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 rounded-lg text-[12px] font-medium transition-colors shrink-0"
                        >
                          Save Analysis
                        </button>
                      )}
                      <button 
                        onClick={handleDownloadPdf}
                        disabled={isDownloading}
                        className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 rounded-lg text-[12px] font-medium transition-colors disabled:opacity-50 shrink-0"
                      >
                        {isDownloading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Download className="w-3.5 h-3.5" />}
                        {downloadStatus === "Download PDF" ? "Download" : downloadStatus}
                      </button>
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

      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onGuestContinue={handleGuestContinue}
        hideGuest={false}
      />
    </div>
  );
}
