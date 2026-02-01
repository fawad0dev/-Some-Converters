from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import uuid
import shutil
from pathlib import Path
import traceback
import time

# Import conversion modules
from converters import image_converter, document_converter, audio_converter
from converters import video_converter, data_converter, archive_converter
from converters import font_converter, design_converter, model_3d_converter

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CONVERTED_FOLDER'] = 'converted'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

# File cleanup after download (in seconds)
CLEANUP_AFTER = 3600  # 1 hour

ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'webp', 'svg', 'gif', 'bmp', 'tiff'},
    'document': {'pdf', 'docx', 'doc', 'txt'},
    'audio': {'mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac'},
    'video': {'mp4', 'mkv', 'avi', 'mov', 'webm', 'flv'},
    '3d': {'fbx', 'obj', 'gltf', 'glb', 'stl', 'dae'},
    'font': {'ttf', 'otf', 'woff', 'woff2'},
    'data': {'json', 'csv', 'xml', 'yaml', 'yml'},
    'archive': {'zip', 'tar', 'gz', 'rar'},
    'design': {'psd', 'ai', 'eps', 'xcf'}
}

def get_file_category(filename):
    """Determine the category of a file based on its extension"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return category
    return None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return get_file_category(filename) is not None

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/supported-formats', methods=['GET'])
def supported_formats():
    """Return supported file formats and conversions"""
    formats = {
        'image': {
            'formats': ['png', 'jpg', 'jpeg', 'webp', 'svg', 'gif', 'bmp'],
            'conversions': 'All image formats can be converted to any other image format'
        },
        'document': {
            'formats': ['pdf', 'docx', 'txt'],
            'conversions': 'PDF ↔ DOCX, PDF → Images'
        },
        'audio': {
            'formats': ['mp3', 'wav', 'ogg', 'flac'],
            'conversions': 'All audio formats can be converted to any other audio format'
        },
        'video': {
            'formats': ['mp4', 'mkv', 'avi', 'webm', 'gif'],
            'conversions': 'All video formats can be converted to any other video format'
        },
        '3d': {
            'formats': ['obj', 'gltf', 'glb'],
            'conversions': 'OBJ ↔ GLTF ↔ GLB'
        },
        'font': {
            'formats': ['ttf', 'otf', 'woff', 'woff2'],
            'conversions': 'TTF/OTF → WOFF/WOFF2'
        },
        'data': {
            'formats': ['json', 'csv', 'xml'],
            'conversions': 'JSON ↔ CSV ↔ XML'
        },
        'archive': {
            'formats': ['zip', 'tar'],
            'conversions': 'ZIP ↔ TAR'
        },
        'design': {
            'formats': ['psd', 'ai', 'eps'],
            'conversions': 'PSD → PNG/JPG, AI/EPS → SVG/PNG'
        }
    }
    return jsonify(formats)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload (max 100MB)"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400
    
    # Generate unique ID for this conversion
    conversion_id = str(uuid.uuid4())
    
    # Save the uploaded file
    filename = secure_filename(file.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], conversion_id)
    os.makedirs(upload_path, exist_ok=True)
    
    file_path = os.path.join(upload_path, filename)
    file.save(file_path)
    
    # Get file info
    file_size = os.path.getsize(file_path)
    file_category = get_file_category(filename)
    
    return jsonify({
        'conversion_id': conversion_id,
        'filename': filename,
        'size': file_size,
        'category': file_category
    })

@app.route('/api/convert', methods=['POST'])
def convert_file():
    """Handle file conversion"""
    data = request.json
    conversion_id = data.get('conversion_id')
    target_format = data.get('target_format', '').lower()
    
    if not conversion_id or not target_format:
        return jsonify({'error': 'Missing conversion_id or target_format'}), 400
    
    # Find the uploaded file
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], conversion_id)
    if not os.path.exists(upload_path):
        return jsonify({'error': 'Upload not found'}), 404
    
    files = os.listdir(upload_path)
    if not files:
        return jsonify({'error': 'No file found'}), 404
    
    input_file = os.path.join(upload_path, files[0])
    input_filename = files[0]
    
    # Create output directory
    output_path = os.path.join(app.config['CONVERTED_FOLDER'], conversion_id)
    os.makedirs(output_path, exist_ok=True)
    
    # Generate output filename
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}.{target_format}"
    output_file = os.path.join(output_path, output_filename)
    
    try:
        # Determine conversion type and call appropriate converter
        category = get_file_category(input_filename)
        
        if category == 'image':
            success = image_converter.convert(input_file, output_file, target_format)
        elif category == 'document':
            success = document_converter.convert(input_file, output_file, target_format)
        elif category == 'audio':
            success = audio_converter.convert(input_file, output_file, target_format)
        elif category == 'video':
            success = video_converter.convert(input_file, output_file, target_format)
        elif category == '3d':
            success = model_3d_converter.convert(input_file, output_file, target_format)
        elif category == 'font':
            success = font_converter.convert(input_file, output_file, target_format)
        elif category == 'data':
            success = data_converter.convert(input_file, output_file, target_format)
        elif category == 'archive':
            success = archive_converter.convert(input_file, output_file, target_format)
        elif category == 'design':
            success = design_converter.convert(input_file, output_file, target_format)
        else:
            return jsonify({'error': 'Unsupported file category'}), 400
        
        if not success:
            return jsonify({'error': 'Conversion failed'}), 500
        
        # Get output file size
        output_size = os.path.getsize(output_file)
        
        return jsonify({
            'success': True,
            'output_filename': output_filename,
            'output_size': output_size,
            'conversion_id': conversion_id
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Conversion error: {str(e)}'}), 500

@app.route('/api/download/<conversion_id>', methods=['GET'])
def download_file(conversion_id):
    """Download converted file"""
    output_path = os.path.join(app.config['CONVERTED_FOLDER'], conversion_id)
    
    if not os.path.exists(output_path):
        return jsonify({'error': 'File not found'}), 404
    
    files = os.listdir(output_path)
    if not files:
        return jsonify({'error': 'No converted file found'}), 404
    
    file_path = os.path.join(output_path, files[0])
    
    return send_file(file_path, as_attachment=True, download_name=files[0])

@app.route('/api/cleanup/<conversion_id>', methods=['DELETE'])
def cleanup_files(conversion_id):
    """Clean up uploaded and converted files"""
    try:
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], conversion_id)
        output_path = os.path.join(app.config['CONVERTED_FOLDER'], conversion_id)
        
        if os.path.exists(upload_path):
            shutil.rmtree(upload_path)
        
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

if __name__ == '__main__':
    import os
    # Only enable debug mode if explicitly set via environment variable
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
