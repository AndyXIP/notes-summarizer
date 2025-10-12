
import { useEffect, useState } from 'react';
import { fetchNotes, createNote, deleteNote, getNote, summarizeNote } from './api';
import type { Note } from './types';
import './App.css';
import NotesLeftPanel from './components/NotesLeftPanel';
import NoteRightPanel from './components/NoteRightPanel';

async function uploadFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch('http://127.0.0.1:5000/api/notes/upload', {
    method: 'POST',
    body: formData
  });
  return res.json();
}

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [title, setTitle] = useState<string>('');
  const [content, setContent] = useState<string>('');
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [summary, setSummary] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [uploadError, setUploadError] = useState<string>('');
  useEffect(() => {
    loadNotes();
  }, []);

  async function loadNotes() {
    setLoading(true);
    const notesArr = await fetchNotes();
    setNotes(Array.isArray(notesArr) ? notesArr : []);
    setLoading(false);
  }

  async function handleCreate(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    await createNote(title, content);
    setTitle('');
    setContent('');
    loadNotes();
  }

  async function handleSelect(id: number) {
    const note = await getNote(id);
    setSelectedNote(note);
    setSummary(note.summary || '');
  }

  async function handleSummarize(id: number) {
    const res = await summarizeNote(id);
    setSummary(res.summary || '');
    loadNotes();
  }

  const [deleteError, setDeleteError] = useState('');

  async function handleDelete(id: number) {
    setDeleteError('');
    try {
      const result = await deleteNote(id);
      if ('error' in result) {
        setDeleteError(result.error);
      } else {
        setSelectedNote(null);
        await loadNotes();
      }
    } catch (err) {
      setDeleteError('Delete failed.');
    }
  }

  async function handleFileUpload(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setUploadError('');

    const fileInput = e.currentTarget.elements.namedItem('file') as HTMLInputElement | null;
    const file = fileInput?.files?.[0];

    if (!file) {
      setUploadError('No file selected.');
      return;
    }

    const allowed = ['txt', 'pdf'];
    const ext = file.name.split('.').pop()?.toLowerCase() ?? '';
    if (!allowed.includes(ext)) {
      setUploadError('Only TXT and PDF files allowed.');
      return;
    }

    try {
      const result = await uploadFile(file);
      if (result.error) {
        setUploadError(result.error);
      } else {
        setUploadError('');
        await loadNotes();
      }
    } catch (err) {
      setUploadError('Upload failed.');
    }
  }


  return (
    <>
      <div className="app-container">
        <h1 style={{ marginBottom: '2rem' }}>Notes Summarizer</h1>
        <div className="main-content">
          <NotesLeftPanel
            notes={notes}
            loading={loading}
            deleteError={deleteError}
            uploadError={uploadError}
            title={title}
            content={content}
            onTitleChange={setTitle}
            onContentChange={setContent}
            onCreate={handleCreate}
            onUpload={handleFileUpload}
            onSelect={handleSelect}
            onDelete={handleDelete}
          />
          <NoteRightPanel
            note={selectedNote}
            summary={summary}
            onSummarize={handleSummarize}
          />
        </div>
      </div>
    </>
  );
}

export default App;