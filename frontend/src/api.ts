import type { Note } from './types';

const API_BASE = 'http://127.0.0.1:5000/api/notes';

export async function fetchNotes(): Promise<Note[]> {
  const res = await fetch(API_BASE);
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`Failed to fetch notes (${res.status}): ${text}`);
  }
  return res.json();
}

export async function createNote(title: string, content: string): Promise<Note | { error: string }> {
  const res = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content }),
  });
  return res.json();
}

export type DeleteResponse = { result: string } | { error: string };
export async function deleteNote(id: number): Promise<DeleteResponse> {
  const res = await fetch(`${API_BASE}/${id}`, { method: 'DELETE' });
  return res.json();
}

export async function getNote(id: number): Promise<Note> {
  const res = await fetch(`${API_BASE}/${id}`);
  return res.json();
}

export type SummarizeResponse = { id: number; summary: string } | { error: string; summary?: string };
export async function summarizeNote(id: number): Promise<SummarizeResponse> {
  const res = await fetch(`${API_BASE}/${id}/summarize`, { method: 'POST' });
  return res.json();
}
