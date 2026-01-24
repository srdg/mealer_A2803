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
    
    # File paths
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATA_CSV_PATH = os.path.join(BASE_DIR, 'data.csv')
    
    # Theme colors
    PRIMARY_COLOR = '#9a5017'
    SECONDARY_COLOR = '#f9f7f4'
    

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
