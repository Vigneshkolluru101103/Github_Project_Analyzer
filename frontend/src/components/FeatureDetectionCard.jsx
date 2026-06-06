import { motion } from 'framer-motion';
import { 
  Shield, Database, Globe, FlaskConical, 
  Box, GitBranch, KeyRound, Check, X 
} from 'lucide-react';

/**
 * Registry mapping backend feature keys to display metadata.
 * Add new features here as the backend evolves.
 */
const FEATURE_ORDER = [
  "authentication",
  "database",
  "api_layer",
  "testing",
  "docker",
  "cicd",
  "environment_variables",
];

const FEATURE_MAP = {
  authentication: {
    icon: Shield,
    label: "Authentication",
    desc: "JWT, OAuth, bcrypt, login routes",
  },
  database: {
    icon: Database,
    label: "Database",
    desc: "SQLAlchemy, Prisma, MongoDB, PostgreSQL",
  },
  api_layer: {
    icon: Globe,
    label: "API Layer",
    desc: "FastAPI, Express, Django REST routes",
  },
  testing: {
    icon: FlaskConical,
    label: "Testing",
    desc: "pytest, jest, vitest, test suites",
  },
  docker: {
    icon: Box,
    label: "Docker",
    desc: "Dockerfile & docker-compose",
  },
  cicd: {
    icon: GitBranch,
    label: "CI / CD",
    desc: "GitHub Actions workflows",
  },
  environment_variables: {
    icon: KeyRound,
    label: "Environment Variables",
    desc: ".env files & dotenv packages",
  },
};

export default function FeatureDetectionCard({ features }) {
  if (!features || Object.keys(features).length === 0) return null;

  const entries = FEATURE_ORDER
    .filter((key) => key in features)
    .map((key) => [key, features[key]]);
  const detectedCount = entries.filter(([, v]) => v).length;

  return (
    <div className="mb-8">
      {/* Section header */}
      <div className="flex items-center justify-between mb-4">
        <p className="text-xs font-medium text-zinc-500 uppercase tracking-wider">
          Feature Detection
        </p>
        <span className="text-xs font-medium text-zinc-500">
          <span className="text-emerald-400">{detectedCount}</span>
          <span className="mx-0.5">/</span>
          {entries.length} detected
        </span>
      </div>

      {/* Feature grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {entries.map(([key, detected], idx) => {
          const meta = FEATURE_MAP[key] || {
            icon: KeyRound,
            label: key.replace(/_/g, " "),
            desc: "",
          };
          const Icon = meta.icon;

          return (
            <motion.div
              key={key}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15 + idx * 0.06, ease: "easeOut" }}
              className={`
                group relative p-4 rounded-xl border transition-all duration-300 overflow-hidden
                ${detected
                  ? "bg-emerald-500/[0.04] border-emerald-500/20 hover:bg-emerald-500/[0.08] hover:border-emerald-500/30"
                  : "bg-zinc-900/20 border-zinc-800/40 hover:bg-zinc-900/40 hover:border-zinc-700/50"
                }
              `}
            >
              {/* Subtle corner glow for detected features */}
              {detected && (
                <div className="absolute -top-6 -right-6 w-16 h-16 bg-emerald-500/10 blur-2xl rounded-full pointer-events-none" />
              )}

              {/* Icon row */}
              <div className="flex items-center justify-between mb-3 relative z-10">
                <div
                  className={`
                    w-8 h-8 rounded-lg flex items-center justify-center transition-colors
                    ${detected
                      ? "bg-emerald-500/10 group-hover:bg-emerald-500/15"
                      : "bg-zinc-800/50 group-hover:bg-zinc-800/70"
                    }
                  `}
                >
                  <Icon
                    className={`w-4 h-4 transition-colors ${
                      detected ? "text-emerald-400" : "text-zinc-600"
                    }`}
                  />
                </div>

                {/* Status indicator */}
                <div
                  className={`
                    w-5 h-5 rounded-full flex items-center justify-center
                    ${detected
                      ? "bg-emerald-500/15 text-emerald-400"
                      : "bg-zinc-800/60 text-zinc-600"
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

              {/* Label & description */}
              <p
                className={`text-sm font-medium relative z-10 transition-colors ${
                  detected ? "text-zinc-200" : "text-zinc-500"
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
