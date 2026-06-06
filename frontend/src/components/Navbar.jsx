import { Hexagon } from 'lucide-react';
import UserDropdown from './UserDropdown';

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-zinc-800/50 bg-black/60 backdrop-blur-xl">
      <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Hexagon className="w-5 h-5 text-emerald-400" />
          <span className="text-sm font-semibold tracking-tight text-zinc-100">
            ProjectReviewer
          </span>
        </div>
        <UserDropdown />
      </div>
    </nav>
  );
}
