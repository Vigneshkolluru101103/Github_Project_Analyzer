import { motion, AnimatePresence } from 'framer-motion';
import { GoogleLogin } from '@react-oauth/google';
import { Loader2, User, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useState } from 'react';

const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID?.trim();

export default function AuthModal({ isOpen, onClose, onGuestContinue, hideGuest }) {
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

          <div className="p-8">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-[22px] font-semibold text-white mb-2 tracking-tight">Sign in to Continue</h2>
                <p className="text-[14px] text-zinc-400 leading-relaxed pr-4">
                  Save your analysis history and access reports anytime.
                </p>
              </div>
              <button onClick={onClose} className="text-zinc-500 hover:text-white transition-colors p-1 -mr-2 -mt-2 rounded-lg hover:bg-white/5">
                <X className="w-5 h-5" />
              </button>
            </div>

            {error && (
              <div className="mb-6 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-[13px]">
                {error}
              </div>
            )}

            <div className="space-y-5">
              {/* Primary Action: Google */}
              {!googleClientId ? (
                <p className="text-[13px] text-amber-400/90 py-1 text-center">Google Client ID not configured.</p>
              ) : authLoading ? (
                <div className="flex items-center justify-center gap-2 text-zinc-400 h-[48px] w-full bg-[#18181B] rounded-xl border border-white/10">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="text-[14px] font-medium">Authenticating...</span>
                </div>
              ) : (
                <div className="relative w-full h-[48px] rounded-xl bg-white hover:bg-zinc-100 transition-colors flex items-center shadow-md overflow-hidden">
                  {/* Icon Container */}
                  <div className="absolute left-0 top-0 bottom-0 w-[48px] flex items-center justify-center pl-1 border-r border-zinc-200/50">
                    <svg width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.16v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.16C1.43 8.55 1 10.22 1 12s.43 3.45 1.16 4.93l3.68-2.84z" fill="#FBBC05"/>
                      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.16 7.07l3.68 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                    </svg>
                  </div>
                  
                  {/* Button Text */}
                  <div className="flex-1 text-center pr-[48px] font-semibold text-zinc-900 text-[14.5px]">
                    Continue with Google
                  </div>

                  {/* Invisible Overlay for Google Login */}
                  <div className="absolute inset-0 opacity-[0.01] z-10 flex items-center justify-center overflow-hidden cursor-pointer">
                    <div className="transform scale-[2.5]">
                      <GoogleLogin
                        onSuccess={handleSuccess}
                        theme="outline"
                        size="large"
                        text="continue_with"
                        shape="rectangular"
                      />
                    </div>
                  </div>
                </div>
              )}

              {!hideGuest && (
                <>
                  {/* Divider */}
                  <div className="flex items-center gap-4 my-2">
                    <div className="flex-1 h-[1px] bg-white/[0.06]" />
                    <span className="text-[11px] font-medium text-zinc-500 uppercase tracking-widest">OR</span>
                    <div className="flex-1 h-[1px] bg-white/[0.06]" />
                  </div>

                  {/* Secondary Action: Guest */}
                  <div>
                    <button
                      onClick={handleGuest}
                      disabled={isGuestLoading || authLoading}
                      className="w-full h-[44px] flex items-center justify-center gap-2 bg-transparent hover:bg-white/5 text-zinc-300 hover:text-white text-[14px] font-medium rounded-xl border border-zinc-800 hover:border-zinc-700 transition-all disabled:opacity-50"
                    >
                      {isGuestLoading ? (
                        <Loader2 className="w-4 h-4 animate-spin text-zinc-400" />
                      ) : (
                        <>
                          <User className="w-4 h-4" />
                          Continue as Guest
                        </>
                      )}
                    </button>
                    <p className="text-center text-[12px] text-zinc-500 mt-4">
                      Guest mode allows analysis without saving history.
                    </p>
                  </div>
                </>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
