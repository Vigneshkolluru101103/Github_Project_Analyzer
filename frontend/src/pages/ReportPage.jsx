import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import AnalysisReportDashboard from '../components/AnalysisReportDashboard';
import FeatureDetectionCard from '../components/FeatureDetectionCard';
import { FolderTree, Blocks, ArrowLeft, RefreshCw, Loader2, AlertCircle, Download } from 'lucide-react';
import api, { downloadSavedReportPdf } from '../services/api';
import { motion } from 'framer-motion';

export default function ReportPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isDownloading, setIsDownloading] = useState(false);

  useEffect(() => {
    if (!user) {
      navigate('/', { replace: true });
      return;
    }

    const fetchReport = async () => {
      try {
        const { data } = await api.get(`/analysis/${id}`);
        setResult(data);
      } catch (err) {
        console.error(err);
        setError(err.response?.data?.detail || "Failed to load report. It may have been deleted or you don't have access.");
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, [id, user, navigate]);

  const handleReanalyze = () => {
    // Navigate to root and pass repoUrl to be re-analyzed
    if (result && result.data) {
      // Use query param for the LandingPage to pick up
      navigate(`/?repoUrl=${encodeURIComponent(result.data.repo_url)}`);
    } else {
      navigate('/');
    }
  };

  const [downloadStatus, setDownloadStatus] = useState("Download PDF");

  const handleDownloadPdf = async () => {
    if (!result || !result.data) return;
    setIsDownloading(true);
    setDownloadStatus("Generating PDF...");
    console.log("Downloading PDF for analysis:", id);
    
    try {
      const response = await downloadSavedReportPdf(id);
      setDownloadStatus("Downloading...");
      
      // Create a blob URL and trigger download
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
      alert(errorMsg);
    } finally {
      setIsDownloading(false);
      setDownloadStatus("Download PDF");
    }
  };

  if (!user) return null;

  return (
    <div className="min-h-screen flex flex-col pt-24 px-6 bg-[#0A0A0B] overflow-x-hidden">
      <Navbar />

      <div className="w-full max-w-4xl mx-auto relative z-10 pb-20 mt-8">
        <div className="flex items-center justify-between mb-8">
          <button 
            onClick={() => navigate('/history')}
            className="flex items-center gap-2 text-zinc-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span className="text-[14px] font-medium">Back to History</span>
          </button>

          {result && !error && (
            <div className="flex items-center gap-3">
              <button 
                onClick={handleDownloadPdf}
                disabled={isDownloading}
                className="flex items-center gap-2 px-4 py-2 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 rounded-lg text-[13px] font-medium transition-colors disabled:opacity-50"
              >
                {isDownloading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Download className="w-4 h-4" />}
                {downloadStatus}
              </button>
              <button 
                onClick={handleReanalyze}
                className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg text-[13px] font-medium transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                Re-analyze Repository
              </button>
            </div>
          )}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-32 text-zinc-500">
            <Loader2 className="w-8 h-8 animate-spin" />
          </div>
        ) : error ? (
          <div className="p-8 bg-red-500/10 border border-red-500/50 rounded-2xl text-red-400 text-center">
            <AlertCircle className="w-12 h-12 mx-auto mb-4 opacity-80" />
            <h3 className="font-semibold text-lg mb-2">Error Loading Report</h3>
            <p className="text-red-300/80">{error}</p>
          </div>
        ) : result && result.data ? (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full"
          >
            <div className="p-8 bg-zinc-900/50 premium-border rounded-3xl text-left shadow-2xl backdrop-blur-xl">
              <div className="flex items-start justify-between border-b border-zinc-800/50 pb-6 mb-6">
                <div>
                  <h2 className="text-3xl font-bold text-white mb-2 flex items-center">
                    <FolderTree className="w-8 h-8 mr-3 text-emerald-400" />
                    {result.data.name}
                  </h2>
                  <p className="text-zinc-400 text-lg leading-relaxed max-w-2xl">
                    {result.data.description}
                  </p>
                </div>
              </div>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <div className="bg-black/40 p-4 rounded-2xl border border-zinc-800/80">
                  <p className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1">Project Type</p>
                  <p className="text-[17px] font-semibold text-zinc-200">{result.data.project_type}</p>
                </div>
                <div className="bg-black/40 p-4 rounded-2xl border border-zinc-800/80">
                  <p className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1">Primary Language</p>
                  <p className="text-[17px] font-semibold text-zinc-200">{result.data.language || 'N/A'}</p>
                </div>
                <div className="bg-black/40 p-4 rounded-2xl border border-zinc-800/80">
                  <p className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1">Stars</p>
                  <p className="text-[17px] font-semibold text-amber-400">{(result.data.stars || 0).toLocaleString()}</p>
                </div>
                <div className="bg-black/40 p-4 rounded-2xl border border-zinc-800/80">
                  <p className="text-xs text-zinc-500 font-medium uppercase tracking-wider mb-1">Analysis Date</p>
                  <p className="text-[16px] font-semibold text-emerald-400">
                    {result.data.analyzed_at ? new Date(result.data.analyzed_at).toLocaleDateString() : 'N/A'}
                  </p>
                </div>
              </div>

              <AnalysisReportDashboard
                evaluation={result.data.evaluation}
                recommendations={result.data.recommendations}
                projectType={result.data.project_type}
              />
              
              {result.data.technologies && result.data.technologies.length > 0 && (
                <div className="mb-8 mt-8">
                  <p className="text-xs font-medium text-zinc-500 mb-3 uppercase tracking-wider">Technology Stack</p>
                  <div className="flex flex-wrap gap-2">
                    {result.data.technologies.map((tech, idx) => (
                      <span key={idx} className="px-3 py-1.5 bg-zinc-800/50 border border-zinc-700/50 rounded-lg text-[13px] text-zinc-300 flex items-center shadow-sm">
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

              <div className="p-5 mt-8 bg-black/40 rounded-2xl border border-zinc-800/80 shadow-inner group transition-all hover:bg-black/60">
                <p className="text-xs font-medium text-zinc-500 mb-2 uppercase tracking-wider">Repository URL</p>
                <div className="flex items-center">
                  <a href={result.data.repo_url} target="_blank" rel="noreferrer" className="text-emerald-400 hover:text-emerald-300 transition-colors text-lg break-all">
                    {result.data.repo_url}
                  </a>
                </div>
              </div>
            </div>
          </motion.div>
        ) : null}
      </div>
    </div>
  );
}
