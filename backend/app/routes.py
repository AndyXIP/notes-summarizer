from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Note

main = Blueprint('main', __name__)

# Home page — list notes
@main.route('/')
def index():
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return render_template('index.html', notes=notes)

# Create a new note
@main.route('/note/new', methods=['GET', 'POST'])
def new_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        note = Note(title=title, content=content)  # no user_id
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('new_note.html')

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
