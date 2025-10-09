// Basic API utility for Flask backend
const API_BASE = 'http://127.0.0.1:5000/api/notes';

export async function fetchNotes() {
  const res = await fetch(API_BASE);
  return res.json();
}

export async function createNote(title, content) {
  const res = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content })
  });
  return res.json();
}

export async function deleteNote(id) {
  const res = await fetch(`${API_BASE}/${id}`, {
    method: 'DELETE'
  });
  return res.json();
}

export async function getNote(id) {
  const res = await fetch(`${API_BASE}/${id}`);
  return res.json();
}

export async function summarizeNote(id) {
  const res = await fetch(`${API_BASE}/${id}/summarize`, {
    method: 'POST'
  });
  return res.json();
}
