import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

export default function CTASection() {
  return (
    <section className="w-full max-w-6xl mx-auto px-6 mb-24">
      <div className="relative rounded-3xl premium-glass p-12 md:p-20 text-center overflow-hidden group">
        {/* Animated Background Glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-violet-500/10 blur-[100px] rounded-full group-hover:bg-violet-500/20 transition-colors duration-700 pointer-events-none"></div>
        
        <div className="relative z-10">
          <h2 className="text-4xl md:text-5xl font-bold tracking-tighter text-white mb-6">
            Ready to elevate your portfolio?
          </h2>
          <p className="text-lg text-zinc-400 mb-10 max-w-xl mx-auto font-light leading-relaxed">
            Stop guessing what recruiters want. Get immediate, actionable feedback on your codebase and start building with confidence.
          </p>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="inline-flex items-center justify-center px-8 py-4 rounded-full bg-white text-black font-medium text-[15px] hover:bg-zinc-200 transition-colors shadow-[0_0_20px_rgba(255,255,255,0.1)]"
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          >
            Analyze Your First Repo
            <ArrowRight className="w-4 h-4 ml-2" />
          </motion.button>
        </div>
      </div>
    </section>
  );
}
