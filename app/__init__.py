"""
Main Flask application module for Mealer - A meal planning web application.

This module serves as the router and entry point for the application.
All business logic is implemented in subdirectories following industry standards.

Author: Soumik Ranjan Dasgupta
"""

from flask import Flask, render_template, jsonify
from datetime import datetime
from app.utils.data_parser import get_meal_data, calculate_macro_percentages
from app.config import DevelopmentConfig


def create_app():
    """
    Application factory for creating and configuring the Flask app.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Load configuration
    app.config.from_object(DevelopmentConfig)
    
    # Additional Flask configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSON_ENSURE_ASCII'] = False  # Support Unicode characters
    
    # Register routes
    register_routes(app)
    
    return app


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
        return render_template('index.html')
    
    @app.route('/meal-plan')
    def meal_plan():
        """
        Meal plan page route.
        Fetches meal data and renders the meal planning interface.
        """
        # Get meal data for day 1 (can be extended to get current day or user preference)
        meal_data = get_meal_data(day=1)
        macro_percentages = calculate_macro_percentages(meal_data['macros'])
        
        return render_template(
            'meal_plan.html',
            meal_data=meal_data,
            macro_percentages=macro_percentages,
            today=datetime.now().strftime('%Y-%m-%d')
        )
    
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
            meal_data = get_meal_data(day=day)
            macro_percentages = calculate_macro_percentages(meal_data['macros'])
            
            return jsonify({
                'success': True,
                'data': meal_data,
                'macros_percentage': macro_percentages
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400


if __name__ == '__main__':
    app = create_app()
    # Development server with debug mode
    app.run(debug=True, host='127.0.0.1', port=5000)
