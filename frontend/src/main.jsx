import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { GoogleOAuthProvider } from '@react-oauth/google';
import './index.css';
import App from './App.jsx';

const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID?.trim();

if (!googleClientId) {
  console.warn('VITE_GOOGLE_CLIENT_ID is not set. Google login will not work.');
} else if (import.meta.env.DEV) {
  console.info('[auth] VITE_GOOGLE_CLIENT_ID loaded:', googleClientId);
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <GoogleOAuthProvider clientId={googleClientId || ''}>
      <App />
    </GoogleOAuthProvider>
  </StrictMode>,
);
