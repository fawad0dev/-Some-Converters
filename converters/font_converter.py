"""Font converter module"""
from pathlib import Path
import os

def convert(input_file, output_file, target_format):
    """
    Convert font files between formats
    Supports: TTF/OTF → WOFF/WOFF2
    Note: Full font conversion requires fonttools
    """
    try:
        input_ext = Path(input_file).suffix.lower().lstrip('.')
        target_format = target_format.lower()
        
        # Check if fonttools is available
        try:
            from fontTools.ttLib import TTFont
            return convert_with_fonttools(input_file, output_file, target_format)
        except ImportError:
            print("fonttools not available, using basic conversion")
            return basic_convert(input_file, output_file)
    
    except Exception as e:
        print(f"Font conversion error: {e}")
        return False

def convert_with_fonttools(input_file, output_file, target_format):
    """Convert font using fonttools"""
    try:
        from fontTools.ttLib import TTFont
        
        # Load font
        font = TTFont(input_file)
        
        # Save in target format
        if target_format in ['woff', 'woff2']:
            font.flavor = target_format
        
        font.save(output_file)
        return True
    
    except Exception as e:
        print(f"Fonttools conversion error: {e}")
        return False

def basic_convert(input_file, output_file):
    """Basic font conversion (just copy)"""
    try:
        import shutil
        shutil.copy2(input_file, output_file)
        return True
    except Exception as e:
        print(f"Basic font conversion error: {e}")
        return False
