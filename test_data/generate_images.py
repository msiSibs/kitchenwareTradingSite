#!/usr/bin/env python3
"""
Test Image Generator
Generates sample test images for marketplace testing.
Run this script to create sample images in the test_data/images directory.
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

# Test data - product images to generate
TEST_IMAGES = [
    {
        "filename": "dutch_oven_red.png",
        "title": "Dutch Oven",
        "color": (192, 0, 0),  # Red
        "description": "Cast Iron Dutch Oven"
    },
    {
        "filename": "frying_pan_steel.png",
        "title": "Frying Pan",
        "color": (192, 192, 192),  # Silver/Steel
        "description": "Stainless Steel Pan"
    },
    {
        "filename": "mixer_white.png",
        "title": "Stand Mixer",
        "color": (255, 255, 255),  # White
        "description": "KitchenAid Mixer"
    },
    {
        "filename": "knife_set.png",
        "title": "Knife Set",
        "color": (64, 64, 64),  # Dark Gray
        "description": "Professional Knives"
    },
    {
        "filename": "baking_pan_glass.png",
        "title": "Baking Pan",
        "color": (200, 220, 255),  # Light Blue
        "description": "Pyrex Baking Pan"
    },
    {
        "filename": "cutting_board.png",
        "title": "Cutting Board",
        "color": (139, 69, 19),  # Brown
        "description": "Wooden Cutting Board"
    },
    {
        "filename": "measuring_cups.png",
        "title": "Measuring Cups",
        "color": (100, 149, 237),  # Cornflower Blue
        "description": "Stainless Steel Measures"
    },
    {
        "filename": "blender.png",
        "title": "Blender",
        "color": (0, 0, 0),  # Black
        "description": "High-Speed Blender"
    }
]

def create_test_image(filename, title, color, description):
    """Create a test image with the given specifications."""
    # Create image with gradient background
    width, height = 500, 500
    img = Image.new('RGB', (width, height), color)
    
    # Add a gradient effect
    draw = ImageDraw.Draw(img)
    for i in range(height):
        # Create a gradient by adjusting brightness
        factor = 1 - (i / height) * 0.3
        r = int(color[0] * factor)
        g = int(color[1] * factor)
        b = int(color[2] * factor)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Add text
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fall back if not available
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        desc_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        title_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
    
    # Draw white text
    text_color = (255, 255, 255)
    
    # Center title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 180), title, font=title_font, fill=text_color)
    
    # Center description
    desc_bbox = draw.textbbox((0, 0), description, font=desc_font)
    desc_width = desc_bbox[2] - desc_bbox[0]
    desc_x = (width - desc_width) // 2
    draw.text((desc_x, 280), description, font=desc_font, fill=text_color)
    
    # Save image
    img.save(filename)
    print(f"✓ Created {os.path.basename(filename)}")

def main():
    """Generate all test images."""
    images_dir = Path(__file__).parent / "images"
    images_dir.mkdir(exist_ok=True)
    
    print("🖼️  Generating test images...\n")
    
    for image_data in TEST_IMAGES:
        filepath = images_dir / image_data["filename"]
        create_test_image(
            str(filepath),
            image_data["title"],
            image_data["color"],
            image_data["description"]
        )
    
    print(f"\n✅ Successfully created {len(TEST_IMAGES)} test images in {images_dir}")
    print("\nYou can now use these images for testing:")
    print("  - Upload them as item listings in the marketplace")
    print("  - Test image validation (file types, sizes)")
    print("  - Test image display and gallery functionality")

if __name__ == "__main__":
    main()
