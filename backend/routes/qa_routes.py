from flask import request, jsonify
import logging

from backend.routes import qa_bp
from backend.modules import AIService, Config
from backend.utils import FileValidator
from backend.routes.upload_routes import get_current_document, get_embedding_service

logger = logging.getLogger(__name__)

@qa_bp.route('/ask', methods=['POST'])
def ask_question():
    current_document = get_current_document()
    embedding_service = get_embedding_service()
    
    if not current_document['text']:
        return jsonify({
            'error': 'No document uploaded. Please upload a document first.'
        }), 400
    
    if not AIService.is_initialized():
        return jsonify({
            'error': 'AI Service not initialized. Please check your API key configuration.'
        }), 500
    
    data = request.get_json()
    question = data.get('question', '')
    
    try:
        FileValidator.validate_question(question)
        
        relevant_chunks = embedding_service.search_similar_chunks(
            question, 
            top_k=Config.TOP_K_CHUNKS
        )
        
        if not relevant_chunks:
            return jsonify({
                'error': 'Could not find relevant information in the document. This might be due to embedding service issues.'
            }), 404
        
        context = "\n\n".join(relevant_chunks)
        answer = AIService.answer_question(question, context)
        
        return jsonify({
            'answer': answer,
            'question': question,
            'document': current_document['filename'],
            'chunks_used': len(relevant_chunks)
        }), 200
        
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logger.error(f"Q&A error: {str(e)}")
        return jsonify({'error': f'Question answering failed: {str(e)}'}), 500
