import io
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from openai import OpenAI

from . import db
from .models import Note

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename: str) -> bool:
    """
    Check if the uploaded filename has an allowed extension (txt or pdf).
    Used for file upload validation.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def summarize_with_openai(content: str) -> str:
    """
    Generate a summary of the given text using the OpenAI API.
    Returns the summary string or raises an exception if the API call fails.
    """
    api_key = current_app.config.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not configured")
    
    # Debug: Check if API key is loaded (don't log the actual key!)
    current_app.logger.info(f"API key loaded: {bool(api_key) and len(api_key) > 10}")
    
    # Initialize OpenAI client (official way)
    client = OpenAI(api_key=api_key)
    
    # Create a prompt for summarization
    prompt = f"""Please provide a concise summary of the following text. 
Focus on the main points and key information. Keep the summary between 100-300 words.

Text to summarize:
{content}

Summary:"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates clear, concise summaries of text content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        current_app.logger.error(f"OpenAI API error: {str(e)}")
        raise


@main.route('/', methods=['GET'])
def root():
    """
    Root endpoint for health check and welcome message.
    """
    return jsonify({"message": "Reached Notes Summarizer backend API."})


@main.route('/api/notes', methods=['GET'])
def list_notes():
    """
    Get a list of all notes, ordered by most recent.
    Returns a JSON array of note objects.
    """
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return jsonify([
        {
            'id': n.id,
            'title': n.title,
            'content': n.content,
            'summary': n.summary,
            'timestamp': n.timestamp.isoformat() if n.timestamp else None
        } for n in notes
    ])


@main.route('/api/notes', methods=['POST'])
def create_note():
    """
    Create a new note from JSON payload (title, content).
    Returns the created note as JSON.
    """
    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    if not title:
        return jsonify({'error': 'Title is required.'}), 400
    try:
        note = Note(title=title, content=content)
        db.session.add(note)
        db.session.commit()
        return jsonify({'id': note.id, 'title': note.title, 'content': note.content, 'summary': note.summary, 'timestamp': note.timestamp.isoformat() if note.timestamp else None}), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception('Error creating note')
        return jsonify({'error': 'Failed to create note.'}), 500


@main.route('/api/notes/upload', methods=['POST'])
def upload_note():
    """
    Upload a TXT or PDF file, extract its text, and create a new note.
    Returns the created note as JSON, or error if upload fails.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only .txt and .pdf allowed.'}), 400
    filename = secure_filename(file.filename)
    text_content = ''
    try:
        file_bytes = file.read()
        if filename.lower().endswith('.txt'):
            text_content = file_bytes.decode('utf-8', errors='replace')
        elif filename.lower().endswith('.pdf'):
            reader = PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
        else:
            return jsonify({'error': 'Unsupported file extension.'}), 400
    except Exception:
        current_app.logger.exception('Failed to extract text from uploaded file')
        return jsonify({'error': 'Failed to extract text from file. Make sure the file is a valid .txt or .pdf.'}), 500
    title = filename.rsplit('.', 1)[0] or 'Uploaded Note'
    try:
        note = Note(title=title, content=text_content)
        db.session.add(note)
        db.session.commit()
        return jsonify({'id': note.id, 'title': note.title, 'content': note.content, 'summary': note.summary, 'timestamp': note.timestamp.isoformat() if note.timestamp else None}), 201
    except Exception:
        db.session.rollback()
        current_app.logger.exception('DB error saving uploaded note')
        return jsonify({'error': 'Failed to save note.'}), 500


@main.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """
    Get a single note by its ID.
    Returns the note as JSON, or 404 if not found.
    """
    note = Note.query.get_or_404(note_id)
    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'summary': note.summary,
        'timestamp': note.timestamp.isoformat() if note.timestamp else None
    })


@main.route('/api/notes/<int:note_id>/summarize', methods=['POST'])
def summarize_note(note_id):
    """
    Generate and cache an AI summary for a note by its ID.
    Returns the summary as JSON, or error if summarization fails.
    """
    note = Note.query.get_or_404(note_id)
    if not note.content or not note.content.strip():
        return jsonify({'error': 'Cannot summarize an empty note.'}), 400
    if note.summary:
        return jsonify({'error': 'Summary already exists for this note.', 'summary': note.summary}), 200
    try:
        summary = summarize_with_openai(note.content)
        note.summary = summary
        db.session.commit()
        return jsonify({'id': note.id, 'summary': note.summary}), 200
    except ValueError as e:
        current_app.logger.error(f"Configuration error: {str(e)}")
        return jsonify({'error': 'AI summarization is not configured.'}), 500
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            words = note.content.split()
            if len(words) > 100:
                summary = ' '.join(words[:100]) + '...\n\n[Demo Summary - OpenAI quota exceeded. This is a simple text truncation.]'
            else:
                summary = note.content + '\n\n[Demo Summary - OpenAI quota exceeded. Full text shown.]'
            try:
                note.summary = summary
                db.session.commit()
            except Exception:
                db.session.rollback()
            return jsonify({'error': 'AI summarization quota exceeded. Saved simple summary for demo.', 'summary': summary}), 200
        else:
            current_app.logger.exception('Failed to generate summary with OpenAI')
            return jsonify({'error': 'Failed to generate summary. Please try again later.'}), 500


@main.route('/api/notes/<int:note_id>/regenerate-summary', methods=['POST'])
def regenerate_summary(note_id):
    """
    Regenerate the AI summary for a note, replacing any existing summary.
    Returns the new summary as JSON, or error if summarization fails.
    """
    note = Note.query.get_or_404(note_id)
    if not note.content or not note.content.strip():
        return jsonify({'error': 'Cannot summarize an empty note.'}), 400
    try:
        summary = summarize_with_openai(note.content)
        note.summary = summary
        db.session.commit()
        return jsonify({'id': note.id, 'summary': note.summary}), 200
    except ValueError as e:
        current_app.logger.error(f"Configuration error: {str(e)}")
        return jsonify({'error': 'AI summarization is not configured.'}), 500
    except Exception as e:
        current_app.logger.exception('Failed to regenerate summary with OpenAI')
        return jsonify({'error': 'Failed to regenerate summary. Please try again later.'}), 500


@main.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """
    Delete a note by its ID.
    Returns a JSON result message.
    """
    note = Note.query.get_or_404(note_id)
    try:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'result': 'Note deleted.'})
    except Exception:
        db.session.rollback()
        current_app.logger.exception('Failed to delete note')
        return jsonify({'error': 'Failed to delete note.'}), 500
