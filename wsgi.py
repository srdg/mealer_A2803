"""
WSGI entry point for Mealer application.

This module provides the application instance for WSGI servers like Gunicorn.

Author: Soumik Ranjan Dasgupta
"""

from run import app

if __name__ == '__main__':
    # For development only - use run.py instead
    app.run(debug=True, host='127.0.0.1', port=5000)
