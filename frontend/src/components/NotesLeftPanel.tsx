import type { Note } from '../types';

export interface NotesLeftPanelProps {
  notes: Note[];
  loading: boolean;
  deleteError?: string;
  uploadError?: string;
  title: string;
  content: string;
  onTitleChange: (v: string) => void;
  onContentChange: (v: string) => void;
  onCreate: (e: React.FormEvent<HTMLFormElement>) => void;
  onUpload: (e: React.FormEvent<HTMLFormElement>) => void;
  onSelect: (id: number) => void;
  onDelete: (id: number) => Promise<void> | void;
}

export default function NotesLeftPanel({
  notes,
  loading,
  deleteError,
  uploadError,
  title,
  content,
  onTitleChange,
  onContentChange,
  onCreate,
  onUpload,
  onSelect,
  onDelete,
}: NotesLeftPanelProps) {
  return (
    <div className="left-panel">
      <form onSubmit={onCreate} className="note-form">
        <input
          value={title}
          onChange={(e) => onTitleChange(e.target.value)}
          placeholder="Title"
          required
          style={{ width: '40%', marginRight: 8, padding: 8, borderRadius: 4, border: '1px solid #ccc' }}
        />
        <input
          value={content}
          onChange={(e) => onContentChange(e.target.value)}
          placeholder="Content"
          required
          style={{ width: '40%', marginRight: 8, padding: 8, borderRadius: 4, border: '1px solid #ccc' }}
        />
        <button type="submit" style={{ padding: '8px 16px', borderRadius: 4 }}>Add Note</button>
      </form>

      <form onSubmit={onUpload} style={{ marginBottom: '1rem', background: '#000000ff', borderRadius: 8, border: '1px solid #e0e0e0', padding: '1rem' }}>
        <input type="file" name="file" accept=".txt,.pdf" style={{ marginRight: 8 }} />
        <button type="submit" style={{ padding: '8px 16px', borderRadius: 4 }}>Upload TXT/PDF</button>
        {uploadError && <span style={{ color: 'red', marginLeft: 8 }}>{uploadError}</span>}
      </form>

      <h2 style={{ marginTop: '2rem' }}>All Notes</h2>
      {deleteError && <div style={{ color: 'red', marginBottom: 8 }}>{deleteError}</div>}
      {loading ? <div>Loading...</div> : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {notes.map((note) => (
            <li key={note.id} style={{ marginBottom: 12, padding: '8px 0', borderBottom: '1px solid #eee', display: 'flex', alignItems: 'center' }}>
              <strong style={{ flex: 1 }}>{note.title}</strong>
              <button onClick={() => onSelect(note.id)} style={{ marginLeft: 8, padding: '4px 10px', borderRadius: 4 }}>View</button>
              <button onClick={() => onDelete(note.id)} style={{ marginLeft: 8, padding: '4px 10px', borderRadius: 4 }}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
