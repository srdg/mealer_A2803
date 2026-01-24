"""
Mealer - Personal Meal Planning Web Application

Direct application entry point with all functionality in one file.
No factory pattern - straightforward architecture for single request handling.

Author: Soumik Ranjan Dasgupta
"""

import os
import logging
from flask import Flask, render_template, jsonify, request
from datetime import datetime

# Import utilities
from app.utils.data_parser import get_meal_data, calculate_macro_percentages

# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Configuration based on environment
FLASK_ENV = os.getenv('FLASK_ENV', 'production')

app.config.update(
    DEBUG=FLASK_ENV == 'development',
    JSON_SORT_KEYS=False,
    JSON_ENSURE_ASCII=False,
    SESSION_COOKIE_SECURE=FLASK_ENV == 'production',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600
)

# Setup logging for production
if FLASK_ENV == 'production':
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    handler = logging.FileHandler(os.path.join(log_dir, 'mealer.log'))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Mealer application started in production mode')

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors."""
    app.logger.warning(f'Bad request: {request.url}')
    return jsonify({'success': False, 'error': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    app.logger.warning(f'Not found: {request.url}')
    return jsonify({'success': False, 'error': 'Page not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    app.logger.error(f'Internal server error: {str(error)}')
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# ============================================================================
# MIDDLEWARE
# ============================================================================

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Landing page with hero section and CTA button."""
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f'Error rendering index: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/meal-plan')
def meal_plan():
    """Meal plan page with calendar and nutritional information."""
    try:
        meal_data = get_meal_data(day=1)
        macro_percentages = calculate_macro_percentages(meal_data['macros'])
        
        return render_template(
            'meal_plan.html',
            meal_data=meal_data,
            macro_percentages=macro_percentages,
            today=datetime.now().strftime('%Y-%m-%d')
        )
    except Exception as e:
        app.logger.error(f'Error rendering meal plan: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/meal-data/<int:day>')
def api_get_meal_data(day: int):
    """API endpoint to fetch meal data for a specific day."""
    try:
        if day < 1 or day > 31:
            return jsonify({
                'success': False,
                'error': 'Day must be between 1 and 31'
            }), 400
        
        meal_data = get_meal_data(day=day)
        macro_percentages = calculate_macro_percentages(meal_data['macros'])
        
        return jsonify({
            'success': True,
            'data': meal_data,
            'macros_percentage': macro_percentages
        })
    except Exception as e:
        app.logger.error(f'Error fetching meal data for day {day}: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Error fetching meal data'
        }), 500


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == '__main__':
    if FLASK_ENV == 'development':
        app.run(
            debug=True,
            host='127.0.0.1',
            port=5000,
            use_reloader=True
        )
    else:
        print("=" * 60)
        print("WARNING: Running in PRODUCTION mode")
        print("Use a production WSGI server (Gunicorn) instead!")
        print("Example: gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app")
        print("=" * 60)
        app.run(
            debug=False,
            host='0.0.0.0',
            port=5000
        )
