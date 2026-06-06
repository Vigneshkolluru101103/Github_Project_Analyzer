import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import toast from 'react-hot-toast';
import api, { setAuthToken } from '../services/api';

const AuthContext = createContext(null);

const TOKEN_KEY = 'gpa_access_token';
const USER_KEY = 'gpa_user';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authLoading, setAuthLoading] = useState(false);
  const [error, setError] = useState(null);

  const persistSession = useCallback((token, userData) => {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(userData));
    setAuthToken(token);
    setUser(userData);
  }, []);

  const clearSession = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    setAuthToken(null);
    setUser(null);
    setError(null);
  }, []);

  const restoreSession = useCallback(async () => {
    const token = localStorage.getItem(TOKEN_KEY);
    const savedUser = localStorage.getItem(USER_KEY);

    if (!token) {
      setLoading(false);
      return;
    }

    setAuthToken(token);

    try {
      const { data } = await api.get('/auth/me');
      persistSession(token, data);
    } catch {
      if (savedUser) {
        try {
          persistSession(token, JSON.parse(savedUser));
        } catch {
          clearSession();
        }
      } else {
        clearSession();
        setError('Session expired. Please sign in again.');
      }
    } finally {
      setLoading(false);
    }
  }, [clearSession, persistSession]);

  useEffect(() => {
    restoreSession();
  }, [restoreSession]);

  const loginWithGoogle = useCallback(async (credential) => {
    setAuthLoading(true);
    setError(null);

    try {
      const { data } = await api.post('/auth/google', { credential });
      persistSession(data.access_token, data.user);
      toast.success(
        <div className="flex flex-col">
          <span className="font-semibold text-white">Login Successful</span>
          <span className="text-zinc-400 text-sm">Welcome back!</span>
        </div>
      );
      return data.user;
    } catch (err) {
      const detail = err.response?.data?.detail;
      const message = (typeof detail === 'string' ? detail : null)
        || (Array.isArray(detail) ? detail.map((d) => d.msg).join(', ') : null)
        || (err.request ? 'Network error. Is the backend running?' : 'Login failed. Please try again.');
      setError(message);
      toast.error(
        <div className="flex flex-col">
          <span className="font-semibold text-white">Login Failed</span>
          <span className="text-zinc-400 text-sm">Please try again.</span>
        </div>
      );
      throw new Error(message);
    } finally {
      setAuthLoading(false);
    }
  }, [persistSession]);

  const logout = useCallback(() => {
    clearSession();
  }, [clearSession]);

  const value = useMemo(() => ({
    user,
    loading,
    authLoading,
    error,
    isAuthenticated: Boolean(user),
    loginWithGoogle,
    logout,
    setError,
  }), [user, loading, authLoading, error, loginWithGoogle, logout]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
