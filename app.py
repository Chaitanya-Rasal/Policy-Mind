import os
import logging
from flask import Flask
from flask_cors import CORS

from backend.modules import Config, AIService
from backend.routes import upload_bp, document_bp, qa_bp

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__, 
                static_folder='frontend/static',
                static_url_path='')
    
    CORS(app)
    
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
    
    Config.ensure_directories()
    
    if Config.validate_api_key():
        AIService.initialize()
        logger.info("Application initialized successfully")
    else:
        logger.warning("Application started without AI service (API key missing)")
    
    app.register_blueprint(upload_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(qa_bp)
    
    @app.route('/')
    def index():
        return app.send_static_file('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
