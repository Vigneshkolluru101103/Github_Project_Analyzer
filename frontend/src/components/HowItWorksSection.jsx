import { motion } from 'framer-motion';
import { Link2, Cpu, ScanSearch, CheckCircle } from 'lucide-react';

export default function HowItWorksSection() {
  const steps = [
    {
      icon: Link2,
      title: "1. Paste GitHub URL",
      desc: "Provide the link to any public GitHub repository. No authentication required."
    },
    {
      icon: Cpu,
      title: "2. Analysis Begins",
      desc: "Our engine clones the repo and performs deep static analysis on the architecture."
    },
    {
      icon: ScanSearch,
      title: "3. Detect Tech & Features",
      desc: "We identify your stack, database schemas, API layers, and security practices."
    },
    {
      icon: CheckCircle,
      title: "4. Receive Actionable Feedback",
      desc: "Get a comprehensive score, strength/weakness breakdown, and resume bullets."
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15 }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } }
  };

  return (
    <section className="w-full max-w-5xl mx-auto px-6 mb-32 pt-16">
      <div className="text-center mb-16">
        <h2 className="text-3xl font-bold tracking-tighter text-zinc-100 mb-4">
          How It Works
        </h2>
        <p className="text-zinc-500 text-sm max-w-xl mx-auto font-light">
          A transparent, step-by-step process designed to evaluate your code just like a senior engineer during a technical review.
        </p>
      </div>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-50px" }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {steps.map((step, i) => (
          <motion.div 
            key={i} 
            variants={itemVariants}
            className="bg-[#0a0a0a] premium-border rounded-2xl p-6 relative overflow-hidden group hover:bg-zinc-900/40 transition-colors"
          >
            {/* Subtle glow on hover */}
            <div className="absolute -top-12 -right-12 w-32 h-32 bg-zinc-700/10 blur-3xl rounded-full group-hover:bg-zinc-600/20 transition-colors duration-500"></div>
            
            <div className="w-10 h-10 rounded-xl bg-zinc-900 premium-border flex items-center justify-center mb-5 relative z-10">
              <step.icon className="w-4 h-4 text-zinc-400" />
            </div>
            <h3 className="text-zinc-100 text-[14px] font-medium mb-2 relative z-10">{step.title}</h3>
            <p className="text-zinc-500 text-[13px] leading-relaxed font-light relative z-10">
              {step.desc}
            </p>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}
