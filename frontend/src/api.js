import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Base URL for all requests
});

// Request Interceptor: Add the auth token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;