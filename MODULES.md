# Module Documentation

This document provides detailed descriptions of each module in the Legal/Policy Document Summarizer & Q&A System.

---

## Backend Modules

### 1. `backend/modules/config.py`

**Purpose**: Centralized configuration management for the entire application.

#### Class: `Config`

A configuration class that holds all application settings and provides utility methods.

##### Attributes:

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `UPLOAD_FOLDER` | str | `'data/uploads'` | Directory for temporary file storage |
| `FAISS_FOLDER` | str | `'data/faiss_indexes'` | Directory for FAISS index storage |
| `ALLOWED_EXTENSIONS` | set | `{'pdf', 'docx'}` | Allowed file extensions |
| `MAX_CONTENT_LENGTH` | int | `16777216` (16MB) | Maximum file upload size |
| `MAX_TEXT_LENGTH` | int | `15000` | Maximum text length for summarization |
| `CHUNK_MAX_WORDS` | int | `800` | Maximum words per chunk |
| `TOP_K_CHUNKS` | int | `5` | Number of chunks to retrieve for Q&A |
| `GOOGLE_API_KEY` | str | From env | Google AI API key |
| `GEMINI_MODEL` | str | `'gemini-2.5-flash'` | Gemini model name |
| `EMBEDDING_MODEL` | str | `'models/text-embedding-004'` | Embedding model name |
| `DEBUG` | bool | `True` | Debug mode flag |
| `HOST` | str | `'0.0.0.0'` | Flask server host |
| `PORT` | int | `5000` | Flask server port |

##### Methods:

**`ensure_directories()`**
- **Purpose**: Creates upload and FAISS directories if they don't exist
- **Returns**: None
- **Logs**: Directory creation confirmation

**`validate_api_key()`**
- **Purpose**: Validates that Google API key is present
- **Returns**: `bool` - True if key exists, False otherwise
- **Logs**: Error if key is missing

---

### 2. `backend/modules/document_processor.py`

**Purpose**: Handles document text extraction and chunking operations.

#### Class: `DocumentProcessor`

A utility class with static methods for document processing.

##### Methods:

**`extract_text_from_pdf(file_path: str) -> str`**
- **Purpose**: Extracts text from PDF files using pdfplumber
- **Parameters**: 
  - `file_path`: Path to PDF file
- **Returns**: Extracted text as string
- **Raises**: `Exception` if extraction fails
- **Logs**: Character count and errors

**`extract_text_from_docx(file_path: str) -> str`**
- **Purpose**: Extracts text from DOCX files using python-docx
- **Parameters**:
  - `file_path`: Path to DOCX file
- **Returns**: Extracted text as string
- **Raises**: `Exception` if extraction fails
- **Logs**: Character count and errors

**`extract_text(file_path: str, file_extension: str) -> str`**
- **Purpose**: Unified interface for text extraction
- **Parameters**:
  - `file_path`: Path to file
  - `file_extension`: File extension (`.pdf` or `.docx`)
- **Returns**: Extracted text
- **Raises**: `ValueError` for unsupported extensions

**`count_words(text: str) -> int`**
- **Purpose**: Counts words in text
- **Parameters**:
  - `text`: Input text
- **Returns**: Word count
- **Algorithm**: Splits on whitespace

**`chunk_text(text: str, max_words: int = 800) -> list[str]`**
- **Purpose**: Splits text into chunks of specified size
- **Parameters**:
  - `text`: Input text
  - `max_words`: Maximum words per chunk (default: 800)
- **Returns**: List of text chunks
- **Algorithm**: 
  1. Splits text into words
  2. Groups into chunks of `max_words`
  3. Preserves remainder as final chunk
- **Logs**: Chunk count and statistics

---

### 3. `backend/modules/ai_service.py`

**Purpose**: Manages Google Generative AI interactions for embeddings, summarization, and Q&A.

#### Class: `AIService`

A singleton-pattern service class for AI operations.

##### Class Variables:

- `_model`: Google GenerativeModel instance
- `_embed_model`: Embedding model name
- `_initialized`: Initialization status flag

##### Methods:

**`initialize() -> bool`**
- **Purpose**: Initializes Google AI client
- **Returns**: `bool` - Success status
- **Process**:
  1. Checks if already initialized
  2. Validates API key
  3. Configures Google AI with API key
  4. Creates GenerativeModel instance
- **Logs**: Initialization status and errors

