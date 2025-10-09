
import React, { useEffect, useState } from 'react';
import { fetchNotes, createNote, deleteNote, getNote, summarizeNote } from './api';

async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch('http://127.0.0.1:5000/api/notes/upload', {
    method: 'POST',
    body: formData
  });
  return res.json();
}

function App() {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedNote, setSelectedNote] = useState(null);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  useEffect(() => {
    loadNotes();
  }, []);

  async function loadNotes() {
    setLoading(true);
    const notesArr = await fetchNotes();
    setNotes(Array.isArray(notesArr) ? notesArr : []);
    setLoading(false);
  }

  async function handleCreate(e) {
    e.preventDefault();
    await createNote(title, content);
    setTitle('');
    setContent('');
    loadNotes();
  }

  async function handleSelect(id) {
    const note = await getNote(id);
    setSelectedNote(note);
    setSummary(note.summary || '');
  }

  async function handleSummarize(id) {
    const res = await summarizeNote(id);
    setSummary(res.summary || '');
    loadNotes();
  }

  const [deleteError, setDeleteError] = useState('');

  async function handleDelete(id) {
    setDeleteError('');
    try {
      const result = await deleteNote(id);
      if (result.error) {
        setDeleteError(result.error);
      } else {
        setSelectedNote(null);
        loadNotes();
      }
    } catch (err) {
      setDeleteError('Delete failed.');
    }
  }

  async function handleFileUpload(e) {
    e.preventDefault();
    setUploadError('');
    const file = e.target.file.files[0];
    if (!file) {
      setUploadError('No file selected.');
      return;
    }
    const allowed = ['txt', 'pdf'];
    const ext = file.name.split('.').pop().toLowerCase();
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
        loadNotes();
      }
    } catch (err) {
      setUploadError('Upload failed.');
    }
  }

  return (
    <div style={{
      maxWidth: '1200px',
      margin: '2rem auto',
      fontFamily: 'sans-serif',
      padding: '2rem',
      boxSizing: 'border-box',
      background: '#000000ff',
      borderRadius: '12px'
    }}>
      <h1 style={{ marginBottom: '2rem' }}>Notes Summarizer</h1>
      <div style={{ display: 'flex', gap: '2rem' }}>
        {/* Left: Notes list and forms */}
        <div style={{ flex: 1, minWidth: 320 }}>
          <form onSubmit={handleCreate} style={{ marginBottom: '1rem', background: '#000000ff', borderRadius: 8, border: '1px solid #ffffffff', padding: '1rem' }}>
            <input
              value={title}
              onChange={e => setTitle(e.target.value)}
              placeholder="Title"
              required
              style={{ width: '40%', marginRight: 8, padding: 8, borderRadius: 4, border: '1px solid #ccc' }}
            />
            <input
              value={content}
              onChange={e => setContent(e.target.value)}
              placeholder="Content"
              required
              style={{ width: '40%', marginRight: 8, padding: 8, borderRadius: 4, border: '1px solid #ccc' }}
            />
            <button type="submit" style={{ padding: '8px 16px', borderRadius: 4 }}>Add Note</button>
          </form>

          <form onSubmit={handleFileUpload} style={{ marginBottom: '1rem', background: '#000000ff', borderRadius: 8, border: '1px solid #e0e0e0', padding: '1rem' }}>
            <input type="file" name="file" accept=".txt,.pdf" style={{ marginRight: 8 }} />
            <button type="submit" style={{ padding: '8px 16px', borderRadius: 4 }}>Upload TXT/PDF</button>
            {uploadError && <span style={{ color: 'red', marginLeft: 8 }}>{uploadError}</span>}
          </form>

          <h2 style={{ marginTop: '2rem' }}>All Notes</h2>
          {deleteError && <div style={{ color: 'red', marginBottom: 8 }}>{deleteError}</div>}
          {loading ? <div>Loading...</div> : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {notes.map(note => (
                <li key={note.id} style={{ marginBottom: 12, padding: '8px 0', borderBottom: '1px solid #eee', display: 'flex', alignItems: 'center' }}>
                  <strong style={{ flex: 1 }}>{note.title}</strong>
                  <button onClick={() => handleSelect(note.id)} style={{ marginLeft: 8, padding: '4px 10px', borderRadius: 4 }}>View</button>
                  <button onClick={() => handleDelete(note.id)} style={{ marginLeft: 8, padding: '4px 10px', borderRadius: 4 }}>Delete</button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Right: Selected note details */}
        <div style={{ flex: 2, minWidth: 340, marginLeft: '2rem' }}>
          {selectedNote ? (
            <div style={{ background: '#000000ff', border: '1px solid #ccc', padding: 24, borderRadius: 8, boxShadow: '0 1px 4px #eee', minHeight: 200 }}>
              <h3 style={{ marginTop: 0 }}>{selectedNote.title}</h3>
              <p style={{ whiteSpace: 'pre-wrap' }}>{selectedNote.content}</p>
              <button onClick={() => handleSummarize(selectedNote.id)} style={{ marginTop: 12, padding: '8px 16px', borderRadius: 4 }}>
                Summarize
              </button>
              {summary && (
                <div style={{ marginTop: 18 }}>
                  <strong>Summary:</strong>
                  <p style={{ background: '#000000ff', padding: 12, borderRadius: 4 }}>{summary}</p>
                </div>
              )}
            </div>
          ) : (
            <div style={{ color: '#888', padding: 32, textAlign: 'center' }}>
              <em>Select a note to view its details.</em>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
