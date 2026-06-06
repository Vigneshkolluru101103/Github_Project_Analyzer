import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { LogOut, ChevronDown, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { GoogleLogin } from '@react-oauth/google';

export default function UserDropdown() {
  const navigate = useNavigate();
  const { user, logout, loginWithGoogle, authLoading } = useAuth();
  const [open, setOpen] = useState(false);

  const handleLogout = () => {
    logout();
    setOpen(false);
  };

  const handleSuccess = async (response) => {
    try {
      await loginWithGoogle(response.credential);
    } catch {
      // Error is handled in AuthContext
    }
  };

  const handleError = () => {
    console.error('Google Login Failed');
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
    return (
      <div className="flex items-center">
        {authLoading ? (
          <div className="flex items-center gap-2 text-zinc-400 px-3 py-1.5 h-[34px] rounded-lg border border-white/5 bg-white/5">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span className="text-[13px] font-medium">Signing in...</span>
          </div>
        ) : (
          <div className="h-[36px] rounded-lg overflow-hidden border border-white/10 hover:border-white/20 transition-colors bg-[#131314] flex items-center justify-center">
            <div className="opacity-90 hover:opacity-100 transition-opacity">
              <GoogleLogin
                onSuccess={handleSuccess}
                onError={handleError}
                theme="filled_black"
                size="medium"
                text="continue_with"
                shape="rectangular"
              />
            </div>
          </div>
        )}
      </div>
    );
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
              <button onClick={() => { setOpen(false); navigate('/'); }} className="w-full flex items-center px-3 py-2 text-[13px] font-medium text-zinc-300 hover:text-white hover:bg-white/5 rounded-md transition-colors">
                Dashboard
              </button>
              <button onClick={() => { setOpen(false); navigate('/history'); }} className="w-full flex items-center px-3 py-2 text-[13px] font-medium text-zinc-300 hover:text-white hover:bg-white/5 rounded-md transition-colors">
                Analysis History
              </button>
              <button onClick={() => { setOpen(false); navigate('/settings'); }} className="w-full flex items-center px-3 py-2 text-[13px] font-medium text-zinc-300 hover:text-white hover:bg-white/5 rounded-md transition-colors">
                Settings
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
