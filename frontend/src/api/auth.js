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
  });
}

export function fetchMe(token) {
  return apiRequest("/auth/me", {
    method: "GET",
    token,
  });
}
