// src/api/client.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  timeout: 10000, // 10 seconds
});

// Optional: Global error handling
apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      console.warn("Unauthorized - maybe log the user out.");
      // Optionally clear session or redirect
    }
    return Promise.reject(err);
  }
);

export default apiClient;
