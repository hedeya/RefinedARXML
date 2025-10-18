#!/usr/bin/env python3
"""
Create a simple icon for the ARXML Editor
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for the application"""
    # Create a 256x256 image with transparent background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a blue background circle
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=(52, 144, 220, 255), outline=(30, 100, 150, 255), width=4)
    
    # Draw XML-like brackets
    bracket_width = 8
    bracket_height = 80
    bracket_x = size // 2 - bracket_width // 2
    bracket_y = size // 2 - bracket_height // 2
    
    # Left bracket
    draw.rectangle([bracket_x, bracket_y, bracket_x + bracket_width, bracket_y + bracket_height], 
                   fill=(255, 255, 255, 255))
    draw.rectangle([bracket_x, bracket_y, bracket_x + bracket_width * 2, bracket_y + bracket_width], 
                   fill=(255, 255, 255, 255))
    draw.rectangle([bracket_x, bracket_y + bracket_height - bracket_width, 
                   bracket_x + bracket_width * 2, bracket_y + bracket_height], 
                   fill=(255, 255, 255, 255))
    
    # Right bracket
    right_bracket_x = bracket_x + 30
    draw.rectangle([right_bracket_x, bracket_y, right_bracket_x + bracket_width, bracket_y + bracket_height], 
                   fill=(255, 255, 255, 255))
    draw.rectangle([right_bracket_x - bracket_width, bracket_y, right_bracket_x + bracket_width, bracket_y + bracket_width], 
                   fill=(255, 255, 255, 255))
    draw.rectangle([right_bracket_x - bracket_width, bracket_y + bracket_height - bracket_width, 
                   right_bracket_x + bracket_width, bracket_y + bracket_height], 
                   fill=(255, 255, 255, 255))
    
    # Draw "AR" text in the center
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text = "AR"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 + 10
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save as ICO file
    img.save('arxml_editor.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("Icon created: arxml_editor.ico")

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw, ImageFont
        create_icon()
    except ImportError:
        print("PIL not available, creating a simple placeholder icon...")
        # Create a simple text file as placeholder
        with open('arxml_editor.ico', 'w') as f:
            f.write("Icon placeholder")