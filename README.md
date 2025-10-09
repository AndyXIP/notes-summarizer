# Notes Summarizer

A modern web application built with Flask that allows users to manage their notes and automatically generate AI-powered summaries using OpenAI's GPT models.

## Features

- **Note Management**: Create, view, edit, and delete notes with a clean interface
- **File Upload**: Support for PDF and TXT file uploads with automatic text extraction
- **AI Summarization**: Generate intelligent summaries using OpenAI's GPT-3.5-turbo
- **Smart Caching**: Store summaries in the database to avoid redundant API calls
- **Summary Management**: Regenerate summaries when needed
- **Real-time Feedback**: Comprehensive error handling with user-friendly messages
- **Responsive Design**: Clean, intuitive user interface

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite
- **AI Integration**: OpenAI API
- **File Processing**: PyPDF2 for PDF text extraction
- **Frontend**: Jinja2 templates with HTML/CSS
- **Environment Management**: python-dotenv

## Installation and Setup

### Prerequisites

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AndyXIP/notes-summarizer.git
   cd notes-summarizer
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file in the backend directory
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   echo "SECRET_KEY=your-secret-key-here" >> .env
   ```

5. **Initialize the database**
   ```bash
   python create_db.py
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Open your browser** and navigate to `http://localhost:5000`

## Usage

### Creating Notes
- Click "New Note" to manually create a note with title and content
- Use "Upload" to import content from PDF or TXT files

### AI Summarization
- Click "Summarize" on any note to generate an AI summary
- Summaries are automatically saved to prevent redundant API calls
- Use "Regenerate Summary" to create a new summary if needed

### File Formats Supported
- **PDF**: Automatic text extraction from PDF documents
- **TXT**: Plain text file import

## Project Structure

```
notes-summarizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── models.py            # Database models
│   │   ├── routes.py            # Application routes
│   │   └── templates/           # Jinja2 templates
│   ├── instance/
│   │   └── notes.sqlite         # SQLite database
│   ├── config.py                # Configuration settings
│   ├── create_db.py             # Database initialization
│   ├── run.py                   # Application entry point
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
└── .gitignore
└── LICENSE
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
SECRET_KEY=your-flask-secret-key
DATABASE_URL=sqlite:///instance/notes.sqlite  # Optional
```

### OpenAI API Setup

1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Generate an API key from the API keys section
3. Add billing information (GPT-3.5-turbo costs ~$0.002 per 1K tokens)
4. Add your API key to the `.env` file

## Key Features Explained

### Smart Summary Caching
- Summaries are stored in the database after generation
- Prevents unnecessary API calls and reduces costs
- UI dynamically shows "Summarize" button or existing summary

### Error Handling
- Graceful handling of API quota limits with fallback summaries
- File validation for uploads
- Comprehensive logging for debugging

### Database Design
- Clean SQLAlchemy models with proper relationships
- Automatic timestamps for notes
- Migration scripts for schema updates

## Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Note categories and tagging system
- [ ] Search functionality
- [ ] Export options (PDF, Word)
- [ ] RESTful API for mobile/React frontend
- [ ] Batch summarization
- [ ] Different summary styles (brief, detailed, bullet points)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT API
- [Flask](https://flask.palletsprojects.com/) for the excellent web framework
- [PyPDF2](https://pypdf2.readthedocs.io/) for PDF text extraction

## Contact

Andy - [@AndyXIP](https://github.com/AndyXIP)

Project Link: [https://github.com/AndyXIP/notes-summarizer](https://github.com/AndyXIP/notes-summarizer)

---

⭐ **If you found this project helpful, please give it a star!**
