import { motion, AnimatePresence } from 'framer-motion';
import { GoogleLogin } from '@react-oauth/google';
import { Loader2, User, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useState } from 'react';

const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID?.trim();

export default function AuthModal({ isOpen, onClose, onGuestContinue }) {
  const { loginWithGoogle, authLoading, error } = useAuth();
  const [isGuestLoading, setIsGuestLoading] = useState(false);

  const handleSuccess = async (response) => {
    try {
      await loginWithGoogle(response.credential);
      onClose();
      if (onGuestContinue) onGuestContinue(); // Proceed with analysis after login
    } catch {
      // error handled in context
    }
  };

  const handleGuest = () => {
    setIsGuestLoading(true);
    setTimeout(() => {
      setIsGuestLoading(false);
      onClose();
      if (onGuestContinue) onGuestContinue();
    }, 400);
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        />

        {/* Modal Content */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 10 }}
          transition={{ duration: 0.2, ease: "easeOut" }}
          className="relative w-full max-w-[420px] bg-[#121214] border border-white/[0.08] rounded-2xl shadow-2xl shadow-black overflow-hidden"
        >
          {/* Subtle top highlight */}
          <div className="absolute top-0 inset-x-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />
          
          <div className="p-6">
            <div className="flex justify-between items-start mb-5">
              <div>
                <h2 className="text-[20px] font-semibold text-white mb-1.5 tracking-tight">Save Your Analysis?</h2>
                <p className="text-[14px] text-zinc-400 leading-relaxed">
                  Sign in to save analysis history and access your personal dashboard.
                </p>
              </div>
              <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors p-1">
                <X className="w-5 h-5" />
              </button>
            </div>

            {error && (
              <div className="mb-5 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-[13px]">
                {error}
              </div>
            )}

            <div className="space-y-4">
              {/* Google Option */}
              <div className="p-4 rounded-xl border border-white/10 bg-[#1A1A1C]">
                <div className="mb-4">
                  <h3 className="text-white text-[14px] font-medium mb-2">Continue with Google</h3>
                  <ul className="text-zinc-500 text-[13px] space-y-1.5 ml-4 list-disc marker:text-zinc-700">
                    <li>Save analysis history</li>
                    <li>Personal dashboard</li>
                    <li>Download reports</li>
                    <li>Access previous analyses</li>
                  </ul>
                </div>
                
                {!googleClientId ? (
                  <p className="text-[13px] text-amber-400/90 py-1">Not configured.</p>
                ) : authLoading ? (
                  <div className="flex items-center justify-center gap-2 text-zinc-400 h-[40px] w-full bg-black/40 rounded-lg border border-white/5">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="text-[13px] font-medium">Authenticating...</span>
                  </div>
                ) : (
                  <div className="w-full relative h-[40px] overflow-hidden rounded-lg border border-white/10 bg-black flex items-center justify-center">
                    <div className="w-full flex justify-center opacity-90 hover:opacity-100 transition-opacity">
                      <GoogleLogin
                        onSuccess={handleSuccess}
                        theme="filled_black"
                        size="medium"
                        text="continue_with"
                        shape="rectangular"
                        width="350"
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Guest Option */}
              <div className="p-4 rounded-xl border border-white/[0.04] bg-white/[0.02]">
                <div className="mb-4">
                  <h3 className="text-white text-[14px] font-medium mb-2">Continue as Guest</h3>
                  <ul className="text-zinc-500 text-[13px] space-y-1.5 ml-4 list-disc marker:text-zinc-700">
                    <li>Instant analysis</li>
                    <li>No account required</li>
                  </ul>
                </div>
                
                <button 
                  onClick={handleGuest}
                  disabled={isGuestLoading || authLoading}
                  className="w-full h-[40px] flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 text-white text-[13px] font-medium rounded-lg border border-white/10 transition-colors disabled:opacity-50"
                >
                  {isGuestLoading ? (
                    <Loader2 className="w-4 h-4 animate-spin text-zinc-400" />
                  ) : (
                    <>
                      <User className="w-4 h-4 text-zinc-400" />
                      Continue as Guest
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
