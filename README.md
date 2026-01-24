"""
README - Mealer: Personal Meal Planning Assistant

Author: Soumik Ranjan Dasgupta
Created: January 2026

---

## Overview
Mealer is a responsive web application for personal meal planning with nutritional tracking.
The application features a clean landing page and an interactive meal plan dashboard with
real-time calorie and macronutrient tracking.

## Features
- **Responsive Design**: Fully responsive layout for desktop, tablet, and mobile devices
- **Landing Page**: Hero section with call-to-action button
- **Meal Plan Dashboard**: Two-column layout with meal cards and nutritional breakdown
- **Calendar Integration**: Flatpickr date picker for selecting meal plans
- **Macro Tracking**: Real-time carbohydrates, protein, and fat percentage calculations
- **Smooth Animations**: Hover effects and smooth transitions throughout the app

## Project Structure

```
Mealer/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory and route registration
│   ├── static/                  # Static files
│   │   ├── css/                 # CSS stylesheets
│   │   ├── js/                  # JavaScript files
│   │   └── images/              # Image assets
│   ├── templates/               # HTML templates
│   │   ├── index.html          # Landing page
│   │   └── meal_plan.html      # Meal plan dashboard
│   └── utils/                   # Utility modules
│       ├── __init__.py
│       └── data_parser.py      # CSV parsing and data processing
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
└── data.csv                     # Meal and nutrition data

```

## Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Install Dependencies
```bash
cd Mealer
pip install -r requirements.txt
```

### 3. Place Image Asset
Ensure the SVG image `group_of_friends_febri-adiawarja.svg` is placed in:
```
app/static/images/group_of_friends_febri-adiawarja.svg
```

### 4. Verify CSV Data
The `data.csv` file should be in the root directory with the following columns:
- Day, Breakfast, Lunch, Dinner
- Calories_Breakfast, Calories_Lunch, Calories_Dinner
- Total_Carb_g, Total_Protein_g, Total_Fat_g

## Running the Application

### Development Server
```bash
python run.py
```

The application will be available at: `http://127.0.0.1:5000`

### Production Deployment
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:create_app()
```

## Application Routes

- **`/`** - Landing page with hero section and CTA button
- **`/meal-plan`** - Main meal plan dashboard with calendar and nutritional info
- **`/api/meal-data/<day>`** - API endpoint to fetch meal data for a specific day (JSON)

## Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript** - Client-side interactivity
- **Flatpickr** - Lightweight date picker library

### Backend
- **Flask** - Python web framework
- **Python 3** - Programming language

### Data
- **CSV** - Data storage format

## Code Standards

### File Headers
Every Python and HTML file contains a header comment:
```
"""
[Module Description]

Author: [Author Name]
"""
```

### Documentation
- Comprehensive docstrings for all functions
- Inline comments for complex logic
- Clear variable naming conventions

### Responsiveness
The application uses Tailwind CSS breakpoints for responsive design:
- Mobile: 320px - 640px
- Tablet: 641px - 1024px
- Desktop: 1025px+

## Color Scheme
- **Primary**: #9a5017 (Brown/Tan)
- **Background Light**: #f9f7f4 (Cream)
- **Carbs**: #fbbf24 (Amber)
- **Protein**: #ef4444 (Red)
- **Fat**: #3b82f6 (Blue)

## Extension Points

### Adding More Days
Modify the day parameter when calling `get_meal_data()` in `app/__init__.py`:
```python
meal_data = get_meal_data(day=day_number)  # day_number from 1-31
```

### Adding New Nutritional Fields
Edit the CSV parser in `app/utils/data_parser.py` to handle additional fields.

### Custom Styling
Modify inline styles in templates or create custom CSS in `app/static/css/`.

## Troubleshooting

### CSV File Not Found
- Ensure `data.csv` is in the root Mealer directory
- Check file permissions and encoding (should be UTF-8)

### Image Not Loading
- Verify the SVG file exists in `app/static/images/`
- Check the filename matches exactly in the template

### Calendar Not Appearing
- Ensure Flatpickr CDN link is accessible
- Check browser console for JavaScript errors

## API Usage Example

Fetch meal data for day 15:
```bash
curl http://127.0.0.1:5000/api/meal-data/15
```

Response:
```json
{
  "success": true,
  "data": {
    "breakfast": {"name": "...", "calories": 380},
    "lunch": {"name": "...", "calories": 550},
    "dinner": {"name": "...", "calories": 570},
    "macros": {"carbs": 170, "protein": 95, "fat": 48},
    "total_calories": 1500
  },
  "macros_percentage": {"carbs": 45.3, "protein": 25.3, "fat": 29.4}
}
```

## Performance Considerations

- CSS is loaded from CDN (Tailwind, Flatpickr)
- Minimal JavaScript for optimal page load
- Static pages served efficiently by Flask
- CSV parsing is cached per request

## Browser Support

- Chrome/Chromium (Latest)
- Firefox (Latest)
- Safari (Latest)
- Edge (Latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Future Enhancements

- User authentication and profiles
- Personalized meal preferences
- Shopping list generation
- Recipe details and cooking instructions
- Weekly meal planning
- PDF export functionality
- Mobile app integration

## License

This project is provided as-is for educational purposes.

## Contact & Support

For issues or questions, contact: Soumik Ranjan Dasgupta

---
"""
