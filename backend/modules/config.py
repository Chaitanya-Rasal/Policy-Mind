import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    UPLOAD_FOLDER = 'data/uploads'
    FAISS_FOLDER = 'data/faiss_indexes'
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    MAX_TEXT_LENGTH = 15000
    CHUNK_MAX_WORDS = 800
    TOP_K_CHUNKS = 5
    
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    GEMINI_MODEL = 'gemini-2.5-flash'
    EMBEDDING_MODEL = 'models/text-embedding-004'
    
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = '0.0.0.0'
    PORT = 5000
    
    @classmethod
    def ensure_directories(cls):
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.FAISS_FOLDER, exist_ok=True)
        logger.info(f"Ensured directories: {cls.UPLOAD_FOLDER}, {cls.FAISS_FOLDER}")
    
    @classmethod
    def validate_api_key(cls):
        if not cls.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY not found in environment variables!")
            logger.error("Please add your Google AI Studio API key to Secrets with key 'GOOGLE_API_KEY'")
            return False
        return True
