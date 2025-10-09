from . import db
from datetime import datetime, timezone

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Note {self.title} by User {self.user_id}>'