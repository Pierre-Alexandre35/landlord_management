import { apiFetch } from "./client";

/* ======================
   Types
====================== */

export interface AuthResponse {
  access_token: string;
  token_type?: string;
}

/* ======================
   Helpers
====================== */

function saveToken(token: string) {
  localStorage.setItem("token", token);
}

export function getToken(): string | null {
  return localStorage.getItem("token");
}

export function logout() {
  localStorage.removeItem("token");
}

/* ======================
   API calls
====================== */

export async function register(
  email: string,
  password: string
): Promise<AuthResponse> {
  const data = await apiFetch<AuthResponse>("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  saveToken(data.access_token);
  return data;
}

export async function login(
  email: string,
  password: string
): Promise<AuthResponse> {
  const data = await apiFetch<AuthResponse>("/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  saveToken(data.access_token);
  return data;
}

export async function changePassword(
  oldPassword: string,
  newPassword: string
) {
  const token = getToken();

  if (!token) {
    throw new Error("Not authenticated");
  }

  return apiFetch("/auth/change-password", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      old_password: oldPassword,
      new_password: newPassword,
    }),
  });
}
