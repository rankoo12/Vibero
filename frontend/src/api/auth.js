import { apiRequest } from "./client";

export function registerUser(data) {
  return apiRequest("/auth/register", {
    method: "POST",
    body: data,
  });
}

export function loginUser(data) {
  return apiRequest("/auth/login", {
    method: "POST",
    body: data,
    credentials: "include", 
  });
}

export function fetchMe() {
  return apiRequest("/auth/login", {
    method: "GET",
    credentials: "include",  // ✅ required for cookies
  });
}

