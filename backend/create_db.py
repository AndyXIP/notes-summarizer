from app import create_app, db

app = create_app()

# Use app context to access the database
with app.app_context():
    db.create_all()
    print("Database tables created!")
