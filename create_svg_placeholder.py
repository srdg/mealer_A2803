"""
Placeholder SVG generator for Mealer application.

This script generates the group_of_friends_febri-adiawarja.svg file if it doesn't exist.

Author: Soumik Ranjan Dasgupta
"""

import os


def create_placeholder_svg():
    """
    Create a placeholder SVG image if the original doesn't exist.
    
    Returns:
        bool: True if file was created, False otherwise
    """
    svg_path = os.path.join(
        os.path.dirname(__file__),
        'app',
        'static',
        'images',
        'group_of_friends_febri-adiawarja.svg'
    )
    
    if os.path.exists(svg_path):
        print(f"SVG file already exists at: {svg_path}")
        return False
    
    # Create placeholder SVG
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 80" width="200" height="80">
    <!-- Group of friends placeholder icon -->
    <rect width="200" height="80" fill="#f9f7f4"/>
    
    <!-- Friend 1 -->
    <circle cx="40" cy="25" r="8" fill="#9a5017"/>
    <path d="M 35 35 Q 40 40 45 35" stroke="#9a5017" stroke-width="3" fill="none" stroke-linecap="round"/>
    
    <!-- Friend 2 -->
    <circle cx="100" cy="20" r="8" fill="#9a5017"/>
    <path d="M 95 30 Q 100 35 105 30" stroke="#9a5017" stroke-width="3" fill="none" stroke-linecap="round"/>
    
    <!-- Friend 3 -->
    <circle cx="160" cy="25" r="8" fill="#9a5017"/>
    <path d="M 155 35 Q 160 40 165 35" stroke="#9a5017" stroke-width="3" fill="none" stroke-linecap="round"/>
    
    <!-- Connection line -->
    <path d="M 48 35 L 92 30 L 152 35" stroke="#9a5017" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.6"/>
    
    <!-- Text -->
    <text x="100" y="65" font-size="14" font-weight="bold" text-anchor="middle" fill="#9a5017">
        Mealer
    </text>
</svg>'''
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(svg_path), exist_ok=True)
    
    # Write SVG file
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"Placeholder SVG created at: {svg_path}")
    return True


if __name__ == '__main__':
    create_placeholder_svg()
