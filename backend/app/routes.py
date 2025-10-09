import io
import requests
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

from . import db
from .models import Note

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename: str) -> bool:
    """Return True if filename has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def summarize_with_openai(content: str) -> str:
    """
    Use OpenAI API to generate a summary of the given content using direct HTTP requests.
    Returns a summary string or raises an exception if API call fails.
    """
    api_key = current_app.config.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not configured")
    
    # Debug: Check if API key is loaded (don't log the actual key!)
    current_app.logger.info(f"API key loaded: {bool(api_key) and len(api_key) > 10}")
    
    # Create a prompt for summarization
    prompt = f"""Please provide a concise summary of the following text. 
Focus on the main points and key information. Keep the summary between 100-300 words.

Text to summarize:
{content}

Summary:"""
    
    # Prepare the API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that creates clear, concise summaries of text content."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 400,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            current_app.logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
            raise Exception(f"OpenAI API returned status {response.status_code}")
        
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
        
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Network error calling OpenAI API: {str(e)}")
        raise
    except (KeyError, IndexError) as e:
        current_app.logger.error(f"Unexpected OpenAI API response format: {str(e)}")
        raise


@main.route('/')
def index():
    """Home page: list notes ordered by timestamp descending."""
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return render_template('index.html', notes=notes)


@main.route('/note/new', methods=['GET', 'POST'])
def new_note():
    """Create a new note manually (title + content)."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title:
            flash('Title is required.', 'warning')
            return redirect(request.url)

        try:
            note = Note(title=title, content=content)
            db.session.add(note)
            db.session.commit()
            flash('Note created.', 'success')
            return redirect(url_for('main.index'))
        except Exception:
            db.session.rollback()
            current_app.logger.exception('Error creating note')
            flash('Failed to create note.', 'danger')
            return redirect(request.url)

    return render_template('new_note.html')


@main.route('/note/upload', methods=['GET', 'POST'])
def upload_note():
    """
    Upload a note from a .txt or .pdf file.
    - Reads file bytes once.
    - Decodes text files with utf-8 and fallback replacement.
    - Uses PyPDF2 PdfReader on a BytesIO stream; handles pages with None text.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part.', 'warning')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file.', 'warning')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Invalid file type. Only .txt and .pdf allowed.', 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        text_content = ''

        try:
            # Read file bytes once (useful for PdfReader which expects a bytes-like stream)
            file_bytes = file.read()

            if filename.lower().endswith('.txt'):
                # Decode text file; replace undecodable bytes to avoid exceptions
                text_content = file_bytes.decode('utf-8', errors='replace')
            elif filename.lower().endswith('.pdf'):
                # Parse PDF from bytes using BytesIO
                reader = PdfReader(io.BytesIO(file_bytes))
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
            else:
                flash('Unsupported file extension.', 'danger')
                return redirect(request.url)
        except Exception:
            current_app.logger.exception('Failed to extract text from uploaded file')
            flash('Failed to extract text from file. Make sure the file is a valid .txt or .pdf.', 'danger')
            return redirect(request.url)

        # Use filename (without extension) as a default title
        title = filename.rsplit('.', 1)[0] or 'Uploaded Note'

        try:
            note = Note(title=title, content=text_content)
            db.session.add(note)
            db.session.commit()
            flash('Note uploaded successfully.', 'success')
            return redirect(url_for('main.index'))
        except Exception:
            db.session.rollback()
            current_app.logger.exception('DB error saving uploaded note')
            flash('Failed to save note.', 'danger')
            return redirect(request.url)

    return render_template('upload_note.html')


@main.route('/note/<int:note_id>')
def view_note(note_id):
    """View single note page."""
    note = Note.query.get_or_404(note_id)
    return render_template('view_note.html', note=note)


@main.route('/note/<int:note_id>/summarize', methods=['POST'])
def summarize_note(note_id):
    """
    Generate an AI-powered summary of the note using OpenAI API.
    """
    note = Note.query.get_or_404(note_id)
    
    if not note.content or not note.content.strip():
        flash('Cannot summarize an empty note.', 'warning')
        return redirect(url_for('main.view_note', note_id=note_id))
    
    try:
        summary = summarize_with_openai(note.content)
        return render_template('summary.html', note=note, summary=summary)
    
    except ValueError as e:
        # Configuration error (missing API key)
        current_app.logger.error(f"Configuration error: {str(e)}")
        flash('AI summarization is not configured. Please contact the administrator.', 'danger')
        return redirect(url_for('main.view_note', note_id=note_id))
    
    except Exception as e:
        # Check if it's a quota/billing issue
        if "429" in str(e) or "quota" in str(e).lower():
            # Provide a simple fallback summary for demo purposes
            words = note.content.split()
            if len(words) > 100:
                summary = ' '.join(words[:100]) + '...\n\n[Demo Summary - OpenAI quota exceeded. This is a simple text truncation.]'
            else:
                summary = note.content + '\n\n[Demo Summary - OpenAI quota exceeded. Full text shown.]'
            
            flash('AI summarization quota exceeded. Showing simple summary for demo.', 'warning')
            return render_template('summary.html', note=note, summary=summary)
        else:
            # Other API or network errors
            current_app.logger.exception('Failed to generate summary with OpenAI')
            flash('Failed to generate summary. Please try again later.', 'danger')
            return redirect(url_for('main.view_note', note_id=note_id))


@main.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    """Delete a note (POST)."""
    note = Note.query.get_or_404(note_id)
    try:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted.', 'success')
    except Exception:
        db.session.rollback()
        current_app.logger.exception('Failed to delete note')
        flash('Failed to delete note.', 'danger')
    return redirect(url_for('main.index'))
