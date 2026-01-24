"""
Setup and initialization script for Mealer application.

This script verifies the project structure and initializes necessary components.

Author: Soumik Ranjan Dasgupta
"""

import os
import sys
import csv
from pathlib import Path


def check_project_structure():
    """Verify that all required directories and files exist."""
    print("Checking project structure...")
    
    required_dirs = [
        'app',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/static/images',
        'app/templates',
        'app/utils',
    ]
    
    required_files = [
        'app/__init__.py',
        'app/config.py',
        'app/utils/__init__.py',
        'app/utils/data_parser.py',
        'app/templates/index.html',
        'app/templates/meal_plan.html',
        'run.py',
        'requirements.txt',
        'data.csv',
    ]
    
    # Check directories
    for directory in required_dirs:
        path = Path(directory)
        if not path.exists():
            print(f"  ✗ Missing directory: {directory}")
            return False
        else:
            print(f"  ✓ Found directory: {directory}")
    
    # Check files
    for file in required_files:
        path = Path(file)
        if not path.exists():
            print(f"  ✗ Missing file: {file}")
            return False
        else:
            print(f"  ✓ Found file: {file}")
    
    return True


def verify_data_csv():
    """Verify that data.csv has the correct structure."""
    print("\nVerifying data.csv structure...")
    
    required_columns = [
        'Day', 'Breakfast', 'Lunch', 'Dinner',
        'Calories_Breakfast', 'Calories_Lunch', 'Calories_Dinner',
        'Total_Carb_g', 'Total_Protein_g', 'Total_Fat_g'
    ]
    
    try:
        with open('data.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            if headers != required_columns:
                print("  ✗ CSV headers don't match expected structure")
                print(f"    Expected: {required_columns}")
                print(f"    Got: {headers}")
                return False
            
            row_count = sum(1 for _ in reader)
            print(f"  ✓ CSV structure valid ({row_count} meal days)")
            return True
    
    except FileNotFoundError:
        print("  ✗ data.csv not found")
        return False
    except Exception as e:
        print(f"  ✗ Error reading CSV: {e}")
        return False


def check_svg_image():
    """Check if the SVG image exists."""
    print("\nChecking for SVG image...")
    
    svg_path = 'app/static/images/group_of_friends_febri-adiawarja.svg'
    
    if os.path.exists(svg_path):
        print(f"  ✓ SVG image found: {svg_path}")
        return True
    else:
        print(f"  ✗ SVG image not found: {svg_path}")
        print("    You can provide the image or run: python create_svg_placeholder.py")
        return False


def check_dependencies():
    """Check if required Python packages are installed."""
    print("\nChecking dependencies...")
    
    required_packages = ['flask', 'werkzeug']
    
    try:
        import flask
        import werkzeug
        print("  ✓ Flask installed")
        print("  ✓ Werkzeug installed")
        return True
    except ImportError as e:
        print(f"  ✗ Missing dependency: {e}")
        print("    Run: pip install -r requirements.txt")
        return False


def run_initialization():
    """Run the complete initialization check."""
    print("=" * 60)
    print("Mealer Application Initialization")
    print("=" * 60)
    
    all_checks_passed = True
    
    # Run checks
    if not check_project_structure():
        all_checks_passed = False
    
    if not verify_data_csv():
        all_checks_passed = False
    
    if not check_svg_image():
        all_checks_passed = False
    
    if not check_dependencies():
        all_checks_passed = False
    
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✓ All checks passed! Ready to run the application.")
        print("\nTo start the development server, run:")
        print("  python run.py")
        print("\nThe application will be available at:")
        print("  http://127.0.0.1:5000")
    else:
        print("✗ Some checks failed. Please resolve the issues above.")
        sys.exit(1)
    
    print("=" * 60)


if __name__ == '__main__':
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    run_initialization()
