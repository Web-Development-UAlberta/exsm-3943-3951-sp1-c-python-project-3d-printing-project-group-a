/* eslint-disable @typescript-eslint/no-explicit-any */
const API_URL = "http://127.0.0.1:5000/api";

const url = (path: string) => {
  const full = `${API_URL}${path}`;
  return full.endsWith("/") ? full : full + "/";
};

export async function apiGet(path: string) {
  const token = localStorage.getItem("token");
  const res = await fetch(url(path), {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || "Request failed");
  }
  return res.json();
}

export async function apiPost(path: string, body: any) {
  const token = localStorage.getItem("token");
  const res = await fetch(url(path), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || "Request failed");
  }
  return res.json();
}

export async function apiPut(path: string, body: any) {
  const token = localStorage.getItem("token");
  const res = await fetch(url(path), {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || "Request failed");
  }
  return res.json();
}

export async function apiDelete(path: string) {
  const token = localStorage.getItem("token");
  const res = await fetch(url(path), {
    method: "DELETE",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.error || "Request failed");
  }
  return res.json();
}
