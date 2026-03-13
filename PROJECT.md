# Legal/Policy Document Summarizer & Q&A System

## Overview

A Flask-based web application that enables users to upload legal and policy documents (PDF/DOCX), generate AI-powered summaries, and ask questions about document content using semantic search powered by Google Generative AI (Gemini 2.5 Flash) and FAISS vector embeddings.

## Key Features

### 1. Document Processing
- **Supported Formats**: PDF and DOCX files
- **Text Extraction**: Automatic extraction using pdfplumber and python-docx
- **Smart Chunking**: Documents are split into manageable chunks (800 words max) for optimal processing
- **File Validation**: Robust validation for file types and content

### 2. AI-Powered Summarization
- **Model**: Google Gemini 2.5 Flash (latest stable model)
- **On-Demand Generation**: Summaries are generated only when explicitly requested (no automatic API calls)
- **Concise Output**: Highlights key points, requirements, and important clauses
- **Context-Aware**: Processes up to 15,000 characters with intelligent truncation

### 3. Semantic Question Answering
- **Embedding Model**: Google text-embedding-004
- **Vector Search**: FAISS (Facebook AI Similarity Search) for fast retrieval
- **Context-Based Answers**: Retrieves top 5 most relevant chunks for accurate responses
- **Source Attribution**: Shows which parts of the document were used to answer

### 4. Modern User Interface
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Drag-and-Drop**: Easy file upload with drag-and-drop support
- **Real-Time Feedback**: Loading indicators and status messages
- **Clean Layout**: Gradient background with card-based sections

## Technical Architecture

### Modular Backend Structure

```
backend/
├── modules/              # Core business logic
│   ├── config.py        # Configuration management
│   ├── document_processor.py  # Document extraction and chunking
│   ├── ai_service.py    # Google AI integration
│   └── embedding_service.py   # FAISS vector operations
├── routes/              # API endpoints
│   ├── upload_routes.py # File upload handling
│   ├── document_routes.py  # Summary and status endpoints
│   └── qa_routes.py     # Question answering endpoint
└── utils/               # Utility functions
    └── validators.py    # Input validation
```

### Frontend Structure

```
frontend/
└── static/
    ├── index.html       # Main UI
    ├── js/
    │   └── app.js      # JavaScript logic
    └── css/
        └── style.css   # Styling
```

### Data Storage

```
data/
├── uploads/            # Uploaded documents (temporary)
└── faiss_indexes/      # Vector embeddings and FAISS index
```

## API Endpoints

### 1. Upload Document
- **Endpoint**: `POST /upload`
- **Input**: Multipart form data with 'file' field
- **Output**: File metadata, chunk count, word count
- **Process**: Extracts text → Creates chunks → Generates embeddings → Builds FAISS index

### 2. Generate Summary
- **Endpoint**: `POST /summarize`
- **Input**: None (uses previously uploaded document)
- **Output**: AI-generated summary with document name
- **Note**: Only called when user clicks "Generate Summary" button

### 3. Ask Question
- **Endpoint**: `POST /ask`
- **Input**: JSON with 'question' field
- **Output**: AI-generated answer with source attribution and chunk count
- **Process**: Embeds question → Searches FAISS → Retrieves relevant chunks → Generates answer

### 4. Check Status
- **Endpoint**: `GET /status`
- **Output**: Document loaded status, filename, chunk count

## Key Improvements in This Version

### ✅ Fixed Double Request Issue
**Problem**: Previous version automatically triggered summary generation after upload, causing unnecessary API calls.

**Solution**: 
- Summary generation is now optional
- "Generate Summary" button added to UI
- Summary section hidden until document is uploaded
- Saves API quota and gives users control

### ✅ Updated to Latest Google Models
**Previous**: `gemini-2.0-flash-exp` (experimental)

**Current**: `gemini-2.5-flash` (GA - General Availability)

**Benefits**:
- More stable and reliable
- Better performance
- Production-ready
- Improved reasoning capabilities

### ✅ Modular Architecture
**Previous**: Monolithic `app.py` with all logic in one file

**Current**: Separated into logical modules

**Benefits**:
- Better code organization
- Easier to maintain and test
- Clear separation of concerns
- Reusable components
- Better error handling

