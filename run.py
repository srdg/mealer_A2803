"""
Entry point for the Mealer web application.

Supports both development and production modes via FLASK_ENV environment variable.

Author: Soumik Ranjan Dasgupta
"""

import os
from app import create_app


if __name__ == '__main__':
    # Get environment from FLASK_ENV, default to production
    env = os.getenv('FLASK_ENV', 'production')
    
    # Create app with appropriate config
    app = create_app()
    
    # Development server settings
    if env == 'development':
        app.run(
            debug=True,
            host='127.0.0.1',
            port=5000,
            use_reloader=True
        )
    else:
        # Production warning
        print("=" * 60)
        print("WARNING: Running in PRODUCTION mode")
        print("Use a production WSGI server (Gunicorn, Waitress) instead!")
        print("Example: gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'")
        print("=" * 60)
        app.run(
            debug=False,
            host='0.0.0.0',
            port=5000
        )
