import { motion } from 'framer-motion';

export default function ResultCardPlaceholder() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="w-full max-w-5xl mx-auto mt-16 premium-glass rounded-3xl p-10"
    >
      <div className="flex flex-col space-y-12">
        
        {/* Header Skeleton */}
        <div className="flex items-center space-x-6">
          <div className="w-16 h-16 rounded-2xl bg-zinc-800 premium-border shimmer"></div>
          <div className="space-y-3 flex-1">
            <div className="h-5 w-1/3 bg-zinc-800 rounded-md shimmer"></div>
            <div className="h-4 w-1/4 bg-zinc-800/50 rounded-md shimmer"></div>
          </div>
        </div>

        {/* Subtle Divider */}
        <div className="h-px w-full bg-gradient-to-r from-zinc-800/0 via-zinc-800 to-zinc-800/0"></div>
        
        {/* Metrics Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-32 rounded-2xl bg-zinc-800/30 premium-border p-5 flex flex-col justify-end">
               <div className="h-3 w-1/2 bg-zinc-700/50 rounded shimmer mb-3"></div>
               <div className="h-8 w-3/4 bg-zinc-700 rounded shimmer"></div>
            </div>
          ))}
        </div>

        {/* Content Area */}
        <div className="space-y-4 pt-4">
           <div className="h-4 w-full bg-zinc-800/60 rounded shimmer"></div>
           <div className="h-4 w-11/12 bg-zinc-800/60 rounded shimmer"></div>
           <div className="h-4 w-4/5 bg-zinc-800/60 rounded shimmer"></div>
        </div>

      </div>
    </motion.div>
  );
}
