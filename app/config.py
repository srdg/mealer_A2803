"""
Application configuration module for Mealer.

Author: Soumik Ranjan Dasgupta
"""

import os


class Config:
    """Base configuration class for Mealer application."""
    
    # Flask configuration
    DEBUG = False
    TESTING = False
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # File paths
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATA_CSV_PATH = os.path.join(BASE_DIR, 'data.csv')
    
    # Theme colors
    PRIMARY_COLOR = '#9a5017'
    SECONDARY_COLOR = '#f9f7f4'
    

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Ensure all security settings are strict
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = 'https'
    

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False
