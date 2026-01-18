import axios from 'axios';

// Dynamically set API URL based on current hostname
const getAPIUrl = () => {
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  // If running on localhost/127.0.0.1, use localhost:8000
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8000/api';
  }
  
  // Otherwise use the current hostname with port 8000
  return `${protocol}//${hostname}:8000/api`;
};

const API_URL = getAPIUrl();

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/token/refresh/`, {
          refresh: refreshToken,
        });
        localStorage.setItem('access_token', response.data.access);
        api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
        return api(originalRequest);
      } catch (err) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(err);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
