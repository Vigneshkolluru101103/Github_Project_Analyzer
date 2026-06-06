import axios from 'axios';

// Create an Axios instance pointing to our FastAPI backend
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeRepository = async (repoUrl, projectType) => {
  try {
    const response = await api.post('/analyze', {
      repo_url: repoUrl,
      project_type: projectType,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};
