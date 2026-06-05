import { motion } from 'framer-motion';
import { Sparkles, Loader2 } from 'lucide-react';

export default function AnalyzeButton({ isLoading, onClick }) {
  return (
    <motion.button
      whileHover={{ scale: isLoading ? 1 : 1.02 }}
      whileTap={{ scale: isLoading ? 1 : 0.98 }}
      onClick={onClick}
      disabled={isLoading}
      className={`relative w-full max-w-xl mx-auto mt-6 flex items-center justify-center py-3.5 px-6 rounded-xl font-medium text-[15px] transition-all duration-300
        ${isLoading 
          ? 'bg-zinc-800 text-zinc-400 cursor-not-allowed premium-border' 
          : 'bg-white text-black hover:bg-zinc-200 shadow-[0_0_20px_rgba(255,255,255,0.15)]'
        }`}
    >
      {isLoading ? (
        <>
          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
          Analyzing...
        </>
      ) : (
        <>
          <Sparkles className="w-4 h-4 mr-2" />
          Run Deep Analysis
        </>
      )}
    </motion.button>
  );
}
