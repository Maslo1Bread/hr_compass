const API_BASE = "http://127.0.0.1:8000";

let accessToken = localStorage.getItem("hr_access_token") || "";

export async function login(login, password) {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ login, password }),
  });
  if (!response.ok) {
    throw new Error("Login failed");
  }
  const data = await response.json();
  accessToken = data.access_token;
  localStorage.setItem("hr_access_token", accessToken);
  return data;
}

export async function getMyProfile() {
  const response = await fetch(`${API_BASE}/users/me`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!response.ok) {
    throw new Error("Failed to load profile");
  }
  return response.json();
}

export async function askChat(question) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ question }),
  });
  if (!response.ok) {
    throw new Error("Chat request failed");
  }
  return response.json();
}
