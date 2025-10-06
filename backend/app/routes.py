from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Note
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

main = Blueprint('main', __name__)

# Allowed file types for upload
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page — list notes
@main.route('/')
def index():
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return render_template('index.html', notes=notes)

# Create a new note manually
@main.route('/note/new', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        note = Note(title=title, content=content)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('new_note.html')

# Upload a note from a file
@main.route('/note/upload', methods=['GET', 'POST'])
def upload_note():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            text_content = ""

            if filename.lower().endswith('.txt'):
                text_content = file.read().decode('utf-8')
            elif filename.lower().endswith('.pdf'):
                reader = PdfReader(file)
                for page in reader.pages:
                    text_content += page.extract_text() + "\n"

            title = filename.rsplit('.', 1)[0]  # use filename (without extension) as title
            note = Note(title=title, content=text_content)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('Invalid file type. Only .txt and .pdf allowed.')
            return redirect(request.url)

    return render_template('upload_note.html')

# View a single note
@main.route('/note/<int:note_id>')
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('view_note.html', note=note)

# Summarize a note
@main.route('/note/<int:note_id>/summarize', methods=['POST'])
def summarize_note(note_id):
    note = Note.query.get_or_404(note_id)
    # TEMP: placeholder summarization
    summary = note.content[:100] + '...'  # replace later with AI summarization
    return render_template('summary.html', note=note, summary=summary)

# Delete a note
@main.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('main.index'))