"""
# API_REFERENCE.md - API Documentation for Mealer

Author: Soumik Ranjan Dasgupta

---

## Overview

The Mealer application provides RESTful endpoints for accessing meal and nutritional data.

Base URL: `http://127.0.0.1:5000` (Development)

---

## Endpoints

### 1. Landing Page

**Endpoint**: `GET /`

**Description**: Returns the main landing page with hero section

**Response**: HTML page
- Status: `200 OK`
- Content-Type: `text/html`

**Example**:
```bash
curl http://127.0.0.1:5000/
```

---

### 2. Meal Plan Page

**Endpoint**: `GET /meal-plan`

**Description**: Returns the meal planning dashboard with calendar and nutritional info

**Response**: HTML page with embedded data
- Status: `200 OK`
- Content-Type: `text/html`

**Query Parameters**: None

**Example**:
```bash
curl http://127.0.0.1:5000/meal-plan
```

**Rendered Variables**:
- `meal_data`: Dictionary containing meal information
- `macro_percentages`: Dictionary with macro distribution percentages
- `today`: Today's date in YYYY-MM-DD format

---

### 3. Get Meal Data API

**Endpoint**: `GET /api/meal-data/<day>`

**Description**: Returns meal and nutritional data for a specific day in JSON format

**Parameters**:
- `day` (integer, required): Day number (1-31)

**Response**:
```json
{
  "success": true,
  "data": {
    "breakfast": {
      "name": "string",
      "calories": integer
    },
    "lunch": {
      "name": "string",
      "calories": integer
    },
    "dinner": {
      "name": "string",
      "calories": integer
    },
    "macros": {
      "carbs": integer,
      "protein": integer,
      "fat": integer
    },
    "total_calories": integer
  },
  "macros_percentage": {
    "carbs": float,
    "protein": float,
    "fat": float
  }
}
```

**Status Codes**:
- `200 OK` - Successfully retrieved meal data
- `400 Bad Request` - Invalid day number or server error

**Example**:
```bash
# Get meal data for day 1
curl http://127.0.0.1:5000/api/meal-data/1

# Get meal data for day 15
curl http://127.0.0.1:5000/api/meal-data/15

# Get meal data for day 31
curl http://127.0.0.1:5000/api/meal-data/31
```

**Response Example** (Day 1):
```json
{
  "success": true,
  "data": {
    "breakfast": {
      "name": "Vegetable Poha",
      "calories": 350
    },
    "lunch": {
      "name": "Chicken Pulao",
      "calories": 550
    },
    "dinner": {
      "name": "Palak Paneer + 1 Roti",
      "calories": 600
    },
    "macros": {
      "carbs": 180,
      "protein": 92,
      "fat": 48
    },
    "total_calories": 1500
  },
  "macros_percentage": {
    "carbs": 47.8,
    "protein": 24.5,
    "fat": 27.7
  }
}
```

---

## Request Examples

### Using cURL

```bash
# Get meal data for day 5
curl -X GET "http://127.0.0.1:5000/api/meal-data/5" \
  -H "Content-Type: application/json"
```

### Using Python (requests library)

```python
import requests

# Fetch meal data for day 10
response = requests.get('http://127.0.0.1:5000/api/meal-data/10')
data = response.json()

print(f"Total Calories: {data['data']['total_calories']}")
print(f"Breakfast: {data['data']['breakfast']['name']}")
```

### Using JavaScript (fetch API)

```javascript
// Fetch meal data for day 7
fetch('http://127.0.0.1:5000/api/meal-data/7')
  .then(response => response.json())
  .then(data => {
    console.log('Total Calories:', data.data.total_calories);
    console.log('Breakfast:', data.data.breakfast.name);
  })
  .catch(error => console.error('Error:', error));
```

### Using JavaScript (jQuery)

```javascript
$.get('/api/meal-data/12', function(data) {
  console.log('Meal data:', data.data);
});
```

---

## Data Validation

### Day Number Validation
- **Valid Range**: 1-31
- **Invalid Input**: Values outside this range will default to day 1
- **Type**: Integer

### Response Codes
- **200 OK**: Request successful
- **400 Bad Request**: Invalid input or server error
- **500 Internal Server Error**: Unexpected server error

---

## Data Structures

### Meal Object
```json
{
  "breakfast": {
    "name": "Vegetable Poha",
    "calories": 350
  },
  "lunch": {
    "name": "Chicken Pulao",
    "calories": 550
  },
  "dinner": {
    "name": "Palak Paneer + 1 Roti",
    "calories": 600
  }
}
```

### Macro Object
```json
{
  "carbs": 180,
  "protein": 92,
  "fat": 48
}
```

### Macro Percentage Object
```json
{
  "carbs": 47.8,
  "protein": 24.5,
  "fat": 27.7
}
```

---

## Calculation Formulas

### Macro Percentages

The application uses standard macronutrient calorie values:
- **Carbohydrates**: 4 calories per gram
- **Protein**: 4 calories per gram
- **Fat**: 9 calories per gram

**Calculation**:
```
Carb Calories = carbs_grams × 4
Protein Calories = protein_grams × 4
Fat Calories = fat_grams × 9

Total Calories from Macros = Carb Calories + Protein Calories + Fat Calories

Carb Percentage = (Carb Calories / Total Calories) × 100
Protein Percentage = (Protein Calories / Total Calories) × 100
Fat Percentage = (Fat Calories / Total Calories) × 100
```

**Example** (Day 1):
```
Carbs: 180g × 4 = 720 calories
Protein: 92g × 4 = 368 calories
Fat: 48g × 9 = 432 calories
Total: 720 + 368 + 432 = 1520 calories

Carb %: (720 / 1520) × 100 = 47.4%
Protein %: (368 / 1520) × 100 = 24.2%
Fat %: (432 / 1520) × 100 = 28.4%
```

---

## Rate Limiting

Currently, the API has **no rate limiting**. For production, consider implementing:
- IP-based rate limiting
- User-based rate limiting
- Global rate limiting

---

## CORS & Security

### Current Configuration
- CORS is enabled for all origins (development mode)
- No authentication required (development mode)

### Production Recommendations
1. Restrict CORS to specific domains
2. Implement authentication (JWT, OAuth)
3. Add request validation
4. Enable HTTPS
5. Implement rate limiting

---

## Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": "Error message describing the issue"
}
```

### Common Errors

| Error | Status | Cause |
|-------|--------|-------|
| File not found | 400 | data.csv missing |
| Invalid day | 400 | Day < 1 or > 31 |
| Parse error | 400 | CSV format issue |
| Server error | 500 | Unexpected exception |

---

## Testing the API

### Using Postman

1. Open Postman
2. Create a new GET request
3. Enter URL: `http://127.0.0.1:5000/api/meal-data/1`
4. Click "Send"
5. View the JSON response

### Automated Testing

```bash
# Install httpie (HTTP client)
pip install httpie

# Test the API
http GET http://127.0.0.1:5000/api/meal-data/5
```

---

## Versioning

Current API Version: **v1** (Implied)

Future versions may be implemented with:
- `/api/v2/meal-data/<day>`
- `/api/v2/users/<user_id>/meals`
- `/api/v2/recipes/`

---

## Deprecation Policy

Breaking changes will be announced 6 months in advance.

---

## Future API Enhancements

Planned features:
- [ ] User authentication
- [ ] Personal meal preferences
- [ ] Shopping list generation
- [ ] Recipe details endpoint
- [ ] Weekly meal planning
- [ ] Batch data fetching
- [ ] Search functionality

---

## Support

For API issues or questions, refer to:
1. [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
2. [README.md](README.md) - Project overview
3. Source code: `/app/__init__.py`

---

Author: Soumik Ranjan Dasgupta
Last Updated: January 2026
"""
