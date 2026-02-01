# Developer Guide - Universal File Converter

## Architecture Overview

### Backend Structure
```
app.py                    # Main Flask application with API endpoints
converters/              # Conversion modules
  ├── __init__.py
  ├── image_converter.py      # Pillow-based image conversion
  ├── document_converter.py   # PDF/DOCX handling
  ├── audio_converter.py      # FFmpeg audio conversion
  ├── video_converter.py      # FFmpeg video conversion
  ├── data_converter.py       # JSON/CSV/XML conversion
  ├── archive_converter.py    # ZIP/TAR handling
  ├── font_converter.py       # fonttools-based font conversion
  ├── design_converter.py     # PSD/AI/EPS conversion
  └── model_3d_converter.py   # 3D model conversion
```

### Frontend Structure
```
templates/
  └── index.html          # Main SPA template
static/
  ├── css/
  │   └── style.css       # Styles and responsive design
  └── js/
      └── app.js          # Frontend logic and API calls
```

## API Endpoints

### `GET /`
Returns the main web interface

### `GET /api/supported-formats`
Returns JSON with all supported formats and conversion capabilities

### `POST /api/upload`
Upload a file for conversion
- **Content-Type**: multipart/form-data
- **Body**: file (binary)
- **Response**: 
```json
{
  "conversion_id": "uuid",
  "filename": "file.ext",
  "size": 1024,
  "category": "image"
}
```

### `POST /api/convert`
Convert uploaded file
- **Content-Type**: application/json
- **Body**:
```json
{
  "conversion_id": "uuid",
  "target_format": "png"
}
```
- **Response**:
```json
{
  "success": true,
  "output_filename": "file.png",
  "output_size": 2048,
  "conversion_id": "uuid"
}
```

### `GET /api/download/<conversion_id>`
Download converted file
- **Response**: File download

### `DELETE /api/cleanup/<conversion_id>`
Clean up uploaded and converted files
- **Response**: 
```json
{
  "success": true
}
```

## Adding New Converters

### Step 1: Create Converter Module
Create a new file in `converters/` directory:

```python
# converters/new_converter.py

def convert(input_file, output_file, target_format):
    """
    Convert files from one format to another
    
    Args:
        input_file (str): Path to input file
        output_file (str): Path to output file
        target_format (str): Target format extension
    
    Returns:
        bool: True if conversion succeeded, False otherwise
    """
    try:
        # Your conversion logic here
        return True
    except Exception as e:
        print(f"Conversion error: {e}")
        return False
```

### Step 2: Register in app.py
Add your converter to the imports and routing:

```python
from converters import new_converter

# In convert_file() function:
elif category == 'newtype':
    success = new_converter.convert(input_file, output_file, target_format)
```

### Step 3: Add to ALLOWED_EXTENSIONS
Update the ALLOWED_EXTENSIONS dict in app.py:

```python
ALLOWED_EXTENSIONS = {
    'newtype': {'ext1', 'ext2', 'ext3'},
    # ... other types
}
```

### Step 4: Update supported-formats endpoint
Add information about your new format in the `supported_formats()` function.

## Frontend Customization

### Adding New Format Categories
Update `formatMappings` in `static/js/app.js`:

```javascript
const formatMappings = {
    'newtype': ['ext1', 'ext2', 'ext3'],
    // ... other types
};
```

### Styling
All styles are in `static/css/style.css`. Key CSS variables:

```css
:root {
    --primary-color: #4F46E5;
    --primary-hover: #4338CA;
    --secondary-color: #6B7280;
    --success-color: #10B981;
    --error-color: #EF4444;
}
```

## Testing

### Manual API Testing
```bash
# Upload a file
curl -X POST -F "file=@test.png" http://localhost:5000/api/upload

# Convert file (use the conversion_id from upload response)
curl -X POST -H "Content-Type: application/json" \
  -d '{"conversion_id":"YOUR_ID","target_format":"jpg"}' \
  http://localhost:5000/api/convert

# Download file
curl -O http://localhost:5000/api/download/YOUR_ID
```

### Adding Unit Tests
Create `tests/` directory with test files:

```python
# tests/test_converters.py
import unittest
from converters import image_converter

class TestImageConverter(unittest.TestCase):
    def test_png_to_jpg(self):
        result = image_converter.convert(
            'tests/fixtures/test.png',
            'tests/output/test.jpg',
            'jpg'
        )
        self.assertTrue(result)
```

## Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install FFmpeg if needed
RUN apt-get update && apt-get install -y ffmpeg

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t file-converter .
docker run -p 5000:5000 file-converter
```

### Environment Variables
- `FLASK_DEBUG`: Set to "true" to enable debug mode (default: false)
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)

## Performance Optimization

### File Size Limits
Adjust in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### Cleanup Schedule
Automatic cleanup happens after download. To add scheduled cleanup:

```python
from apscheduler.schedulers.background import BackgroundScheduler

def cleanup_old_files():
    # Clean files older than 1 hour
    pass

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_files, 'interval', hours=1)
scheduler.start()
```

## Troubleshooting

### Common Issues

**FFmpeg not found**
- Install: `sudo apt-get install ffmpeg` (Ubuntu/Debian)
- Or download from: https://ffmpeg.org/

**Import errors**
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

**Port already in use**
- Change port in app.py or kill existing process
- Find process: `lsof -i :5000`

**Out of memory**
- Reduce `MAX_CONTENT_LENGTH`
- Use streaming for large files
- Add file compression

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## License
MIT License - See LICENSE file for details
