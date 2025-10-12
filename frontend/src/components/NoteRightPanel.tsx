import type { Note } from '../types';

export interface NoteRightPanelProps {
  note: Note | null;
  summary: string;
  onSummarize: (id: number) => void;
}

export default function NoteRightPanel({ note, summary, onSummarize }: NoteRightPanelProps) {
  return (
    <div className="right-panel">
      {note ? (
        <div className="note_content">
          <h3 style={{ marginTop: 0 }}>{note.title}</h3>
          <p style={{ whiteSpace: 'pre-wrap' }}>{note.content}</p>
          <button onClick={() => onSummarize(note.id)} style={{ marginTop: 12, padding: '8px 16px', borderRadius: 4 }}>
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
  );
}
