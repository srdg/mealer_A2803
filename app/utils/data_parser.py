"""
Data parser module for handling meal and nutrition data from CSV.

Author: Soumik Ranjan Dasgupta
"""

import csv
import os
from typing import Dict, List, Any


def get_meal_data(day: int = 1) -> Dict[str, Any]:
    """
    Parse and retrieve meal data for a given day from data.csv.
    
    Args:
        day (int): Day number (1-31). Defaults to 1.
    
    Returns:
        dict: Dictionary containing meal information and nutritional data
              Example: {
                  'breakfast': {'name': str, 'calories': int},
                  'lunch': {'name': str, 'calories': int},
                  'dinner': {'name': str, 'calories': int},
                  'macros': {'carbs': int, 'protein': int, 'fat': int},
                  'total_calories': int
              }
    """
    # Ensure day is within valid range
    day = max(1, min(day, 31))
    
    # Get the path to data.csv (should be in root of Mealer directory)
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'data.csv'
    )
    
    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader, 1):
                if idx == day:
                    return {
                        'breakfast': {
                            'name': row['Breakfast'],
                            'calories': int(row['Calories_Breakfast'])
                        },
                        'lunch': {
                            'name': row['Lunch'],
                            'calories': int(row['Calories_Lunch'])
                        },
                        'dinner': {
                            'name': row['Dinner'],
                            'calories': int(row['Calories_Dinner'])
                        },
                        'macros': {
                            'carbs': int(row['Total_Carb_g']),
                            'protein': int(row['Total_Protein_g']),
                            'fat': int(row['Total_Fat_g'])
                        },
                        'total_calories': (
                            int(row['Calories_Breakfast']) +
                            int(row['Calories_Lunch']) +
                            int(row['Calories_Dinner'])
                        )
                    }
    except FileNotFoundError:
        # Return default data if file not found
        return get_default_meal_data()
    
    # Return day 1 data if day not found
    return get_meal_data(1)


def get_default_meal_data() -> Dict[str, Any]:
    """
    Return default meal data as fallback.
    
    Returns:
        dict: Default meal information
    """
    return {
        'breakfast': {
            'name': 'Vegetable Poha',
            'calories': 350
        },
        'lunch': {
            'name': 'Chicken Pulao',
            'calories': 550
        },
        'dinner': {
            'name': 'Palak Paneer + 1 Roti',
            'calories': 600
        },
        'macros': {
            'carbs': 180,
            'protein': 92,
            'fat': 48
        },
        'total_calories': 1500
    }


def calculate_macro_percentages(macros: Dict[str, int]) -> Dict[str, float]:
    """
    Calculate percentage distribution of macronutrients based on calories.
    
    Assumptions:
    - Carbs: 4 calories per gram
    - Protein: 4 calories per gram
    - Fat: 9 calories per gram
    
    Args:
        macros (dict): Dictionary with keys 'carbs', 'protein', 'fat'
    
    Returns:
        dict: Percentage distribution of macronutrients
    """
    carb_calories = macros['carbs'] * 4
    protein_calories = macros['protein'] * 4
    fat_calories = macros['fat'] * 9
    total = carb_calories + protein_calories + fat_calories
    
    if total == 0:
        return {'carbs': 0, 'protein': 0, 'fat': 0}
    
    return {
        'carbs': round((carb_calories / total) * 100, 1),
        'protein': round((protein_calories / total) * 100, 1),
        'fat': round((fat_calories / total) * 100, 1)
    }
