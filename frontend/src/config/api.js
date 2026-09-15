// API base URLs. Override via frontend/.env (see .env.example) for
// non-local environments; falls back to local dev ports otherwise.
export const AUTH_API_BASE = import.meta.env.VITE_AUTH_API_URL || 'http://localhost:5000'
export const STRIPE_API_BASE = import.meta.env.VITE_STRIPE_API_URL || 'http://localhost:5001'
export const ANALYZE_API_BASE = import.meta.env.VITE_ANALYZE_API_URL || 'http://localhost:8000'
