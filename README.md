# 🔄 Universal File Converter

A comprehensive web-based file converter supporting multiple file formats including documents, images, audio, video, 3D models, fonts, data files, and archives.

## 🌟 Features

- **Multiple File Format Support**
  - 🖼️ **Images**: PNG, JPG, WEBP, SVG, GIF, BMP
  - 📄 **Documents**: PDF ↔ DOCX, PDF → Images, TXT
  - 🎵 **Audio**: MP3, WAV, OGG, FLAC
  - 🎬 **Video**: MP4, MKV, AVI, WEBM, GIF
  - 🎮 **3D Models**: OBJ, GLTF, GLB
  - 🔤 **Fonts**: TTF, OTF, WOFF, WOFF2
  - 📊 **Data**: JSON ↔ CSV ↔ XML
  - 🗜️ **Archives**: ZIP ↔ TAR
  - 🎨 **Design**: PSD → PNG/JPG, AI/EPS → SVG

- **User-Friendly Interface**
  - Drag-and-drop file upload
  - Real-time conversion progress
  - One-click download
  - Automatic file cleanup

- **Secure & Private**
  - Files are processed on the server
  - Automatic deletion after download
  - No file storage retention

## 🛠️ Technologies

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Pillow** - Image processing
- **pypdf & python-docx** - Document conversion
- **psd-tools** - PSD file support
- **reportlab** - PDF generation
- **fonttools** - Font conversion

### Frontend
- **HTML5, CSS3, JavaScript**
- Modern responsive design
- No external JS frameworks required

### External Tools (Optional)
- **FFmpeg** - Audio/Video conversion (install separately)
- **Blender CLI** - Advanced 3D model conversion (install separately)

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- 2GB RAM minimum
- 1GB free disk space

### Python Dependencies
All Python dependencies are listed in `requirements.txt`:
```
Flask==3.0.0
Werkzeug==3.0.1
Pillow==10.1.0
psd-tools==1.9.31
pypdf==3.17.4
python-docx==1.1.0
pdf2image==1.16.3
svglib==1.5.1
reportlab==4.0.7
fonttools==4.46.0
lxml==4.9.4
cairosvg==2.7.1
```

### Optional Dependencies
- **FFmpeg** (for audio/video conversion)
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/)

- **Poppler** (for PDF to image conversion)
  - Ubuntu/Debian: `sudo apt-get install poppler-utils`
  - macOS: `brew install poppler`

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/fawad0dev/-Some-Converters.git
cd -Some-Converters
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Optional Tools (Recommended)
For full functionality, install FFmpeg:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg poppler-utils
```

**macOS:**
```bash
brew install ffmpeg poppler
```

**Windows:**
- Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add FFmpeg to your system PATH

## 🏃 Running the Application

### Development Mode
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### Production Mode
For production deployment, use a WSGI server like Gunicorn:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📖 Usage

1. **Open the Application**
   - Navigate to `http://localhost:5000` in your web browser

2. **Upload a File**
   - Drag and drop a file onto the upload area, or
   - Click "Choose File" to browse your files

3. **Select Target Format**
   - Choose the desired output format from the available options
   - Formats are automatically filtered based on the input file type

4. **Convert**
   - Click the "Convert File" button
   - Wait for the conversion to complete

5. **Download**
   - Click "Download File" to get your converted file
   - Files are automatically cleaned up after download

## 🔧 API Endpoints

### `GET /`
Returns the main web interface

### `GET /api/supported-formats`
Returns list of supported file formats and conversions

### `POST /api/upload`
Upload a file for conversion
- **Body**: multipart/form-data with 'file' field
- **Returns**: `{conversion_id, filename, size, category}`

### `POST /api/convert`
Convert the uploaded file
- **Body**: `{conversion_id, target_format}`
- **Returns**: `{success, output_filename, output_size, conversion_id}`

### `GET /api/download/<conversion_id>`
Download the converted file

### `DELETE /api/cleanup/<conversion_id>`
Manually cleanup uploaded and converted files

### `GET /api/health`
Health check endpoint

## 📁 Project Structure

```
-Some-Converters/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── converters/                 # Converter modules
│   ├── __init__.py
│   ├── image_converter.py      # Image conversions
│   ├── document_converter.py   # Document conversions
│   ├── audio_converter.py      # Audio conversions
│   ├── video_converter.py      # Video conversions
│   ├── data_converter.py       # Data format conversions
│   ├── archive_converter.py    # Archive conversions
│   ├── font_converter.py       # Font conversions
│   ├── design_converter.py     # Design file conversions
│   └── model_3d_converter.py   # 3D model conversions
├── templates/
│   └── index.html              # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css           # Stylesheet
│   └── js/
│       └── app.js              # Frontend JavaScript
├── uploads/                    # Temporary upload directory
└── converted/                  # Temporary conversion directory
```

## 🔒 Security Considerations

- Maximum file size: 100MB (configurable in `app.py`)
- Files are stored temporarily and deleted after download
- Input validation for file types
- Secure filename handling
- No permanent file storage

## 🐛 Troubleshooting

### FFmpeg not found
If audio/video conversion fails:
- Verify FFmpeg is installed: `ffmpeg -version`
- Ensure FFmpeg is in your system PATH

### PDF to Image conversion fails
- Install poppler-utils: `sudo apt-get install poppler-utils`
- Or use pdf2image with custom poppler path

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Port already in use
- Change the port in `app.py`: `app.run(port=5001)`
- Or kill the process using port 5000

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

This project uses the following open-source tools:
- [Pillow](https://python-pillow.org/) - Image processing
- [FFmpeg](https://ffmpeg.org/) - Audio/Video processing
- [psd-tools](https://github.com/psd-tools/psd-tools) - PSD file support
- [python-docx](https://python-docx.readthedocs.io/) - DOCX support
- [pypdf](https://pypdf.readthedocs.io/) - PDF support
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [fonttools](https://github.com/fonttools/fonttools) - Font manipulation

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ by the open-source community
