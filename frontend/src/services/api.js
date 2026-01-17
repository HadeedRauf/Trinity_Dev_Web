import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

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

// Authentication
export const login = async (username, password) => {
  const response = await api.post('/token/', { username, password });
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/register/', userData);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user_role');
  localStorage.removeItem('username');
};

// Products
export const getProducts = () => api.get('/products/');
export const getProduct = (id) => api.get(`/products/${id}/`);
export const createProduct = (data) => api.post('/products/', data);
export const updateProduct = (id, data) => api.put(`/products/${id}/`, data);
export const deleteProduct = (id) => api.delete(`/products/${id}/`);

// Customers
export const getCustomers = () => api.get('/customers/');
export const getCustomer = (id) => api.get(`/customers/${id}/`);
export const createCustomer = (data) => api.post('/customers/', data);
export const updateCustomer = (id, data) => api.put(`/customers/${id}/`, data);
export const deleteCustomer = (id) => api.delete(`/customers/${id}/`);

// Invoices
export const getInvoices = () => api.get('/invoices/');
export const getInvoice = (id) => api.get(`/invoices/${id}/`);
export const createInvoice = (data) => api.post('/invoices/', data);
export const updateInvoice = (id, data) => api.put(`/invoices/${id}/`, data);
export const deleteInvoice = (id) => api.delete(`/invoices/${id}/`);

// OpenFoodFacts
export const searchOpenFoodFacts = async (query) => {
  try {
    const response = await axios.get('https://world.openfoodfacts.org/cgi/search.pl', {
      params: {
        search_terms: query,
        search_simple: 1,
        json: 1,
        page_size: 1,
      },
    });
    const products = response.data.products || [];
    return products;
  } catch (error) {
    console.error('OpenFoodFacts search error:', error);
    return [];
  }
};

export default api;
