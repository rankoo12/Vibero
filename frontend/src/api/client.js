const BASE_URL = import.meta.env.VITE_API_URL;

export async function apiRequest(endpoint, { method = "GET", body, token, credentials } = {}) {
  const headers = {
    "Content-Type": "application/json",
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
    credentials, // ✅ this line enables cookie auth
  });

  const data = await res.json();

  if (!res.ok) {
    const message = data?.detail || res.statusText;
    throw new Error(message);
  }

  return data;
}
