import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common.Authorization = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common.Authorization;
  }
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const isGoogleLogin = error.config?.url?.includes('/auth/google');
    if (error.response?.status === 401 && !isGoogleLogin) {
      localStorage.removeItem('gpa_access_token');
      localStorage.removeItem('gpa_user');
      delete api.defaults.headers.common.Authorization;
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  },
);

export const loginWithGoogle = async (credential) => {
  const response = await api.post('/auth/google', { credential });
  return response.data;
};

export const fetchCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const analyzeRepository = async (repoUrl, projectType) => {
  const response = await api.post('/analyze', {
    repo_url: repoUrl,
    project_type: projectType,
  });
  return response.data;
};

export const downloadSavedReportPdf = async (id) => {
  const response = await api.get(`/analysis/${id}/pdf`, {
    responseType: 'blob',
  });
  return response;
};

export const downloadRawReportPdf = async (reportData) => {
  const response = await api.post('/analysis/pdf/raw', reportData, {
    responseType: 'blob',
  });
  return response;
};

export default api;
