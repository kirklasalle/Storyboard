/**
 * Centralized API base URL.
 * Set VITE_API_URL in your .env file to override for staging/production.
 */
export const API_BASE = (import.meta.env.VITE_API_URL as string) || 'http://127.0.0.1:8000';
