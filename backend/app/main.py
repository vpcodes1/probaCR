"""Main Flask application for B2B Hub."""
import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS

from .database import init_db
from .api import auth_bp, listings_bp, messages_bp, companies_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def create_app():
    """Create and configure Flask app."""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'b2b-hub-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///b2b_hub.db')

    # CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Initialize database
    with app.app_context():
        init_db()
        logger.info("Database initialized")

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(listings_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(companies_bp)

    # Root endpoint
    @app.route('/')
    def root():
        """Root endpoint."""
        return jsonify({
            "message": "Welcome to B2B Hub API",
            "version": "1.0.0",
            "endpoints": {
                "auth": "/api/auth",
                "listings": "/api/listings",
                "messages": "/api/messages",
                "companies": "/api/companies"
            }
        })

    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "B2B Hub"
        })

    logger.info("B2B Hub API started successfully")
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
