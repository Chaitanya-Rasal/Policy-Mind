import numpy as np
import faiss
import pickle
import os
import logging
from backend.modules.config import Config
from backend.modules.ai_service import AIService

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.faiss_index = None
        self.chunk_texts = []
    
    def create_faiss_index(self, chunks):
        if not chunks:
            logger.warning("No chunks provided for FAISS index creation")
            return None
        
        self.chunk_texts = chunks
        embeddings = []
        
        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        for i, chunk in enumerate(chunks):
            embedding = AIService.generate_embedding(chunk)
            embeddings.append(embedding)
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1}/{len(chunks)} embeddings")
        
        embeddings_array = np.array(embeddings).astype('float32')
        
        dimension = embeddings_array.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(embeddings_array)
        
        self._save_index()
        
        logger.info(f"FAISS index created successfully with {len(chunks)} vectors")
        return self.faiss_index
    
    def search_similar_chunks(self, query, top_k=5):
        if self.faiss_index is None or not self.chunk_texts:
            logger.warning("FAISS index not initialized or no chunks available")
            return []
        
        try:
            query_embedding = AIService.generate_embedding(query)
            query_vector = np.array([query_embedding]).astype('float32')
            
            distances, indices = self.faiss_index.search(query_vector, top_k)
            
            results = []
            for idx in indices[0]:
                if idx < len(self.chunk_texts):
                    results.append(self.chunk_texts[idx])
            
            logger.info(f"Found {len(results)} similar chunks for query")
            return results
        except Exception as e:
            logger.error(f"Error searching similar chunks: {str(e)}")
            raise
    
    def _save_index(self):
        try:
            faiss_path = os.path.join(Config.FAISS_FOLDER, 'index.faiss')
            chunks_path = os.path.join(Config.FAISS_FOLDER, 'chunks.pkl')
            
            faiss.write_index(self.faiss_index, faiss_path)
            with open(chunks_path, 'wb') as f:
                pickle.dump(self.chunk_texts, f)
            
            logger.info(f"FAISS index saved to {faiss_path}")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {str(e)}")
            raise
    
    def load_index(self):
        try:
            faiss_path = os.path.join(Config.FAISS_FOLDER, 'index.faiss')
            chunks_path = os.path.join(Config.FAISS_FOLDER, 'chunks.pkl')
            
            if os.path.exists(faiss_path) and os.path.exists(chunks_path):
                self.faiss_index = faiss.read_index(faiss_path)
                with open(chunks_path, 'rb') as f:
                    self.chunk_texts = pickle.load(f)
                logger.info(f"FAISS index loaded with {len(self.chunk_texts)} chunks")
                return True
            else:
                logger.info("No existing FAISS index found")
                return False
        except Exception as e:
            logger.error(f"Error loading FAISS index: {str(e)}")
            return False
    
    def clear_index(self):
        self.faiss_index = None
        self.chunk_texts = []
        logger.info("FAISS index cleared")
