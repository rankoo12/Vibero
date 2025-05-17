// src/api/users.js
import apiClient from './client';

// Register a new user
export const registerUser = async (data) => {
  try {
    const res = await apiClient.post('/users', data);
    return res.data; // If needed
  } catch (err) {
    // Extract useful backend error message
    const msg =
      err.response?.data?.detail || err.message || "Registration failed";
    throw new Error(msg); // Ensures clean error in RegisterPage
  }
};

// Log in an existing user
export async function loginUser(username, data) {
  const res = await apiClient.post(
    `/users/${username}/login`,
    data,
    { withCredentials: true } // ✅ ensure cookies are handled
  );
  return res.data;  // user object
}

// Restore session from cookie
export async function fetchSession() {
  const res = await apiClient.get('/users/session', {
    withCredentials: true, // ✅ same here for cookie session
  });
  return res.data;  // user object
}
