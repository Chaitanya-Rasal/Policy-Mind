import google.generativeai as genai
import logging
from backend.modules.config import Config

logger = logging.getLogger(__name__)

class AIService:
    _model = None
    _embed_model = None
    _initialized = False
    
    @classmethod
    def initialize(cls):
        if cls._initialized:
            return True
        
        if not Config.GOOGLE_API_KEY:
            logger.error("Cannot initialize AI Service: GOOGLE_API_KEY not found")
            return False
        
        try:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            cls._model = genai.GenerativeModel(Config.GEMINI_MODEL)
            cls._embed_model = Config.EMBEDDING_MODEL
            cls._initialized = True
            logger.info(f"AI Service initialized with model: {Config.GEMINI_MODEL}")
            return True
        except Exception as e:
            logger.error(f"Error initializing AI Service: {str(e)}")
            cls._initialized = False
            return False
    
    @classmethod
    def get_model(cls):
        if not cls._initialized:
            cls.initialize()
        return cls._model
    
    @classmethod
    def get_embedding_model(cls):
        if not cls._initialized:
            cls.initialize()
        return cls._embed_model
    
    @classmethod
    def is_initialized(cls):
        return cls._initialized
    
    @classmethod
    def generate_embedding(cls, text):
        if not cls._initialized:
            raise Exception("AI Service not initialized. Please check your API key configuration.")
        
        try:
            result = genai.embed_content(
                model=cls._embed_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "429" in error_str:
                raise Exception(
                    "Google AI API quota exceeded. Please wait 1-2 minutes before trying again, or check your usage at https://aistudio.google.com/"
                )
            elif "api" in error_str and "key" in error_str:
                raise Exception(
                    "Invalid Google AI API key. Please check your API key configuration."
                )
            else:
                logger.error(f"Embedding error: {str(e)}")
                raise Exception(f"Embedding generation failed: {str(e)}")
    
    @classmethod
    def generate_summary(cls, text):
        if not cls._initialized:
            raise Exception("AI Service not initialized. Please check your API key configuration.")
        
        if len(text) > Config.MAX_TEXT_LENGTH:
            text = text[:Config.MAX_TEXT_LENGTH] + "..."
        
        prompt = f"""You are a helpful assistant that summarizes legal and policy documents. 
Provide a clear, concise summary highlighting key points, requirements, and important clauses.

Please summarize the following document:

{text}"""
        
        try:
            response = cls._model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "429" in error_str:
                raise Exception(
                    "API quota exceeded. Please wait a minute before trying again. The free tier has a limit of 2 requests per minute."
                )
            else:
                logger.error(f"Summary generation error: {str(e)}")
                raise Exception(f"Summary generation failed: {str(e)}")
    
    @classmethod
    def answer_question(cls, question, context):
        if not cls._initialized:
            raise Exception("AI Service not initialized. Please check your API key configuration.")
        
        prompt = f"""You are a helpful assistant that answers questions about legal and policy documents. 
Use only the provided context to answer questions accurately and cite relevant sections when possible.

Context from document:
{context}

Question: {question}

Please provide a detailed answer based on the context above."""
        
        try:
            response = cls._model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "429" in error_str:
                raise Exception(
                    "API quota exceeded. Please wait a minute before trying again. The free tier has a limit of 2 requests per minute."
                )
            else:
                logger.error(f"Question answering error: {str(e)}")
                raise Exception(f"Question answering failed: {str(e)}")