**`get_model() -> GenerativeModel`**
- **Purpose**: Returns the initialized model
- **Returns**: GenerativeModel instance
- **Auto-initializes**: If not already initialized

**`get_embedding_model() -> str`**
- **Purpose**: Returns embedding model name
- **Returns**: Model name string

**`is_initialized() -> bool`**
- **Purpose**: Checks initialization status
- **Returns**: `bool` - True if initialized

**`generate_embedding(text: str) -> list[float]`**
- **Purpose**: Generates vector embedding for text
- **Parameters**:
  - `text`: Input text
- **Returns**: List of floats (embedding vector)
- **Task Type**: `"retrieval_document"`
- **Error Handling**:
  - Quota exceeded: User-friendly message with wait time
  - Invalid API key: Configuration error message
  - Other errors: Generic embedding failure
- **Raises**: `Exception` with descriptive message

**`generate_summary(text: str) -> str`**
- **Purpose**: Generates AI summary of document
- **Parameters**:
  - `text`: Document text (truncated to MAX_TEXT_LENGTH)
- **Returns**: Summary text
- **Prompt**: Optimized for legal/policy documents
- **Error Handling**:
  - Quota errors: Rate limit message
  - Other errors: Summary generation failure
- **Raises**: `Exception` with descriptive message

**`answer_question(question: str, context: str) -> str`**
- **Purpose**: Answers questions based on document context
- **Parameters**:
  - `question`: User's question
  - `context`: Relevant document chunks (concatenated)
- **Returns**: Answer text
- **Prompt**: Instructs to use only provided context
- **Error Handling**:
  - Quota errors: Rate limit message
  - Other errors: Question answering failure
- **Raises**: `Exception` with descriptive message

---

### 4. `backend/modules/embedding_service.py`

**Purpose**: Manages FAISS vector index creation, storage, and similarity search.

#### Class: `EmbeddingService`

Handles vector embeddings and FAISS operations.

##### Instance Variables:

- `faiss_index`: FAISS IndexFlatL2 instance
- `chunk_texts`: List of text chunks corresponding to vectors

##### Methods:

**`__init__()`**
- **Purpose**: Initializes empty embedding service
- **Sets**: `faiss_index` and `chunk_texts` to None/empty

**`create_faiss_index(chunks: list[str]) -> faiss.Index`**
- **Purpose**: Creates FAISS index from text chunks
- **Parameters**:
  - `chunks`: List of text chunks
- **Returns**: FAISS index
- **Process**:
  1. Validates chunks exist
  2. Generates embeddings for each chunk (via AIService)
  3. Converts to numpy array (float32)
  4. Creates FAISS IndexFlatL2 (L2 distance)
  5. Adds vectors to index
  6. Saves to disk
- **Logs**: Progress every 10 chunks, completion status
- **Performance**: ~1-2 seconds per chunk depending on API

**`search_similar_chunks(query: str, top_k: int = 5) -> list[str]`**
- **Purpose**: Finds most similar chunks to query
- **Parameters**:
  - `query`: Search query text
  - `top_k`: Number of results to return (default: 5)
- **Returns**: List of most similar text chunks
- **Process**:
  1. Generates embedding for query
  2. Searches FAISS index
  3. Returns corresponding text chunks
- **Algorithm**: L2 distance (Euclidean)
- **Logs**: Result count
- **Error Handling**: Re-raises exceptions for upstream handling

**`_save_index()`**
- **Purpose**: Saves FAISS index and chunks to disk
- **Files**:
  - `data/faiss_indexes/index.faiss`: Binary FAISS index
  - `data/faiss_indexes/chunks.pkl`: Pickled chunk texts
- **Raises**: `Exception` if save fails

**`load_index() -> bool`**
- **Purpose**: Loads previously saved FAISS index from disk
- **Returns**: `bool` - True if successful, False if files don't exist
- **Logs**: Load status and chunk count

**`clear_index()`**
- **Purpose**: Clears in-memory index and chunks
- **Use Case**: Uploading new document

---

### 5. `backend/utils/validators.py`

**Purpose**: Input validation for file uploads, questions, and content.

#### Class: `FileValidator`

Validation utility class with static methods.

##### Methods:

**`allowed_file(filename: str) -> bool`**
- **Purpose**: Validates file extension
- **Parameters**:
  - `filename`: File name
