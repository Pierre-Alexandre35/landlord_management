import { apiFetch } from "./client";

export async function register(email: string, password: string) {
  const data = await apiFetch("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  localStorage.setItem("token", data.access_token);
  return data;
}

export async function login(email: string, password: string) {
  const data = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });

  localStorage.setItem("token", data.access_token);
  return data;
}

export async function changePassword(oldPassword: string, newPassword: string) {
  const token = localStorage.getItem("token");

  return apiFetch("/auth/change-password", {
    method: "POST",
    body: JSON.stringify({
      old_password: oldPassword,
      new_password: newPassword,
    }),
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
