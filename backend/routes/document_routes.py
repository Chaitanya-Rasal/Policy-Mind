from flask import jsonify
import logging

from backend.routes import document_bp
from backend.modules import AIService
from backend.routes.upload_routes import get_current_document

logger = logging.getLogger(__name__)

@document_bp.route('/summarize', methods=['POST'])
def summarize():
    current_document = get_current_document()
    
    if not current_document['text']:
        return jsonify({
            'error': 'No document uploaded. Please upload a document first.'
        }), 400
    
    if not AIService.is_initialized():
        return jsonify({
            'error': 'AI Service not initialized. Please check your API key configuration.'
        }), 500
    
    try:
        text = current_document['text']
        summary = AIService.generate_summary(text)
        
        return jsonify({
            'summary': summary,
            'document': current_document['filename']
        }), 200
        
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        return jsonify({'error': f'Summarization failed: {str(e)}'}), 500

@document_bp.route('/status', methods=['GET'])
def status():
    current_document = get_current_document()
    
    return jsonify({
        'document_loaded': bool(current_document['text']),
        'filename': current_document.get('filename', ''),
        'total_chunks': len(current_document.get('chunks', []))
    }), 200
