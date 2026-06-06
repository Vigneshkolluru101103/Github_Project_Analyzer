import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';

export default function UserDropdown() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [open, setOpen] = useState(false);

  const handleLogout = () => {
    try {
      logout();
      setOpen(false);
      navigate('/');
      toast.success(
        <div className="flex flex-col">
          <span className="font-semibold text-white">Logged Out Successfully</span>
          <span className="text-zinc-400 text-sm">You have been signed out.</span>
        </div>
      );
    } catch (err) {
      toast.error(
        <div className="flex flex-col">
          <span className="font-semibold text-white">Logout Failed</span>
          <span className="text-zinc-400 text-sm">Please refresh and try again.</span>
        </div>
      );
    }
  };


  const ref = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (!user) {
    return null;
  }

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-1.5 py-1 rounded-full hover:bg-white/5 transition-colors border border-transparent hover:border-white/10"
      >
        <img
          src={user.picture}
          alt={user.name}
          className="w-9 h-9 rounded-full"
          referrerPolicy="no-referrer"
        />
        <span className="text-[14px] text-zinc-200 font-medium hidden sm:block max-w-[120px] truncate ml-1">
          {user.name}
        </span>
        <ChevronDown className={`w-3.5 h-3.5 text-zinc-500 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 8, scale: 0.96 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 mt-2 w-56 rounded-xl bg-[#1A1A1C] border border-white/[0.08] shadow-2xl overflow-hidden z-50"
          >
            <div className="p-1">
              <button onClick={() => { setOpen(false); navigate('/history'); }} className="w-full flex items-center px-3 py-2 text-[13px] font-medium text-zinc-300 hover:text-white hover:bg-white/5 rounded-md transition-colors">
                Analysis History
              </button>
            </div>

            <div className="p-1 border-t border-white/[0.04]">
              <button
                onClick={handleLogout}
                className="w-full flex items-center px-3 py-2 text-[13px] font-medium text-zinc-400 hover:text-red-400 hover:bg-red-500/10 rounded-md transition-colors"
              >
                Logout
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
