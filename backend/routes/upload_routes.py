import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
import logging

from backend.routes import upload_bp
from backend.modules import Config, DocumentProcessor, EmbeddingService
from backend.utils import FileValidator

logger = logging.getLogger(__name__)

current_document = {'text': '', 'chunks': [], 'filename': ''}
embedding_service = EmbeddingService()

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    global current_document
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename or not FileValidator.allowed_file(file.filename):
        return jsonify({
            'error': 'Invalid file type. Only PDF and DOCX files are allowed.'
        }), 400
    
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        file_extension = os.path.splitext(filename)[1].lower()
        text = DocumentProcessor.extract_text(file_path, file_extension)
        
        FileValidator.validate_text_content(text)
        
        chunks = DocumentProcessor.chunk_text(text, max_words=Config.CHUNK_MAX_WORDS)
        
        FileValidator.validate_chunks(chunks)
        
        try:
            embedding_service.create_faiss_index(chunks)
            
            current_document = {
                'text': text,
                'chunks': chunks,
                'filename': filename
            }
        except Exception as embedding_error:
            if "quota" in str(embedding_error).lower():
                return jsonify({
                    'error': f'Upload successful but embedding failed due to quota limits. {str(embedding_error)} Please try again later or upgrade your Google AI plan.'
                }), 429
            else:
                return jsonify({
                    'error': f'Upload successful but indexing failed: {str(embedding_error)}'
                }), 500
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'text_preview': text[:500] + '...' if len(text) > 500 else text,
            'total_chunks': len(chunks),
            'total_words': DocumentProcessor.count_words(text)
        }), 200
        
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def get_current_document():
    return current_document

def get_embedding_service():
    return embedding_service
