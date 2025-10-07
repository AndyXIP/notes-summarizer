import io
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
    Placeholder summarization endpoint.
    Replace this with a real summarizer (AI service, algorithm, or background job).
    """
    note = Note.query.get_or_404(note_id)
    # TEMP: simple slice summary — replace with your summarization logic
    summary = (note.content or '')[:500].strip()
    if len(note.content or '') > 500:
        summary += '...'
    return render_template('summary.html', note=note, summary=summary)


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
