from flask import Blueprint

upload_bp = Blueprint('upload', __name__)
document_bp = Blueprint('document', __name__)
qa_bp = Blueprint('qa', __name__)

from backend.routes import upload_routes, document_routes, qa_routes

__all__ = ['upload_bp', 'document_bp', 'qa_bp']
