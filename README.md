

# Notes Summarizer

## Features

- **Note Management**: Create, view, edit, and delete notes with a clean interface
- **File Upload**: Support for PDF and TXT file uploads with automatic text extraction
- **AI Summarization**: Generate intelligent summaries using OpenAI's GPT-3.5-turbo
- **Smart Caching**: Store summaries in the database to avoid redundant API calls
- **Summary Management**: Regenerate summaries when needed
- **Real-time Feedback**: Comprehensive error handling with user-friendly messages
- **Responsive Design**: Clean, intuitive user interface
- **React Frontend**: Fast, modern UI built with Vite + React

## Technology Stack

- **Frontend**: React (Vite)
- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite
- **AI Integration**: OpenAI API
- **File Processing**: PyPDF2 for PDF text extraction
- **Environment Management**: python-dotenv

## Project Structure

```
notes-summarizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── models.py            # Database models
│   │   ├── routes.py            # Application routes
│   ├── instance/
│   │   └── notes.sqlite         # SQLite database
│   ├── config.py                # Configuration settings
│   ├── create_db.py             # Database initialization
│   ├── run.py                   # Application entry point
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
├── frontend/
│   ├── src/App.tsx              # Main React component
│   ├── src/api.ts               # API utility for backend
│   └── ...                      # Other frontend files
└── README.md
```

## Cloning & Setup

### Prerequisites
- Python 3.8+
- Node.js & npm
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Clone the repository
```bash
git clone https://github.com/AndyXIP/notes-summarizer.git
cd notes-summarizer
```

## Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
# On Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Create .env file in the backend directory
echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env
python create_db.py
python run.py
```

Note: you may need to create an directory called 'instance' in the backend directory with a file called 'notes.sqlite' inside of it to work as the databse. Alternative databases can also be used but will need to have their paths updated in the .env or config.py file.

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

> The React frontend communicates with the Flask backend at `http://127.0.0.1:5000`. Make sure the backend is running before using the frontend.

## Usage

### Creating Notes
- Use the React app to manually create a note with title and content
- Use "Upload" to import content from PDF or TXT files

### AI Summarization
- Click "Summarize" on any note to generate an AI summary
- Summaries are automatically saved to prevent redundant API calls
- Use "Regenerate Summary" to create a new summary if needed

### File Formats Supported
- **PDF**: Automatic text extraction from PDF documents
- **TXT**: Plain text file import

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

## Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Note categories and tagging system
- [ ] Search functionality
- [ ] Export options (PDF, Word)
- [ ] Batch summarization
- [ ] Different summary styles (brief, detailed, bullet points)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com/) for providing the GPT API
- [Flask](https://flask.palletsprojects.com/) for the excellent web framework
- [PyPDF2](https://pypdf2.readthedocs.io/) for PDF text extraction

---
