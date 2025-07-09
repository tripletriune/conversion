// src/api.js
const BASE_URL = "http://localhost:5000"

export async function getProfile() {
  const res = await fetch(`${BASE_URL}/api/profile`, {
    credentials: 'include'
  })
  if (!res.ok) throw new Error("Not logged in")
  return res.json()
}

export function login() {
  window.location.assign(`${BASE_URL}/login`)
}

export async function logout() {
  await fetch(`${BASE_URL}/api/logout`, { credentials: 'include' })
}

export async function convertMeters(meters) {
  const res = await fetch(`${BASE_URL}/api/convert`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ meters })
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error)
  return data
}
