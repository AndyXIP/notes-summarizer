

# Notes Summarizer

![Status](https://img.shields.io/badge/Status-Complete-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000?logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=06192E)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

Full‑stack note taking app with AI‑powered summarization. Upload PDFs/TXT or write notes, then generate concise summaries using OpenAI. Built with Flask + SQLite on the backend and a Vite + React TypeScript frontend.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
	- [Backend Setup](#backend-setup)
	- [Frontend Setup](#frontend-setup)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Development Notes](#development-notes)
- [Suggested Future Directions](#suggested-future-directions)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

Notes Summarizer helps you manage notes and generate high‑quality summaries. It supports file uploads (PDF/TXT), smart caching to avoid repeat API calls, and smooth error handling. Ideal for students and professionals who need quick overviews of lengthy content.

---

## Features

- Create, view, and delete notes with a clean UI
- Upload PDF and TXT files with automatic text extraction
- One‑click AI summarization (OpenAI GPT‑3.5‑turbo)
- Smart caching of generated summaries to save cost
- Regenerate summaries on demand
- Helpful error messages and validation
- Fast, responsive React frontend

---

## Architecture

```
┌──────────────────────────┐        HTTP (fetch/axios)        ┌──────────────────────────┐
│     Frontend (Vite)      │ ───────────────────────────────► │        Flask API         │
│   React + TypeScript     │                                  │   (Flask, CORS, ORM)     │
└───────────────┬──────────┘                                  └───────────────┬──────────┘
				│                                                          │
				│                         SQLAlchemy ORM                   │
				│                                                          │
				│                                                          ▼
				│                                                   SQLite Database
				│
				│                 External AI (Summarization)
				└──────────────────────────────────────────────────────► OpenAI API
```

---

## Tech Stack

- Frontend: React 19, Vite, TypeScript
- Backend: Flask 3.x, Flask‑SQLAlchemy, Flask‑CORS
- Database: SQLite (default) via SQLAlchemy
- AI: OpenAI API (chat completions, gpt‑3.5‑turbo)
- File processing: PyPDF2 (PDF text extraction)

---

## Project Structure

```
notes-summarizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory + CORS + DB init
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── routes.py            # API routes (notes, upload, summarize)
│   ├── instance/                # SQLite database location
│   │   └── notes.sqlite
│   ├── config.py                # Configuration settings
│   ├── create_db.py             # DB initialization script
│   ├── run.py                   # App entrypoint
│   └── requirements.txt         # Python deps
├── frontend/
│   ├── src/App.tsx              # Main React component
│   ├── src/api.ts               # Backend API client
│   └── ...                      # Other frontend files
├── LICENSE
└── README.md
```

---

## Getting Started

### Backend Setup

Prerequisites: Python 3.8+, OpenAI API key

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# Create environment file
cat > .env << 'EOF'
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key
# Optional: override default DB path
# DATABASE_URL=sqlite:///instance/notes.sqlite
EOF

# Initialize database
python create_db.py

# Run the API (http://127.0.0.1:5000)
python run.py
```

### Frontend Setup

Prerequisites: Node.js 18+ and npm

```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
```

---

## Configuration

Create `backend/.env` with:

```env
OPENAI_API_KEY=sk-your-openai-api-key
SECRET_KEY=your-flask-secret-key
DATABASE_URL=sqlite:///instance/notes.sqlite  # optional
```

OpenAI setup:
1) Create an account and API key at https://platform.openai.com/
2) Add billing if needed; set the key in `.env`
3) The backend will read `OPENAI_API_KEY` at runtime

---

## API Documentation

Base URL (dev): `http://127.0.0.1:5000`

- `GET /` – Health check
	- Response: `{ "message": "Reached Notes Summarizer backend API." }`

- `GET /api/notes` – List notes (most recent first)

- `POST /api/notes` – Create note
	- JSON: `{ "title": string, "content": string }`

- `POST /api/notes/upload` – Upload TXT/PDF and create note
	- multipart/form‑data: `file` (.txt | .pdf)

- `GET /api/notes/:id` – Get note by ID

- `POST /api/notes/:id/summarize` – Generate summary if missing
	- Errors: 400 on empty note; 200 with existing summary
	- On OpenAI quota errors, a fallback demo summary is stored

- `POST /api/notes/:id/regenerate-summary` – Force regenerate summary

- `DELETE /api/notes/:id` – Delete note

All responses are JSON. See `backend/app/routes.py` for full details.

---

## Development Notes

- Frontend dev server: `http://localhost:5173`
- Backend dev server: `http://127.0.0.1:5000`
- CORS is enabled in the Flask app factory
- Default DB path is `backend/instance/notes.sqlite` (auto‑created)
- Max upload size is enforced; large files return HTTP 413

---

## Suggested Future Directions

The project is archived; below are non‑committal ideas that could be explored if development resumes:

- User authentication and multi‑user support
- Note categories and tagging
- Full‑text search
- Export to PDF/Markdown
- Batch summarization
- Summary styles (brief, detailed, bullets)

---

## License

This project is licensed under the MIT License – see [LICENSE](LICENSE).

---

## Acknowledgements

- [OpenAI](https://openai.com/) for the GPT API
- [Flask](https://flask.palletsprojects.com/) for the elegant web framework
- [PyPDF2](https://pypdf2.readthedocs.io/) for lightweight PDF text extraction
