import { motion } from 'framer-motion';
import { BarChart3, CheckCircle2, AlertCircle } from 'lucide-react';

function getScoreColor(score) {
  if (score >= 71) return { text: 'text-emerald-400', bar: 'bg-emerald-500', glow: 'bg-emerald-500/20' };
  if (score >= 41) return { text: 'text-amber-400', bar: 'bg-amber-500', glow: 'bg-amber-500/20' };
  return { text: 'text-red-400', bar: 'bg-red-500', glow: 'bg-red-500/20' };
}

function getScoreLabel(score) {
  if (score >= 81) return 'Excellent';
  if (score >= 61) return 'Good';
  if (score >= 41) return 'Fair';
  if (score >= 21) return 'Needs Work';
  return 'Early Stage';
}

export default function ProjectScoreCard({ evaluation }) {
  if (!evaluation || typeof evaluation.score !== 'number') return null;

  const { score, strengths = [], missing = [] } = evaluation;
  const colors = getScoreColor(score);
  const label = getScoreLabel(score);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="mb-8 p-6 rounded-2xl bg-black/40 border border-zinc-800/80 relative overflow-hidden"
    >
      <div className={`absolute -top-12 -right-12 w-40 h-40 ${colors.glow} blur-3xl rounded-full pointer-events-none`} />

      {/* Score header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6 relative z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-zinc-800/60 premium-border flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-zinc-400" />
          </div>
          <div>
            <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Project Score</p>
            <p className="text-sm text-zinc-400 font-light">{label} engineering maturity</p>
          </div>
        </div>

        <div className="flex items-baseline gap-1">
          <span className={`text-5xl font-bold tracking-tighter ${colors.text}`}>
            {score}
          </span>
          <span className="text-zinc-500 text-lg font-medium">/ 100</span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="mb-6 relative z-10">
        <div className="h-2.5 w-full rounded-full bg-zinc-800/80 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${score}%` }}
            transition={{ duration: 0.9, ease: 'easeOut', delay: 0.2 }}
            className={`h-full rounded-full ${colors.bar} shadow-[0_0_12px_rgba(16,185,129,0.3)]`}
          />
        </div>
      </div>

      {/* Strengths & missing */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 relative z-10">
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
            <p className="text-xs font-medium text-zinc-400 uppercase tracking-wider">Missing</p>
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
    </motion.div>
  );
}
