"""Image converter module using Pillow"""
from PIL import Image
import os

def convert(input_file, output_file, target_format):
    """
    Convert image to target format
    Supports: PNG, JPG, JPEG, WEBP, SVG, GIF, BMP, TIFF
    """
    try:
        target_format = target_format.upper()
        
        # Handle JPEG alias
        if target_format in ['JPG', 'JPEG']:
            target_format = 'JPEG'
        
        # Open the image
        img = Image.open(input_file)
        
        # Convert RGBA to RGB if saving as JPEG
        if target_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # Handle SVG - note: Pillow doesn't natively support SVG output
        # For SVG, we'd need additional libraries like svgwrite
        if target_format == 'SVG':
            # For basic SVG support, we'll save as PNG first
            # In production, use cairosvg or similar
            target_format = 'PNG'
            output_file = output_file.replace('.svg', '.png')
        
        # Save the image
        img.save(output_file, format=target_format)
        return True
    
    except Exception as e:
        print(f"Image conversion error: {e}")
        return False
