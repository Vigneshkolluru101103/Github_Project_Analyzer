import { motion } from 'framer-motion';
import {
  Shield, Database, Globe, FlaskConical, Box, GitBranch, KeyRound,
  Check, X, Smartphone, HardDrive, FileText, Table2, Brain,
  BarChart2, BookOpen, Package, Rocket, LineChart, FileBarChart,
} from 'lucide-react';

const FEATURE_MAP = {
  authentication: { icon: Shield, label: 'Authentication', desc: 'JWT, OAuth, login flows' },
  database: { icon: Database, label: 'Database', desc: 'SQL, NoSQL, ORM integration' },
  api_layer: { icon: Globe, label: 'API Layer', desc: 'REST routes and endpoints' },
  testing: { icon: FlaskConical, label: 'Testing', desc: 'Unit and integration tests' },
  docker: { icon: Box, label: 'Docker', desc: 'Containerization setup' },
  cicd: { icon: GitBranch, label: 'CI/CD', desc: 'Automated pipelines' },
  environment_variables: { icon: KeyRound, label: 'Environment Variables', desc: '.env configuration' },
  api_integration: { icon: Globe, label: 'API Integration', desc: 'Backend API client calls' },
  local_storage: { icon: HardDrive, label: 'Local Storage', desc: 'On-device data persistence' },
  documentation: { icon: BookOpen, label: 'Documentation', desc: 'README and project docs' },
  dataset: { icon: Table2, label: 'Dataset', desc: 'Structured data files' },
  model_files: { icon: Brain, label: 'Model Files', desc: 'Trained model artifacts' },
  evaluation_metrics: { icon: BarChart2, label: 'Evaluation Metrics', desc: 'Model performance metrics' },
  requirements_file: { icon: Package, label: 'Requirements File', desc: 'Dependency management' },
  deployment: { icon: Rocket, label: 'Deployment', desc: 'Model serving infrastructure' },
  eda_notebook: { icon: FileText, label: 'EDA Notebook', desc: 'Exploratory analysis notebooks' },
  visualizations: { icon: LineChart, label: 'Visualizations', desc: 'Charts and plots' },
  insights_reports: { icon: FileBarChart, label: 'Insights/Reports', desc: 'Analysis findings' },
};

const FEATURE_ORDER_BY_TYPE = {
  'Web Application': [
    'authentication', 'database', 'api_layer', 'testing',
    'docker', 'cicd', 'environment_variables',
  ],
  'Backend API': [
    'api_layer', 'authentication', 'database', 'testing', 'docker', 'cicd',
  ],
  'Mobile App': [
    'authentication', 'api_integration', 'local_storage', 'database',
    'testing', 'cicd', 'documentation',
  ],
  'Machine Learning': [
    'dataset', 'model_files', 'evaluation_metrics',
    'documentation', 'requirements_file', 'deployment',
  ],
  'Data Science': [
    'dataset', 'eda_notebook', 'visualizations',
    'documentation', 'requirements_file', 'insights_reports',
  ],
};

export default function FeatureDetectionCard({ features, projectType }) {
  if (!features || Object.keys(features).length === 0) return null;

  const order = FEATURE_ORDER_BY_TYPE[projectType] || Object.keys(features);
  const entries = order
    .filter((key) => key in features)
    .map((key) => [key, features[key]]);

  const detectedCount = entries.filter(([, v]) => v).length;

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Smartphone className="w-4 h-4 text-zinc-500 hidden sm:block" />
          <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider">
            {projectType ? `${projectType} Features` : 'Feature Detection'}
          </p>
        </div>
        <span className="text-xs font-medium text-zinc-500">
          <span className="text-emerald-400">{detectedCount}</span>
          <span className="mx-0.5">/</span>
          {entries.length} detected
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {entries.map(([key, detected], idx) => {
          const meta = FEATURE_MAP[key] || {
            icon: KeyRound,
            label: key.replace(/_/g, ' '),
            desc: '',
          };
          const Icon = meta.icon;

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
                  <Icon
                    className={`w-4 h-4 transition-colors ${
                      detected ? 'text-emerald-400' : 'text-zinc-600'
                    }`}
                  />
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

              <p
                className={`text-sm font-medium relative z-10 transition-colors ${
                  detected ? 'text-zinc-200' : 'text-zinc-500'
                }`}
              >
                {meta.label}
              </p>
              <p className="text-[11px] text-zinc-600 mt-1 leading-relaxed relative z-10">
                {meta.desc}
              </p>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