### ✅ Enhanced Error Handling
- Comprehensive validation for all inputs
- Detailed error messages for API quota issues
- Graceful handling of missing API keys
- Proper exception propagation

### ✅ Improved Configuration
- Centralized configuration in `Config` class
- Environment variable management
- Easy to modify settings
- Type-safe constants

## Setup Instructions

### 1. Environment Setup

```bash
# Install Python dependencies (already configured in pyproject.toml)
# Dependencies are managed by uv/pip automatically
```

### 2. Configure Google API Key

Add your Google AI Studio API key to Replit Secrets:
- Key: `GOOGLE_API_KEY`
- Value: Your API key from https://aistudio.google.com/

### 3. Run the Application

```bash
python app.py
```

The application will be available at `http://0.0.0.0:5000`

### 4. Directory Structure

The application automatically creates necessary directories on startup:
- `data/uploads/` - Temporary storage for uploaded files
- `data/faiss_indexes/` - Vector embeddings and FAISS index

## Usage Workflow

1. **Upload Document**
   - Click "Select File" or drag-and-drop a PDF/DOCX file
   - Click "Upload & Process"
   - Wait for processing (text extraction + embedding generation)

2. **Generate Summary** (Optional)
   - Click "Generate Summary" button when ready
   - AI generates a comprehensive summary

3. **Ask Questions**
   - Type your question in the text area
   - Click "Ask Question" or press Ctrl+Enter
   - View AI-generated answer with source attribution

## Configuration Options

Edit `backend/modules/config.py` to customize:

```python
CHUNK_MAX_WORDS = 800        # Max words per chunk
TOP_K_CHUNKS = 5             # Number of chunks to retrieve for Q&A
MAX_TEXT_LENGTH = 15000      # Max text length for summarization
MAX_CONTENT_LENGTH = 16 MB   # Max file upload size
GEMINI_MODEL = 'gemini-2.5-flash'  # AI model
EMBEDDING_MODEL = 'models/text-embedding-004'  # Embedding model
```

## Security Considerations

1. **API Key Protection**: API key stored in environment variables, never exposed to frontend
2. **File Validation**: Only PDF and DOCX files accepted
3. **File Size Limit**: Maximum 16MB upload size
4. **Secure Filenames**: Uses werkzeug's secure_filename for sanitization
5. **CORS Configuration**: Configured for development (adjust for production)

## Performance Optimization

1. **Chunking Strategy**: 800-word chunks optimize embedding quality vs. speed
2. **FAISS Indexing**: Fast similarity search using L2 distance
3. **Caching**: FAISS index saved to disk for persistence
4. **Batch Processing**: Embeddings generated in batches with progress logging

## Troubleshooting

### Issue: API Quota Exceeded
**Solution**: Wait 1-2 minutes between requests. Free tier has rate limits (2 requests/minute for generation).

### Issue: Document Upload Fails
**Possible Causes**:
- File is scanned PDF (no extractable text)
- File is corrupted
- File is too large (>16MB)

### Issue: No Text Extracted
**Solution**: Ensure PDF is not image-based. Use OCR if necessary (not included in this version).

### Issue: Slow Processing
**Cause**: Embedding generation takes time for large documents
**Solution**: Normal for documents with many chunks. Progress logged in console.

## Future Enhancements

- [ ] Support for more file formats (TXT, RTF, HTML)
- [ ] OCR for scanned documents
- [ ] Multi-document comparison
- [ ] Export summaries to PDF/DOCX
- [ ] Document history and management
- [ ] Custom chunking strategies
- [ ] Advanced search filters
- [ ] User authentication and document privacy

## License

This project is provided as-is for educational and development purposes.

## Support

For issues with:
- **Google AI API**: Visit https://aistudio.google.com/
- **Application bugs**: Check logs in `/tmp/logs/` directory
- **Configuration**: Review `backend/modules/config.py`

## Version History

### v2.0.0 (Current)
- ✅ Modular architecture with separated modules
- ✅ Fixed double API request issue
- ✅ Updated to Gemini 2.5 Flash
- ✅ Enhanced error handling
- ✅ Improved documentation

### v1.0.0 (Previous)
- Basic functionality with monolithic structure
- Gemini 2.0 Flash experimental
- Automatic summary generation
