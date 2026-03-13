# Legal/Policy Document Summarization and Q&A System

## Overview
A Flask-based web application with modular architecture that allows users to upload legal and policy documents (PDF/DOCX), get AI-powered summaries, and ask questions about the document content using semantic search and Google Generative AI (Gemini 2.5 Flash).

## Features
- **Document Upload**: Supports PDF and DOCX file formats with drag-and-drop
- **Text Extraction**: Automatic extraction from uploaded documents using pdfplumber and python-docx
- **AI Summarization**: On-demand summaries using Google Gemini 2.5 Flash (latest stable GA model)
- **Q&A System**: Semantic search using FAISS embeddings to retrieve relevant document chunks and answer user questions
- **Responsive UI**: Clean, modern interface that works on mobile and desktop
- **Modular Architecture**: Well-organized codebase with separation of concerns

## Architecture

### Backend Structure (Modular)
```
backend/
├── modules/                    # Core business logic
│   ├── config.py              # Configuration management
│   ├── document_processor.py  # Document extraction and chunking
│   ├── ai_service.py          # Google AI integration
│   └── embedding_service.py   # FAISS vector operations
├── routes/                     # API endpoints
│   ├── upload_routes.py       # File upload handling
│   ├── document_routes.py     # Summary and status endpoints
│   └── qa_routes.py           # Question answering endpoint
└── utils/                      # Utility functions
    └── validators.py          # Input validation
```

### Frontend Structure
```
frontend/
└── static/
    ├── index.html            # Main UI
    ├── js/
    │   └── app.js           # JavaScript logic
    └── css/
        └── style.css        # Styling
```

### API Endpoints
- `GET /` - Serve frontend
- `POST /upload` - Upload and process documents (extracts text, creates embeddings, builds FAISS index)
- `POST /summarize` - Generate document summary using Gemini (on-demand only)
- `POST /ask` - Answer questions using RAG (Retrieval-Augmented Generation)
- `GET /status` - Check document status

### Document Processing Pipeline
1. User uploads PDF/DOCX file
2. DocumentProcessor extracts text
3. Text is chunked into ~800 word segments
4. EmbeddingService generates embeddings using Google's text-embedding-004 model
5. Embeddings are stored in a FAISS index for fast similarity search
6. User optionally generates summary (no automatic API calls)
7. When users ask questions, top 5 most relevant chunks are retrieved as context for Gemini

## Dependencies
- **Backend**: Flask, Flask-CORS, pdfplumber, python-docx, faiss-cpu, google-generativeai, python-dotenv, numpy
- **Frontend**: Vanilla JavaScript (no frameworks)

## Environment Variables
- `GOOGLE_API_KEY` - Required for Google Generative AI access (get it from https://aistudio.google.com/)

## AI Models Used
- **Chat Model**: gemini-2.5-flash (latest GA/stable model, production-ready)
- **Embedding Model**: models/text-embedding-004 (for semantic search)

## Recent Changes

### November 12, 2025 - Version 2.0.0 (Major Refactor)
- **✅ Modular Architecture**: Completely restructured codebase
  - Separated into backend modules (config, document_processor, ai_service, embedding_service)
  - Created dedicated route handlers (upload, document, qa)
  - Added utility validators
  - Improved code organization and maintainability

- **✅ Fixed Double Request Issue**: 
  - Summary generation is now optional (user must click "Generate Summary")
  - Previous version auto-generated summary after upload, wasting API quota
  - Summary section now hidden until document is uploaded

- **✅ Updated to Latest Stable Models**:
  - Changed from gemini-2.0-flash-exp (experimental) to gemini-2.5-flash (GA)
  - Gemini 2.5 Flash is production-ready with better performance
  - Still using text-embedding-004 (current stable embedding model)

- **✅ Enhanced Error Handling**:
  - Comprehensive validation for all inputs
  - Detailed error messages for API quota issues
  - Graceful handling of missing API keys
  - Better exception propagation

- **✅ Improved Configuration**:
  - Centralized configuration in Config class
  - Environment variable management
  - Easy to modify settings

- **✅ Better Directory Structure**:
  - Moved data to `data/` directory (uploads, faiss_indexes)
  - Frontend reorganized to `frontend/static/`
  - Cleaner project root

- **✅ Comprehensive Testing**:
  - Module import tests
  - Configuration validation tests
  - File validator edge case tests
  - API endpoint tests
  - Error handling tests

- **✅ Documentation**:
  - PROJECT.md: Complete project overview and setup instructions
  - MODULES.md: Detailed module documentation
  - Updated replit.md (this file)

## User Preferences
None specified yet.

## Project Structure
```
.
├── app.py                      # Flask app entry point
├── backend/
│   ├── modules/               # Core business logic
│   │   ├── config.py
│   │   ├── document_processor.py
│   │   ├── ai_service.py
│   │   └── embedding_service.py
│   ├── routes/                # API endpoints
│   │   ├── upload_routes.py
│   │   ├── document_routes.py
│   │   └── qa_routes.py
│   └── utils/                 # Utilities
│       └── validators.py
├── frontend/
│   └── static/
│       ├── index.html
│       ├── js/
│       │   └── app.js
│       └── css/
│           └── style.css
├── data/
│   ├── uploads/               # Temporary document storage
│   └── faiss_indexes/         # FAISS index storage
├── PROJECT.md                 # Detailed project documentation
├── MODULES.md                 # Module-level documentation
├── .gitignore                # Git ignore rules
└── replit.md                 # This file
```

## Important Notes
- The free tier of Google AI API has rate limits (approximately 2 requests per minute for generation)
- If you hit quota limits, wait 1-2 minutes before trying again
- Check your usage at https://aistudio.google.com/
- Summary generation is now optional to save API quota
- All test results show successful operation of all modules

## Setup Instructions

1. **Configure API Key**:
   - Add GOOGLE_API_KEY to Replit Secrets
   - Get your key from https://aistudio.google.com/

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the Application**:
   - Open the web preview
   - Upload a PDF or DOCX file
   - Optionally generate a summary
   - Ask questions about the document

## Testing Results

All comprehensive tests passed:
- ✅ Module imports
- ✅ Configuration validation
- ✅ File validator (PDF, DOCX, edge cases)
- ✅ AI Service initialization
- ✅ Document processor (chunking, word count)
- ✅ Error handling for empty/invalid inputs
- ✅ Directory structure
- ✅ Critical files present
- ✅ API endpoints registered
- ✅ Full upload/summarize/ask workflow

## Security Features
- API key protection (environment variables only)
- File type validation (whitelist: PDF, DOCX)
- File size limits (16MB max)
- Secure filename sanitization
- Input validation on all endpoints
- No sensitive data in error messages

## Performance Characteristics
- Document processing: ~1-2 seconds per chunk for embeddings
- Summary generation: ~2-5 seconds depending on document length
- Question answering: ~2-3 seconds (embedding + retrieval + generation)
- FAISS search: Milliseconds for similarity search

## Future Enhancements
- Support for more file formats (TXT, RTF, HTML)
- OCR for scanned documents
- Multi-document comparison
- Export summaries to PDF/DOCX
- Document history and management
- User authentication
