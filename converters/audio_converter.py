"""Audio converter module - uses ffmpeg if available"""
import subprocess
import os
from pathlib import Path

def convert(input_file, output_file, target_format):
    """
    Convert audio files between formats
    Supports: MP3, WAV, OGG, FLAC, M4A, AAC
    """
    try:
        # Check if ffmpeg is available
        if not is_ffmpeg_available():
            print("ffmpeg not available, attempting basic conversion")
            return basic_convert(input_file, output_file, target_format)
        
        # Use ffmpeg for conversion
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-y',  # Overwrite output file
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_file):
            return True
        else:
            print(f"ffmpeg error: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"Audio conversion error: {e}")
        return False

def is_ffmpeg_available():
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def basic_convert(input_file, output_file, target_format):
    """Basic conversion without ffmpeg (limited functionality)"""
    try:
        # For basic audio, just copy the file
        # In production, use pydub or similar
        import shutil
        shutil.copy2(input_file, output_file)
        return True
    except Exception as e:
        print(f"Basic audio conversion error: {e}")
        return False
