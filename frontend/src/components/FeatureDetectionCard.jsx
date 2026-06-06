import { motion } from 'framer-motion';
import {
  Shield, Database, Globe, FlaskConical, KeyRound, Check, X,
  Smartphone, HardDrive, FileText, Table2, Brain, BarChart2,
  BookOpen, LineChart, FileBarChart, Layout, Server, FileSearch,
} from 'lucide-react';

const CAPABILITY_META = {
  frontend_framework: { icon: Layout, desc: 'React, Vue, Angular, Svelte, Next.js' },
  backend_framework: { icon: Server, desc: 'FastAPI, Flask, Django, Express' },
  database: { icon: Database, desc: 'PostgreSQL, MySQL, MongoDB, Firebase' },
  authentication: { icon: Shield, desc: 'JWT, OAuth, Clerk, Auth0' },
  testing: { icon: FlaskConical, desc: 'Jest, Cypress, Playwright, Pytest' },
  api_documentation: { icon: FileSearch, desc: 'Swagger, OpenAPI, ReDoc' },
  mobile_framework: { icon: Smartphone, desc: 'Flutter, React Native, Android, iOS' },
  storage: { icon: HardDrive, desc: 'SQLite, Hive, SharedPreferences, Room' },
  api_integration: { icon: Globe, desc: 'REST API, GraphQL clients' },
  ml_framework: { icon: Brain, desc: 'TensorFlow, PyTorch, Scikit-Learn' },
  dataset: { icon: Table2, desc: 'CSV, datasets, data folders' },
  model: { icon: Brain, desc: 'Trained model artifacts' },
  evaluation: { icon: BarChart2, desc: 'Accuracy, F1, confusion matrix' },
  documentation: { icon: BookOpen, desc: 'README, project docs' },
  data_processing: { icon: Table2, desc: 'Pandas, NumPy, SciPy' },
  visualization: { icon: LineChart, desc: 'Matplotlib, Seaborn, Plotly' },
  eda: { icon: FileText, desc: 'Jupyter notebooks, exploratory analysis' },
};

const ORDER_BY_TYPE = {
  'Web Application': [
    'frontend_framework', 'backend_framework', 'database', 'authentication', 'testing',
  ],
  'Backend API': [
    'backend_framework', 'database', 'authentication', 'api_documentation', 'testing',
  ],
  'Mobile App': [
    'mobile_framework', 'authentication', 'storage', 'api_integration', 'testing',
  ],
  'Machine Learning': [
    'ml_framework', 'dataset', 'model', 'evaluation', 'documentation',
  ],
  'Data Science': [
    'data_processing', 'visualization', 'dataset', 'eda', 'documentation',
  ],
};

function normalizeCapabilities(capabilities) {
  if (!capabilities) return [];

  const order = ORDER_BY_TYPE[capabilities.projectType] || Object.keys(capabilities.data || capabilities);

  const data = capabilities.data || capabilities;
  const keys = Array.isArray(order) ? order : Object.keys(data);

  return keys
    .filter((key) => data[key])
    .map((key) => {
      const entry = data[key];
      if (typeof entry === 'object' && entry !== null && 'detected' in entry) {
        return [key, entry.detected, entry.label, entry.matched || [], entry.evidence || []];
      }
      return [key, Boolean(entry), key.replace(/_/g, ' '), [], []];
    });
}

export default function FeatureDetectionCard({ features, capabilities, projectType }) {
  const source = capabilities || features;
  if (!source || Object.keys(source).length === 0) return null;

  const entries = normalizeCapabilities({ data: source, projectType });
  const detectedCount = entries.filter(([, detected]) => detected).length;

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider">
          {projectType ? `${projectType} Capabilities` : 'Capability Detection'}
        </p>
        <span className="text-xs font-medium text-zinc-500">
          <span className="text-emerald-400">{detectedCount}</span>
          <span className="mx-0.5">/</span>
          {entries.length} present
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {entries.map(([key, detected, label, matched, evidenceList], idx) => {
          const meta = CAPABILITY_META[key] || { icon: KeyRound, desc: '' };
          const Icon = meta.icon;
          const displayLabel = label || key.replace(/_/g, ' ');

          return (
            <motion.div
              key={key}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 + idx * 0.06, ease: 'easeOut' }}
              className={`
                group relative p-4 rounded-xl border transition-all duration-300 overflow-hidden
                ${detected
                  ? 'bg-emerald-500/[0.04] border-emerald-500/20 hover:bg-emerald-500/[0.08] hover:border-emerald-500/30'
                  : 'bg-zinc-900/20 border-zinc-800/40 hover:bg-zinc-900/40 hover:border-zinc-700/50'
                }
              `}
            >
              {detected && (
                <div className="absolute -top-6 -right-6 w-16 h-16 bg-emerald-500/10 blur-2xl rounded-full pointer-events-none" />
              )}

              <div className="flex items-center justify-between mb-3 relative z-10">
                <div
                  className={`
                    w-8 h-8 rounded-lg flex items-center justify-center transition-colors
                    ${detected
                      ? 'bg-emerald-500/10 group-hover:bg-emerald-500/15'
                      : 'bg-zinc-800/50 group-hover:bg-zinc-800/70'
                    }
                  `}
                >
                  <Icon className={`w-4 h-4 ${detected ? 'text-emerald-400' : 'text-zinc-600'}`} />
                </div>
                <div
                  className={`
                    w-5 h-5 rounded-full flex items-center justify-center
                    ${detected
                      ? 'bg-emerald-500/15 text-emerald-400'
                      : 'bg-zinc-800/60 text-zinc-600'
                    }
                  `}
                >
                  {detected ? (
                    <Check className="w-3 h-3" strokeWidth={3} />
                  ) : (
                    <X className="w-3 h-3" strokeWidth={2.5} />
                  )}
                </div>
              </div>

              <p className={`text-sm font-medium relative z-10 ${detected ? 'text-zinc-200' : 'text-zinc-500'}`}>
                {displayLabel}
              </p>
              {detected && evidenceList.length > 0 ? (
                <div className="mt-2 relative z-10">
                  <p className="text-[10px] text-zinc-500 uppercase tracking-wider mb-1">Evidence</p>
                  <ul className="space-y-0.5">
                    {evidenceList.slice(0, 4).map((ev, i) => (
                      <li key={i} className="text-[11px] text-emerald-400/80 font-mono truncate">
                        • {ev.value}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : detected && matched.length > 0 ? (
                <p className="text-[11px] text-emerald-400/70 mt-1 relative z-10">
                  via {matched.slice(0, 2).join(', ')}
                </p>
              ) : (
                <p className="text-[11px] text-zinc-600 mt-1 leading-relaxed relative z-10">
                  {meta.desc}
                </p>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
