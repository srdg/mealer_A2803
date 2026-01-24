"""
Main Flask application module for Mealer - A meal planning web application.

This module serves as the router and entry point for the application.
All business logic is implemented in subdirectories following industry standards.

Author: Soumik Ranjan Dasgupta
"""

import os
import logging
from flask import Flask, render_template, jsonify, request
from datetime import datetime
from app.utils.data_parser import get_meal_data, calculate_macro_percentages
from app.config import DevelopmentConfig, ProductionConfig


def create_app(config=None):
    """
    Application factory for creating and configuring the Flask app.
    
    Args:
        config: Configuration class to use. Defaults to environment-based selection.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Load configuration based on environment or argument
    if config is None:
        env = os.getenv('FLASK_ENV', 'production')
        config = DevelopmentConfig if env == 'development' else ProductionConfig
    
    app.config.from_object(config)
    
    # Additional Flask configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSON_ENSURE_ASCII'] = False  # Support Unicode characters
    
    # Configure logging for production
    if not app.debug:
        configure_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register routes
    register_routes(app)
    
    # Add security headers middleware
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    return app


def configure_logging(app: Flask):
    """
    Configure logging for production environment.
    
    Args:
        app (Flask): Flask application instance
    """
    # Set up file logging
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    handler = logging.FileHandler(os.path.join(log_dir, 'mealer.log'))
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Mealer application started')


def register_error_handlers(app: Flask):
    """
    Register error handlers for common HTTP errors.
    
    Args:
        app (Flask): Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        app.logger.warning(f'Bad request: {request.url}')
        return jsonify({
            'success': False,
            'error': 'Bad request'
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        app.logger.warning(f'Not found: {request.url}')
        return jsonify({
            'success': False,
            'error': 'Page not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        app.logger.error(f'Internal server error: {str(error)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


def register_routes(app: Flask):
    """
    Register all application routes.
    
    Args:
        app (Flask): Flask application instance
    """
    
    @app.route('/')
    def index():
        """
        Landing page route.
        Renders the main landing page with hero section and CTA button.
        """
        try:
            return render_template('index.html')
        except Exception as e:
            app.logger.error(f'Error rendering index: {str(e)}')
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/meal-plan')
    def meal_plan():
        """
        Meal plan page route.
        Fetches meal data and renders the meal planning interface.
        """
        try:
            # Get meal data for day 1 (can be extended to get current day or user preference)
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
        """
        API endpoint to fetch meal data for a specific day.
        
        Args:
            day (int): Day number (1-31)
        
        Returns:
            JSON: Meal data and macro information
        """
        try:
            # Validate day parameter
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
        """
        Health check endpoint for monitoring.
        
        Returns:
            JSON: Health status
        """
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat()
        }), 200


if __name__ == '__main__':
    app = create_app()
    # Development server with debug mode

    app.run(debug=True, host='127.0.0.1', port=5000)
