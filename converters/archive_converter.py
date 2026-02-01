"""Archive converter module"""
import zipfile
import tarfile
import os
from pathlib import Path
import shutil

def convert(input_file, output_file, target_format):
    """
    Convert archive files between formats
    Supports: ZIP ↔ TAR
    """
    try:
        input_ext = Path(input_file).suffix.lower().lstrip('.')
        target_format = target_format.lower()
        
        # Create temporary extraction directory
        temp_dir = output_file + '_temp'
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Extract source archive
            if input_ext == 'zip':
                extract_zip(input_file, temp_dir)
            elif input_ext in ['tar', 'gz', 'tgz']:
                extract_tar(input_file, temp_dir)
            else:
                print(f"Unsupported input archive: {input_ext}")
                return False
            
            # Create target archive
            if target_format == 'zip':
                return create_zip(temp_dir, output_file)
            elif target_format in ['tar', 'gz']:
                return create_tar(temp_dir, output_file, target_format)
            else:
                print(f"Unsupported output archive: {target_format}")
                return False
        
        finally:
            # Clean up temp directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    except Exception as e:
        print(f"Archive conversion error: {e}")
        return False

def extract_zip(filepath, extract_to):
    """Extract ZIP archive"""
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def extract_tar(filepath, extract_to):
    """Extract TAR archive"""
    with tarfile.open(filepath, 'r:*') as tar_ref:
        tar_ref.extractall(extract_to)

def create_zip(source_dir, output_file):
    """Create ZIP archive"""
    try:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        return True
    except Exception as e:
        print(f"ZIP creation error: {e}")
        return False

def create_tar(source_dir, output_file, format_type):
    """Create TAR archive"""
    try:
        mode = 'w:gz' if format_type == 'gz' else 'w'
        
        with tarfile.open(output_file, mode) as tarf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    tarf.add(file_path, arcname=arcname)
        return True
    except Exception as e:
        print(f"TAR creation error: {e}")
        return False
