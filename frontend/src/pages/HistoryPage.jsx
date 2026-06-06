import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import { Search, History, ArrowRight, Trash2, Loader2, FolderTree } from 'lucide-react';
import api from '../services/api';

export default function HistoryPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/', { replace: true });
      return;
    }

    const fetchHistory = async () => {
      try {
        const { data } = await api.get('/history');
        setHistory(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [user, navigate]);

  const handleDelete = (id) => {
    setHistory(history.filter(item => item.id !== id));
  };

  const filteredHistory = history.filter(item => 
    item.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
    item.project_type.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (!user) return null;

  return (
    <div className="min-h-screen flex flex-col pt-32 px-6 bg-[#0A0A0B] overflow-x-hidden">
      <Navbar />
      
      <div className="w-full max-w-4xl mx-auto relative z-10 pb-20">
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <History className="w-8 h-8 text-emerald-400" />
            Analysis History
          </h1>
          
          <div className="relative w-full md:w-64">
            <Search className="w-4 h-4 text-zinc-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input 
              type="text" 
              placeholder="Search repositories..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-[#121214] border border-white/10 rounded-xl py-2 pl-9 pr-4 text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-white/20 transition-colors"
            />
          </div>
        </div>

        <div className="bg-[#121214] border border-white/[0.08] rounded-2xl overflow-hidden shadow-2xl shadow-black/50">
          {loading ? (
            <div className="p-12 flex flex-col items-center justify-center text-zinc-500">
              <Loader2 className="w-8 h-8 animate-spin mb-4 text-emerald-400" />
              <p>Loading your history...</p>
            </div>
          ) : filteredHistory.length === 0 ? (
            <div className="p-12 flex flex-col items-center justify-center text-zinc-500">
              <FolderTree className="w-12 h-12 mb-4 opacity-20" />
              <p className="text-lg font-medium text-zinc-400 mb-1">No analyses found</p>
              <p className="text-sm">Try adjusting your search or analyzing a new repository.</p>
            </div>
          ) : (
            <div className="divide-y divide-white/[0.04]">
              {filteredHistory.map((item) => (
                <div key={item.id} className="p-5 hover:bg-white/[0.02] transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-4 group">
                  <div>
                    <h3 className="text-lg font-medium text-white mb-1.5">{item.name}</h3>
                    <div className="flex flex-wrap items-center gap-3 text-xs text-zinc-500">
                      <span className="px-2 py-0.5 rounded-full bg-white/5 border border-white/10 text-zinc-300">
                        {item.project_type}
                      </span>
                      <span>{item.date}</span>
                      <span className="text-emerald-400 font-medium bg-emerald-400/10 px-2 py-0.5 rounded-full">Score: {item.score}/100</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2 opacity-100 sm:opacity-0 group-hover:opacity-100 transition-opacity">
                    <button 
                      onClick={() => navigate(`/report/${item.id}`)} 
                      className="px-3 py-1.5 bg-white/10 hover:bg-white/15 text-white text-xs font-medium rounded-lg transition-colors flex items-center gap-1.5"
                    >
                      View Report
                      <ArrowRight className="w-3 h-3" />
                    </button>
                    <button 
                      onClick={() => handleDelete(item.id)}
                      className="p-1.5 text-zinc-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                      title="Delete analysis"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
