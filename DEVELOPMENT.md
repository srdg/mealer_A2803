"""
# DEVELOPMENT.md - Development Guide for Mealer

Author: Soumik Ranjan Dasgupta

---

## Quick Start

### 1. Initial Setup
```bash
# Navigate to the project directory
cd Mealer

# Create a placeholder SVG (if you don't have the original)
python create_svg_placeholder.py

# Run the setup verification
python setup.py

# Install dependencies
pip install -r requirements.txt

# Start the development server
python run.py
```

### 2. Access the Application
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## Project Architecture

### Directory Structure Explanation

```
app/
├── __init__.py          # Flask app factory and route definitions
├── config.py            # Configuration classes (Dev, Prod, Test)
├── static/              # Static files served to clients
│   ├── css/             # Custom stylesheets (currently using Tailwind CDN)
│   ├── js/              # Client-side JavaScript
│   └── images/          # Image assets
├── templates/           # Jinja2 HTML templates
│   ├── index.html      # Landing page
│   └── meal_plan.html  # Meal planning dashboard
└── utils/               # Utility modules and helpers
    ├── __init__.py
    └── data_parser.py  # CSV parsing and data processing
```

### Code Organization Principles

1. **Separation of Concerns**: Routes are in `app/__init__.py`, business logic in `utils/`
2. **Configuration**: All config in dedicated `config.py`
3. **Reusability**: Common functions in `utils/` package
4. **Scalability**: Easy to add more utilities and routes

---

## Core Components

### 1. Flask Application (`app/__init__.py`)

**Purpose**: Define routes and act as the entry point

**Key Functions**:
- `create_app()` - Application factory pattern
- `register_routes()` - Centralized route registration

**Routes**:
- `GET /` - Landing page
- `GET /meal-plan` - Meal planning dashboard
- `GET /api/meal-data/<day>` - API endpoint for meal data

### 2. Data Parser (`app/utils/data_parser.py`)

**Purpose**: Handle CSV parsing and data processing

**Key Functions**:
- `get_meal_data(day)` - Fetch meal info for a specific day
- `calculate_macro_percentages(macros)` - Compute macro distribution
- `get_default_meal_data()` - Fallback data

**Formula for Macro Percentages**:
```
Carb Calories = Carbs (g) × 4
Protein Calories = Protein (g) × 4
Fat Calories = Fat (g) × 9

Percentage = (Meal Calories / Total Calories) × 100
```

### 3. Frontend Templates

#### index.html - Landing Page
- Hero section with background gradient
- Smooth scroll to meal plan on button click
- Header with logo and application name
- Responsive design using Tailwind CSS

#### meal_plan.html - Meal Dashboard
- Two-column layout (left: meals & macros, right: calendar)
- Three meal cards with calorie badges
- Three macro cards with progress bars
- Flatpickr calendar integration
- Fully responsive grid system

### 4. Configuration (`app/config.py`)

Three configuration classes for different environments:
- `Config` - Base configuration with common settings
- `DevelopmentConfig` - Debug enabled, verbose logging
- `ProductionConfig` - Optimized for production
- `TestingConfig` - For running tests

---

## Technologies & Dependencies

### Backend
- **Flask 3.1.2** - Lightweight WSGI web framework
- **Python 3.8+** - Programming language

### Frontend
- **Tailwind CSS** - Utility-first CSS framework (CDN)
- **Flatpickr** - Lightweight JavaScript date picker (CDN)
- **Vanilla JavaScript** - No build tools needed

### Data
- **CSV Format** - Simple data storage (can be upgraded to database)

---

## Extending the Application

### 1. Adding a New Route

```python
# In app/__init__.py, add to register_routes():

@app.route('/new-feature')
def new_feature():
    """Description of the new feature."""
    return render_template('new_feature.html', data=some_data)
```

### 2. Adding a New Utility Function

```python
# In app/utils/data_parser.py

def new_utility_function(param):
    """
    Description of what this function does.
    
    Args:
        param: Description of parameter
    
    Returns:
        type: Description of return value
    """
    # Implementation
    pass
```

### 3. Adding Database Support

```python
# Install Flask-SQLAlchemy
pip install flask-sqlalchemy

# In app/__init__.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Create models
class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, required=True)
    # ... more fields
```

### 4. Adding User Authentication

```python
# Install Flask-Login
pip install flask-login

# Use Flask-Login decorators on protected routes
from flask_login import login_required, current_user

@app.route('/user-meals')
@login_required
def user_meals():
    return render_template('user_meals.html', user=current_user)
```

---

## Testing

### Manual Testing Checklist
- [ ] Landing page loads correctly
- [ ] View Plan button scrolls to meal section
- [ ] Meal cards display correct data
- [ ] Calendar picker is interactive
- [ ] Macro percentages calculate correctly
- [ ] Responsive design on mobile (320px)
- [ ] Responsive design on tablet (768px)
- [ ] Responsive design on desktop (1920px)
- [ ] All fonts readable and properly sized

### Unit Testing Example

```python
# Create test file: tests/test_data_parser.py

import unittest
from app.utils.data_parser import calculate_macro_percentages

class TestDataParser(unittest.TestCase):
    def test_macro_percentages(self):
        macros = {'carbs': 180, 'protein': 92, 'fat': 48}
        result = calculate_macro_percentages(macros)
        self.assertTrue(all(0 <= v <= 100 for v in result.values()))

if __name__ == '__main__':
    unittest.main()
```

---

## Debugging Tips

### 1. Enable Flask Debug Toolbar
```python
# In app/config.py
class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

# In run.py
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)
```

### 2. Check Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### 3. Browser DevTools
- Chrome/Firefox: Press F12
- Check Network tab for API calls
- Check Console for JavaScript errors

---

## Performance Optimization

### Current Optimizations
1. CSS loaded from CDN (cached by browser)
2. Minimal JavaScript (no heavy frameworks)
3. CSV parsing cached per request
4. Static files served by Flask with proper headers

### Future Optimizations
1. Implement caching (Flask-Caching)
2. Minify CSS and JavaScript
3. Use PostgreSQL instead of CSV
4. Add gzip compression
5. Implement lazy loading for images

---

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints (Optional)
- Write docstrings for all functions
- Keep functions small and focused

### HTML
- Use semantic HTML5 elements
- Include alt text for images
- Proper heading hierarchy (h1 > h2 > h3)

### CSS (Tailwind)
- Use utility classes (not custom CSS)
- Follow responsive-first approach
- Use CSS variables for colors
- Avoid inline styles (use Tailwind classes)

### JavaScript
- Use const/let instead of var
- Add meaningful comments
- Keep functions pure when possible
- Use event delegation for dynamic elements

---

## Deployment Checklist

Before deploying to production:
- [ ] Set DEBUG = False in config
- [ ] Use a production WSGI server (Gunicorn, Waitress)
- [ ] Set up environment variables for secrets
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS if needed
- [ ] Set up logging to files
- [ ] Configure database backups
- [ ] Set up monitoring and alerts
- [ ] Load test the application
- [ ] Security audit (SQL injection, XSS, CSRF)

### Deployment Command
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 'app:create_app()'
```

---

## Troubleshooting Common Issues

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "FileNotFoundError: data.csv"
**Solution**: Ensure data.csv is in the root Mealer directory

### Issue: SVG image not displaying
**Solution**: Run `python create_svg_placeholder.py` or provide the actual image

### Issue: Calendar not appearing
**Solution**: Check browser console for JavaScript errors, verify Flatpickr CDN is accessible

### Issue: Meal data shows incorrect values
**Solution**: Verify data.csv format and that CSV library is parsing it correctly

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/)
- [Flatpickr Documentation](https://flatpickr.js.org/)
- [Python PEP 8 Style Guide](https://pep8.org/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with proper comments
4. Test thoroughly
5. Commit with clear messages: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

## License & Credits

Created by: Soumik Ranjan Dasgupta
Date: January 2026

---
"""
