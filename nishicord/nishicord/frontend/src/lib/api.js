import { supabase } from './supabaseClient';

const BASE_URL = import.meta.env.VITE_BACKEND_URL;

async function authHeaders() {
  const { data } = await supabase.auth.getSession();
  return { Authorization: `Bearer ${data.session?.access_token}` };
}

export async function apiGet(path) {
  const res = await fetch(`${BASE_URL}${path}`, { headers: await authHeaders() });
  if (!res.ok) throw new Error((await res.json()).error);
  return res.json();
}

export async function apiPost(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(await authHeaders()) },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error((await res.json()).error);
  return res.json();
}

export async function apiDelete(path) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'DELETE',
    headers: await authHeaders(),
  });
  if (!res.ok && res.status !== 204) throw new Error((await res.json()).error);
}