- **Returns**: `bool` - True if extension is allowed
- **Allowed**: `.pdf`, `.docx`
- **Logs**: Warning for disallowed extensions

**`validate_text_content(text: str) -> bool`**
- **Purpose**: Validates extracted text is not empty
- **Parameters**:
  - `text`: Extracted text
- **Returns**: `bool` - Always True if valid
- **Raises**: `ValueError` if text is empty or whitespace-only
- **Message**: Suggests file might be scanned/image-based

**`validate_chunks(chunks: list) -> bool`**
- **Purpose**: Validates chunks were created
- **Parameters**:
  - `chunks`: List of text chunks
- **Returns**: `bool` - Always True if valid
- **Raises**: `ValueError` if chunks list is empty
- **Message**: Suggests document might be too short

**`validate_question(question: str) -> bool`**
- **Purpose**: Validates question is not empty
- **Parameters**:
  - `question`: User's question
- **Returns**: `bool` - Always True if valid
- **Raises**: `ValueError` if question is empty or whitespace-only

---

## Backend Routes

### 6. `backend/routes/upload_routes.py`

**Purpose**: Handles file upload and document processing endpoints.

#### Global Variables:

- `current_document`: Dict storing uploaded document state
- `embedding_service`: EmbeddingService instance

#### Endpoints:

**`POST /upload`**
- **Purpose**: Handles document upload and processing
- **Input**: Multipart form data with 'file' field
- **Process**:
  1. Validates file presence and type
  2. Saves file with secure filename
  3. Extracts text based on extension
  4. Validates text content
  5. Creates chunks
  6. Generates FAISS index with embeddings
  7. Updates current_document state
- **Success Response** (200):
  ```json
  {
    "message": "File uploaded successfully",
    "filename": "document.pdf",
    "text_preview": "First 500 chars...",
    "total_chunks": 5,
    "total_words": 3842
  }
  ```
- **Error Responses**:
  - 400: Invalid file type, no file, empty text
  - 429: API quota exceeded during embedding
  - 500: Processing failure

#### Utility Functions:

**`get_current_document() -> dict`**
- **Purpose**: Returns current document state
- **Used By**: Other route modules

**`get_embedding_service() -> EmbeddingService`**
- **Purpose**: Returns embedding service instance
- **Used By**: Q&A route module

---

### 7. `backend/routes/document_routes.py`

**Purpose**: Document-related endpoints (summary, status).

#### Endpoints:

**`POST /summarize`**
- **Purpose**: Generates AI summary of uploaded document
- **Input**: None (uses current_document)
- **Process**:
  1. Validates document is loaded
  2. Validates AI service is initialized
  3. Generates summary via AIService
- **Success Response** (200):
  ```json
  {
    "summary": "AI-generated summary text...",
    "document": "filename.pdf"
  }
  ```
- **Error Responses**:
  - 400: No document uploaded
  - 500: AI service not initialized or generation failed

**`GET /status`**
- **Purpose**: Returns current document status
- **Input**: None
- **Response** (200):
  ```json
  {
    "document_loaded": true,
    "filename": "document.pdf",
    "total_chunks": 5
  }
  ```
- **Use Case**: Frontend checks on page load

---

### 8. `backend/routes/qa_routes.py`

**Purpose**: Question answering endpoint.

#### Endpoints:

**`POST /ask`**
- **Purpose**: Answers questions about uploaded document
- **Input**:
  ```json
  {
    "question": "What are the key requirements?"
  }
  ```
- **Process**:
  1. Validates document and AI service
  2. Validates question
  3. Searches similar chunks via FAISS
  4. Generates answer using retrieved context
- **Success Response** (200):
  ```json
  {
    "answer": "Based on the document...",
    "question": "What are the key requirements?",
    "document": "filename.pdf",
    "chunks_used": 5
  }
  ```
- **Error Responses**:
  - 400: No document or empty question
  - 404: No relevant chunks found
  - 500: AI service or Q&A failure

---

## Frontend Modules

### 9. `frontend/static/js/app.js`

**Purpose**: Frontend JavaScript logic for UI interactions and API calls.

#### Global Variables:

- `API_BASE_URL`: Empty string (relative URLs)
- `uploadedFile`: Currently selected file
- `documentLoaded`: Document upload status flag

#### Event Handlers:

**File Selection**:
- Click handlers for upload area and button
- Drag-and-drop handlers
- File input change handler
- Validates file types (PDF, DOCX)

