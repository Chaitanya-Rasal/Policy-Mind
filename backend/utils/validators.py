from backend.modules.config import Config
import logging

logger = logging.getLogger(__name__)

class FileValidator:
    
    @staticmethod
    def allowed_file(filename):
        if not filename or '.' not in filename:
            return False
        
        extension = filename.rsplit('.', 1)[1].lower()
        is_allowed = extension in Config.ALLOWED_EXTENSIONS
        
        if not is_allowed:
            logger.warning(f"File extension '.{extension}' not allowed")
        
        return is_allowed
    
    @staticmethod
    def validate_text_content(text):
        if not text or not text.strip():
            raise ValueError(
                "No text could be extracted from the document. The file may be empty, scanned, or image-based."
            )
        return True
    
    @staticmethod
    def validate_chunks(chunks):
        if not chunks:
            raise ValueError(
                "Document is too short to process. Please upload a longer document."
            )
        return True
    
    @staticmethod
    def validate_question(question):
        if not question or not question.strip():
            raise ValueError("No question provided")
        return True
