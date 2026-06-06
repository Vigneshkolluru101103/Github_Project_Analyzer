import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import { motion } from 'framer-motion';
import { Hexagon, Loader2, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

export default function LoginPage() {
  const navigate = useNavigate();
  const { isAuthenticated, authLoading, error, loginWithGoogle, setError } = useAuth();

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleSuccess = async (response) => {
    try {
      await loginWithGoogle(response.credential);
      navigate('/', { replace: true });
    } catch {
      // error set in context
    }
  };

  const handleError = () => {
    setError('Login failed. Please try again.');
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-6 relative overflow-hidden">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="w-full max-w-md relative z-10"
      >
        <div className="premium-glass rounded-3xl p-10 text-center">
          {/* Logo */}
          <div className="flex items-center justify-center gap-2 mb-8">
            <Hexagon className="w-8 h-8 text-emerald-400" />
            <span className="text-xl font-semibold tracking-tight text-zinc-100">
              ProjectReviewer
            </span>
          </div>

          <h1 className="text-2xl font-bold text-white mb-2 tracking-tight">
            Welcome back
          </h1>
          <p className="text-zinc-400 text-sm leading-relaxed mb-8 font-light">
            Sign in to save analysis history and access personalized reports.
          </p>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 flex items-start gap-2 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm text-left"
            >
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{error}</span>
            </motion.div>
          )}

          <div className="flex flex-col items-center gap-4">
            {!googleClientId ? (
              <p className="text-sm text-amber-400/90">
                Google sign-in is not configured. Set VITE_GOOGLE_CLIENT_ID in frontend/.env
              </p>
            ) : authLoading ? (
              <div className="flex items-center gap-2 text-zinc-400 py-3">
                <Loader2 className="w-5 h-5 animate-spin" />
                <span className="text-sm">Authenticating...</span>
              </div>
            ) : (
              <div className="w-full flex justify-center [&>div]:!w-full [&_iframe]:!mx-auto">
                <GoogleLogin
                  onSuccess={handleSuccess}
                  onError={handleError}
                  theme="filled_black"
                  size="large"
                  text="continue_with"
                  shape="pill"
                  width="320"
                />
              </div>
            )}
          </div>

          <p className="mt-8 text-xs text-zinc-600 leading-relaxed">
            By signing in, you agree to our terms of service and privacy policy.
          </p>
        </div>

        <p className="text-center text-zinc-600 text-xs mt-6">
          Analyze GitHub repos like a senior engineer.
        </p>
      </motion.div>
    </div>
  );
}
