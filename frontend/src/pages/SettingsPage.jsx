import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import { LogOut, User, Mail, Shield } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate('/', { replace: true });
    }
  }, [user, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/', { replace: true });
  };

  if (!user) return null;

  return (
    <div className="min-h-screen flex flex-col pt-32 px-6 bg-[#0A0A0B] overflow-x-hidden">
      <Navbar />
      <div className="w-full max-w-2xl mx-auto relative z-10 pb-20">
        <h1 className="text-3xl font-bold text-white mb-8 tracking-tight">Settings</h1>

        <div className="bg-[#121214] border border-white/[0.08] rounded-2xl overflow-hidden shadow-2xl shadow-black/50">
          <div className="p-8 border-b border-white/[0.04]">
            <h2 className="text-lg font-medium text-white mb-6">Profile Information</h2>
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
              <img 
                src={user.picture} 
                alt={user.name} 
                className="w-20 h-20 rounded-full border border-white/10"
                referrerPolicy="no-referrer"
              />
              <div className="flex-1 w-full space-y-4">
                <div>
                  <label className="text-[13px] text-zinc-500 font-medium mb-1 block">Name</label>
                  <div className="flex items-center gap-3 bg-black/40 border border-white/[0.06] rounded-xl px-4 py-2.5">
                    <User className="w-4 h-4 text-zinc-400" />
                    <span className="text-white text-[14px]">{user.name}</span>
                  </div>
                </div>
                <div>
                  <label className="text-[13px] text-zinc-500 font-medium mb-1 block">Email</label>
                  <div className="flex items-center gap-3 bg-black/40 border border-white/[0.06] rounded-xl px-4 py-2.5">
                    <Mail className="w-4 h-4 text-zinc-400" />
                    <span className="text-white text-[14px]">{user.email}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="p-8 border-b border-white/[0.04]">
            <h2 className="text-lg font-medium text-white mb-4">Account Security</h2>
            <div className="flex items-start gap-4">
              <div className="p-2.5 bg-emerald-500/10 rounded-xl border border-emerald-500/20 shrink-0">
                <Shield className="w-5 h-5 text-emerald-400" />
              </div>
              <div>
                <p className="text-white text-[14px] font-medium mb-1">Google Authentication Active</p>
                <p className="text-zinc-400 text-[13px] leading-relaxed max-w-md">
                  Your account is securely linked to your Google identity. Passwords are not required.
                </p>
              </div>
            </div>
          </div>

          <div className="p-8 bg-black/20">
            <h2 className="text-lg font-medium text-red-400 mb-4">Danger Zone</h2>
            <button 
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2.5 bg-red-500/10 hover:bg-red-500/20 border border-red-500/20 text-red-400 text-[14px] font-medium rounded-xl transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Sign out of ProjectReviewer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
