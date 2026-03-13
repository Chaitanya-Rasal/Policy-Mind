import pdfplumber
from docx import Document
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    
    @staticmethod
    def extract_text_from_pdf(file_path):
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            logger.info(f"Successfully extracted {len(text)} characters from PDF")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_path):
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            logger.info(f"Successfully extracted {len(text)} characters from DOCX")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            raise Exception(f"Failed to extract text from DOCX: {str(e)}")
    
    @staticmethod
    def extract_text(file_path, file_extension):
        if file_extension == '.pdf':
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return DocumentProcessor.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
    
    @staticmethod
    def count_words(text):
        return len(text.split())
    
    @staticmethod
    def chunk_text(text, max_words=800):
        words = text.split()
        chunks = []
        
        current_chunk = []
        for word in words:
            current_chunk.append(word)
            if len(current_chunk) >= max_words:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        logger.info(f"Created {len(chunks)} chunks from text with {len(words)} words")
        return chunks
