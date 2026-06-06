import { Layers } from 'lucide-react';

export const PROJECT_TYPES = [
  'Web Application',
  'Machine Learning',
  'Data Science',
  'Mobile App',
  'Backend API',
];

export default function ProjectTypeSelect({ value, onChange, disabled = false }) {
  return (
    <div className="w-full max-w-xl mx-auto relative group mb-4">
      <div className="absolute inset-0 bg-gradient-to-r from-zinc-800 to-zinc-800 rounded-xl blur opacity-25 group-hover:opacity-50 transition duration-500" />

      <div className="relative flex items-center bg-[#0a0a0a] premium-border rounded-xl px-4 py-3.5 transition-all focus-within:ring-2 focus-within:ring-zinc-600 focus-within:border-transparent">
        <Layers className="w-5 h-5 text-zinc-500 mr-3 shrink-0" />
        <select
          required
          value={value}
          onChange={onChange}
          disabled={disabled}
          className="w-full bg-transparent text-zinc-100 outline-none text-base appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <option value="" disabled className="bg-zinc-900 text-zinc-500">
            Select project type
          </option>
          {PROJECT_TYPES.map((type) => (
            <option key={type} value={type} className="bg-zinc-900 text-zinc-100">
              {type}
            </option>
          ))}
        </select>
        <svg
          className="w-4 h-4 text-zinc-500 shrink-0 pointer-events-none"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>
  );
}
