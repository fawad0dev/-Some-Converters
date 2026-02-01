"""Video converter module - uses ffmpeg"""
import subprocess
import os
from pathlib import Path

def convert(input_file, output_file, target_format):
    """
    Convert video files between formats
    Supports: MP4, MKV, AVI, MOV, WEBM, FLV, GIF
    """
    try:
        # Check if ffmpeg is available
        if not is_ffmpeg_available():
            print("ffmpeg not available")
            return False
        
        # Special handling for GIF
        if target_format.lower() == 'gif':
            return convert_to_gif(input_file, output_file)
        
        # Use ffmpeg for conversion
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-y',  # Overwrite output file
            '-c:v', 'libx264',  # Video codec
            '-c:a', 'aac',  # Audio codec
            '-strict', 'experimental',
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_file):
            return True
        else:
            print(f"ffmpeg error: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"Video conversion error: {e}")
        return False

def convert_to_gif(input_file, output_file):
    """Convert video to GIF"""
    try:
        # Generate palette for better quality
        palette_file = output_file.replace('.gif', '_palette.png')
        
        # Generate palette
        cmd_palette = [
            'ffmpeg',
            '-i', input_file,
            '-vf', 'fps=10,scale=480:-1:flags=lanczos,palettegen',
            '-y',
            palette_file
        ]
        
        subprocess.run(cmd_palette, capture_output=True)
        
        # Create GIF
        cmd_gif = [
            'ffmpeg',
            '-i', input_file,
            '-i', palette_file,
            '-filter_complex', 'fps=10,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse',
            '-y',
            output_file
        ]
        
        result = subprocess.run(cmd_gif, capture_output=True, text=True)
        
        # Clean up palette
        if os.path.exists(palette_file):
            os.remove(palette_file)
        
        return result.returncode == 0 and os.path.exists(output_file)
    
    except Exception as e:
        print(f"GIF conversion error: {e}")
        return False

def is_ffmpeg_available():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
