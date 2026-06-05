import { Hexagon } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="w-full border-t border-zinc-800/50 bg-[#000000] py-16 px-6 relative z-10">
      {/* Ultra-subtle gradient top border */}
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-zinc-800/80 to-transparent"></div>
      
      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-12 md:gap-8">
        
        {/* Brand & Description (Left half) */}
        <div className="md:col-span-6 flex flex-col justify-between h-full">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Hexagon className="w-5 h-5 text-zinc-100" />
              <span className="text-[15px] font-semibold tracking-tight text-zinc-100">ProjectReviewer</span>
            </div>
            <p className="text-zinc-500 text-[13px] leading-relaxed font-light max-w-sm">
              Analyze GitHub repositories, evaluate project quality, detect implemented features, and provide actionable feedback for developers.
            </p>
          </div>
          
          <div className="text-zinc-600 text-[13px] font-light mt-12 md:mt-0">
            &copy; 2026 Vignesh Kolluru
          </div>
        </div>

        {/* Core Features */}
        <div className="md:col-span-3">
          <h3 className="text-zinc-100 text-[13px] font-medium mb-4">Core Features</h3>
          <ul className="space-y-3">
            <li className="text-zinc-500 text-[13px] font-light">Code Review</li>
            <li className="text-zinc-500 text-[13px] font-light">Project Scoring</li>
            <li className="text-zinc-500 text-[13px] font-light">Feature Detection</li>
            <li className="text-zinc-500 text-[13px] font-light">Improvement Suggestions</li>
          </ul>
        </div>

        {/* Built With */}
        <div className="md:col-span-3">
          <h3 className="text-zinc-100 text-[13px] font-medium mb-4">Built With</h3>
          <ul className="space-y-3">
            <li className="text-zinc-500 text-[13px] font-light">Python</li>
            <li className="text-zinc-500 text-[13px] font-light">FastAPI</li>
            <li className="text-zinc-500 text-[13px] font-light">React</li>
            <li className="text-zinc-500 text-[13px] font-light">GitHub API</li>
          </ul>
        </div>
        
      </div>
    </footer>
  );
}