**Upload Process**:
- Creates FormData with file
- POSTs to `/upload` endpoint
- Shows loading indicator
- Displays success/error status
- Shows summary section on success
- **Does NOT auto-generate summary**

**Summary Generation**:
- Triggered by "Generate Summary" button click
- POSTs to `/summarize` endpoint
- Displays loading state
- Renders summary or error

**Question Answering**:
- Triggered by "Ask Question" button or Ctrl+Enter
- POSTs to `/ask` endpoint with question
- Displays answer with metadata
- Prepends new answers to results list

**Status Check**:
- Runs on page load
- Checks if document already loaded (persistence)
- Shows summary section if document exists

#### Utility Functions:

**`showStatus(message, type)`**
- Displays status messages (success/error)
- Color-coded by type

**`displayAnswer(data)`**
- Creates and displays Q&A result item
- Formats question, answer, and metadata

**`generateSummary()`**
- Async function for summary generation
- Shows loading, calls API, displays result

---

### 10. `frontend/static/css/style.css`

**Purpose**: Styling and responsive design for the application.

#### Key Features:

- **Gradient Background**: Purple gradient (667eea → 764ba2)
- **Card-Based Layout**: White cards with rounded corners and shadows
- **Responsive Design**: Mobile-friendly with media queries
- **Interactive Elements**:
  - Hover effects on buttons
  - Transform animations
  - Color transitions
- **Status Indicators**:
  - Success: Green background
  - Error: Red background
  - Loading: Spinning animation
- **Typography**: Modern sans-serif font stack
- **Spacing**: Consistent padding and margins

---

## Data Flow

### Document Upload Flow

```
User selects file
    ↓
Frontend validates file type
    ↓
POST /upload with file
    ↓
Backend validates and saves file
    ↓
DocumentProcessor extracts text
    ↓
DocumentProcessor creates chunks
    ↓
EmbeddingService generates embeddings
    ↓
FAISS index created and saved
    ↓
Response with metadata
    ↓
Frontend shows summary section
```

### Summary Generation Flow

```
User clicks "Generate Summary"
    ↓
POST /summarize
    ↓
AIService retrieves document text
    ↓
AIService calls Gemini 2.5 Flash
    ↓
Summary generated
    ↓
Response with summary
    ↓
Frontend displays summary
```

### Question Answering Flow

```
User enters question
    ↓
POST /ask with question
    ↓
EmbeddingService generates query embedding
    ↓
FAISS searches similar chunks
    ↓
Top 5 chunks retrieved
    ↓
AIService generates answer with context
    ↓
Response with answer and metadata
    ↓
Frontend displays Q&A item
```

---

## Error Handling Strategy

### Module-Level Error Handling

Each module handles its specific errors:

1. **DocumentProcessor**: File I/O errors, extraction failures
2. **AIService**: API errors, quota limits, network issues
3. **EmbeddingService**: FAISS errors, storage issues
4. **Validators**: Input validation errors

### Route-Level Error Handling

Routes catch module exceptions and return appropriate HTTP status codes:

- 400: Client errors (bad input)
- 404: Resource not found
- 429: Rate limit exceeded
- 500: Server errors

### Frontend Error Handling

- Try-catch blocks for all API calls
- User-friendly error messages
- Fallback UI states
- Network error handling

---

## Testing Strategy

Each module includes:

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test module interactions
3. **API Tests**: Test endpoint responses
4. **Edge Case Tests**: Test boundary conditions

See debugging session output in logs for test results.

---

## Performance Considerations

### Optimization Points

1. **Chunking**: 800 words balances quality vs. speed
2. **FAISS**: L2 distance optimized for CPU
3. **Caching**: Index saved to disk
4. **Lazy Loading**: AI service initialized on first use
5. **Progress Logging**: Visibility into long operations

### Bottlenecks

1. **Embedding Generation**: ~1-2 seconds per chunk
2. **API Calls**: Rate limited (free tier)
3. **Large Documents**: More chunks = slower processing

---

## Security Best Practices

1. **No API Key Exposure**: Keys in environment variables only
2. **Secure Filenames**: werkzeug sanitization
3. **File Type Validation**: Whitelist approach
4. **Size Limits**: Prevent DOS attacks
5. **Input Validation**: All user inputs validated
6. **Error Messages**: No sensitive information leaked

---

This modular documentation ensures each component is well-understood and maintainable.
