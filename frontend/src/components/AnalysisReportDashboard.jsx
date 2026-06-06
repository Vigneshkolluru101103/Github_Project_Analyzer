import { motion } from 'framer-motion';
import {
  BarChart3, CheckCircle2, AlertCircle, Lightbulb,
  TrendingUp, Target, Sparkles, Layers,
} from 'lucide-react';

const MATURITY_STYLES = {
  Beginner: 'text-red-400 bg-red-500/10 border-red-500/25',
  Intermediate: 'text-amber-400 bg-amber-500/10 border-amber-500/25',
  Advanced: 'text-blue-400 bg-blue-500/10 border-blue-500/25',
  'Production Ready': 'text-emerald-400 bg-emerald-500/10 border-emerald-500/25',
};

const IMPACT_STYLES = {
  High: 'text-red-400 bg-red-500/10 border-red-500/20',
  Medium: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  Low: 'text-zinc-400 bg-zinc-500/10 border-zinc-500/20',
};

function getScoreColor(score) {
  if (score >= 86) return { text: 'text-emerald-400', bar: 'bg-emerald-500', glow: 'bg-emerald-500/15' };
  if (score >= 61) return { text: 'text-blue-400', bar: 'bg-blue-500', glow: 'bg-blue-500/15' };
  if (score >= 31) return { text: 'text-amber-400', bar: 'bg-amber-500', glow: 'bg-amber-500/15' };
  return { text: 'text-red-400', bar: 'bg-red-500', glow: 'bg-red-500/15' };
}

export default function AnalysisReportDashboard({ evaluation, recommendations = [], projectType }) {
  if (!evaluation || typeof evaluation.score !== 'number') return null;

  const {
    score,
    maturity = 'Beginner',
    potential_score = score,
    project_type: evalProjectType,
    strengths = [],
    missing = [],
  } = evaluation;

  const displayProjectType = projectType || evalProjectType;

  const colors = getScoreColor(score);
  const maturityStyle = MATURITY_STYLES[maturity] || MATURITY_STYLES.Beginner;
  const scoreGain = potential_score - score;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.55, ease: 'easeOut' }}
      className="mb-8 rounded-2xl bg-black/50 border border-zinc-800/80 overflow-hidden relative"
    >
      <div className={`absolute top-0 right-0 w-64 h-64 ${colors.glow} blur-3xl rounded-full pointer-events-none`} />

      {/* Dashboard header */}
      <div className="px-6 pt-6 pb-4 border-b border-zinc-800/60 relative z-10">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-zinc-800/60 premium-border flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-zinc-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-zinc-100 tracking-tight">Analysis Report</h3>
              <p className="text-xs text-zinc-500 font-light">Project evaluation dashboard</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3">
            {displayProjectType && (
              <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border text-indigo-400 bg-indigo-500/10 border-indigo-500/25">
                <Layers className="w-3.5 h-3.5" />
                {displayProjectType}
              </span>
            )}
            <span className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border ${maturityStyle}`}>
              <Sparkles className="w-3.5 h-3.5" />
              {maturity}
            </span>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6 relative z-10">
        {/* Scores row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {displayProjectType && (
            <div className="p-4 rounded-xl bg-indigo-500/[0.04] border border-indigo-500/20">
              <p className="text-[11px] font-medium text-zinc-500 uppercase tracking-wider mb-2">Project Type</p>
              <p className="text-lg font-bold text-indigo-400">{displayProjectType}</p>
            </div>
          )}
          <div className="p-4 rounded-xl bg-zinc-900/40 border border-zinc-800/60">
            <p className="text-[11px] font-medium text-zinc-500 uppercase tracking-wider mb-2">Project Maturity</p>
            <p className={`text-xl font-bold ${maturityStyle.split(' ')[0]}`}>{maturity}</p>
          </div>

          <div className="p-4 rounded-xl bg-zinc-900/40 border border-zinc-800/60">
            <p className="text-[11px] font-medium text-zinc-500 uppercase tracking-wider mb-2">Current Score</p>
            <p className="flex items-baseline gap-1">
              <span className={`text-3xl font-bold tracking-tighter ${colors.text}`}>{score}</span>
              <span className="text-zinc-500 text-sm font-medium">/ 100</span>
            </p>
            <div className="mt-3 h-1.5 w-full rounded-full bg-zinc-800/80 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${score}%` }}
                transition={{ duration: 0.9, ease: 'easeOut', delay: 0.15 }}
                className={`h-full rounded-full ${colors.bar}`}
              />
            </div>
          </div>

          <div className="p-4 rounded-xl bg-emerald-500/[0.04] border border-emerald-500/20">
            <p className="text-[11px] font-medium text-zinc-500 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Target className="w-3.5 h-3.5 text-emerald-400" />
              Estimated Future Score
            </p>
            <p className="flex items-baseline gap-1">
              <span className="text-3xl font-bold tracking-tighter text-emerald-400">{potential_score}</span>
              <span className="text-zinc-500 text-sm font-medium">/ 100</span>
            </p>
            {scoreGain > 0 && (
              <p className="mt-2 text-xs text-emerald-400/80 flex items-center gap-1">
                <TrendingUp className="w-3.5 h-3.5" />
                +{scoreGain} pts if all gaps are addressed
              </p>
            )}
          </div>
        </div>

        {/* Strengths & missing */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-emerald-500/[0.03] border border-emerald-500/15">
            <div className="flex items-center gap-2 mb-3">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <p className="text-xs font-medium text-zinc-400 uppercase tracking-wider">Strengths</p>
            </div>
            {strengths.length > 0 ? (
              <ul className="space-y-2">
                {strengths.map((item) => (
                  <li key={item} className="flex items-center gap-2 text-sm text-zinc-300">
                    <span className="text-emerald-400">✓</span>
                    {item}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-zinc-500 font-light">No features detected yet.</p>
            )}
          </div>

          <div className="p-4 rounded-xl bg-zinc-900/30 border border-zinc-800/60">
            <div className="flex items-center gap-2 mb-3">
              <AlertCircle className="w-4 h-4 text-zinc-500" />
              <p className="text-xs font-medium text-zinc-400 uppercase tracking-wider">Missing Features</p>
            </div>
            {missing.length > 0 ? (
              <ul className="space-y-2">
                {missing.map((item) => (
                  <li key={item} className="flex items-center gap-2 text-sm text-zinc-500">
                    <span className="text-zinc-600">✗</span>
                    {item}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-sm text-emerald-400/80 font-light">All features implemented!</p>
            )}
          </div>
        </div>

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Lightbulb className="w-4 h-4 text-indigo-400" />
              <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider">
                Recommendations
              </p>
            </div>
            <div className="space-y-2">
              {recommendations.map((rec, idx) => {
                const impactStyle = IMPACT_STYLES[rec.impact] || IMPACT_STYLES.Low;
                return (
                  <motion.div
                    key={rec.title}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 + idx * 0.05 }}
                    className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 p-3.5 rounded-xl bg-zinc-900/30 border border-zinc-800/50 hover:border-zinc-700/50 transition-colors"
                  >
                    <p className="text-sm text-zinc-200">{rec.title}</p>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-medium border ${impactStyle}`}>
                        {rec.impact}
                      </span>
                      <span className="text-xs text-emerald-400 font-medium">+{rec.points} pts</span>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </motion.div>
  );
}
