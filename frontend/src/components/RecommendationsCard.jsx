import { motion } from 'framer-motion';
import { Lightbulb, TrendingUp } from 'lucide-react';

const IMPACT_STYLES = {
  High: 'text-red-400 bg-red-500/10 border-red-500/20',
  Medium: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  Low: 'text-zinc-400 bg-zinc-500/10 border-zinc-500/20',
};

export default function RecommendationsCard({ recommendations }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut', delay: 0.1 }}
      className="mb-8"
    >
      <div className="flex items-center gap-3 mb-4">
        <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center">
          <Lightbulb className="w-4 h-4 text-indigo-400" />
        </div>
        <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider">
          Recommended Improvements
        </p>
      </div>

      <div className="space-y-3">
        {recommendations.map((rec, idx) => {
          const impactStyle = IMPACT_STYLES[rec.impact] || IMPACT_STYLES.Low;

          return (
            <motion.div
              key={rec.title}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.15 + idx * 0.06, ease: 'easeOut' }}
              className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 p-4 rounded-xl bg-zinc-900/30 border border-zinc-800/60 hover:bg-zinc-900/50 hover:border-zinc-700/50 transition-all"
            >
              <p className="text-sm font-medium text-zinc-200">{rec.title}</p>

              <div className="flex items-center gap-3 shrink-0">
                <span className={`px-2.5 py-1 rounded-md text-[11px] font-medium border ${impactStyle}`}>
                  {rec.impact} Impact
                </span>
                <span className="flex items-center gap-1 text-xs text-emerald-400 font-medium">
                  <TrendingUp className="w-3.5 h-3.5" />
                  +{rec.points} pts
                </span>
              </div>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}
