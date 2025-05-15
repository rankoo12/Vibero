// src/api/users.js
import apiClient from './client';

// Register a new user
export const registerUser = (data) => {
  return apiClient.post('/users', data); // ✅ still correct
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
