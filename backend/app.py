import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # CORS configuration
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:8080", "http://localhost", "http://127.0.0.1", "http://localhost:80"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True
        }
    })

    # Import routes using absolute import
    from routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

if __name__ == '__main__':
    application = create_app()
    application.run(debug=True)
