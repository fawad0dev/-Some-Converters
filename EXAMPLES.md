# Examples - Universal File Converter

This document provides examples of using the Universal File Converter.

## Example Files

### 1. Image Conversion (PNG to JPG)

**Create test image:**
```bash
# Using Python
python3 << EOF
from PIL import Image, ImageDraw

img = Image.new('RGB', (400, 300), color='lightblue')
draw = ImageDraw.Draw(img)
draw.rectangle([50, 50, 350, 250], fill='orange', outline='blue', width=5)
draw.text((200, 150), "Hello World", fill='white')
img.save('sample_image.png')
print("Created: sample_image.png")
EOF
```

**Convert via API:**
```bash
# Upload
curl -X POST -F "file=@sample_image.png" http://localhost:5000/api/upload

# Convert (use the conversion_id from above)
curl -X POST -H "Content-Type: application/json" \
  -d '{"conversion_id":"YOUR_ID","target_format":"jpg"}' \
  http://localhost:5000/api/convert

# Download
curl -O http://localhost:5000/api/download/YOUR_ID
```

### 2. Data Conversion (JSON to CSV)

**Create test JSON:**
```bash
cat > sample_data.json << 'EOF'
[
  {"name": "Alice", "age": 30, "city": "New York"},
  {"name": "Bob", "age": 25, "city": "San Francisco"},
  {"name": "Charlie", "age": 35, "city": "Chicago"}
]
EOF
```

**Convert via API:**
```bash
# Upload
RESPONSE=$(curl -s -X POST -F "file=@sample_data.json" http://localhost:5000/api/upload)
ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['conversion_id'])")

# Convert to CSV
curl -X POST -H "Content-Type: application/json" \
  -d "{\"conversion_id\":\"$ID\",\"target_format\":\"csv\"}" \
  http://localhost:5000/api/convert

# Download
curl -O http://localhost:5000/api/download/$ID
```

### 3. Archive Conversion (ZIP to TAR)

**Create test archive:**
```bash
# Create sample files
mkdir sample_archive
echo "File 1 content" > sample_archive/file1.txt
echo "File 2 content" > sample_archive/file2.txt
echo "File 3 content" > sample_archive/file3.txt

# Create ZIP
zip -r sample_archive.zip sample_archive/
```

**Convert via API:**
```bash
# Upload
RESPONSE=$(curl -s -X POST -F "file=@sample_archive.zip" http://localhost:5000/api/upload)
ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['conversion_id'])")

# Convert to TAR
curl -X POST -H "Content-Type: application/json" \
  -d "{\"conversion_id\":\"$ID\",\"target_format\":\"tar\"}" \
  http://localhost:5000/api/convert

# Download
curl -O http://localhost:5000/api/download/$ID
```

### 4. Data Format Chain (CSV → JSON → XML)

**Create test CSV:**
```bash
cat > sample.csv << 'EOF'
product,price,quantity,category
Apple,1.50,100,Fruit
Banana,0.75,150,Fruit
Carrot,0.50,80,Vegetable
Tomato,2.00,60,Vegetable
EOF
```

**Convert CSV to JSON:**
```bash
RESPONSE=$(curl -s -X POST -F "file=@sample.csv" http://localhost:5000/api/upload)
ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['conversion_id'])")

curl -X POST -H "Content-Type: application/json" \
  -d "{\"conversion_id\":\"$ID\",\"target_format\":\"json\"}" \
  http://localhost:5000/api/convert

curl http://localhost:5000/api/download/$ID -o sample.json
```

**Convert JSON to XML:**
```bash
RESPONSE=$(curl -s -X POST -F "file=@sample.json" http://localhost:5000/api/upload)
ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['conversion_id'])")

curl -X POST -H "Content-Type: application/json" \
  -d "{\"conversion_id\":\"$ID\",\"target_format\":\"xml\"}" \
  http://localhost:5000/api/convert

curl http://localhost:5000/api/download/$ID -o sample.xml
```

## Web Interface Examples

### Upload and Convert via Web UI

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open browser:**
   Navigate to `http://localhost:5000`

3. **Upload a file:**
   - Drag and drop a file onto the upload area
   - Or click "Choose File" to browse

4. **Select format:**
   - Choose target format from available options
   - Formats are filtered based on input file type

5. **Convert:**
   - Click "Convert File" button
   - Wait for conversion to complete

6. **Download:**
   - Click "Download File" button
   - File will be automatically downloaded

## Python Script Example

```python
#!/usr/bin/env python3
"""
Example script to convert files using the API
"""
import requests
import sys

def convert_file(input_file, target_format):
    """Convert a file using the API"""
    base_url = "http://localhost:5000/api"
    
    # Upload file
    print(f"Uploading {input_file}...")
    with open(input_file, 'rb') as f:
        response = requests.post(
            f"{base_url}/upload",
            files={'file': f}
        )
    
    if response.status_code != 200:
        print(f"Upload failed: {response.json()}")
        return False
    
    data = response.json()
    conversion_id = data['conversion_id']
    print(f"File uploaded: {data['filename']} ({data['size']} bytes)")
    
    # Convert file
    print(f"Converting to {target_format}...")
    response = requests.post(
        f"{base_url}/convert",
        json={
            'conversion_id': conversion_id,
            'target_format': target_format
        }
    )
    
    if response.status_code != 200:
        print(f"Conversion failed: {response.json()}")
        return False
    
    data = response.json()
    print(f"Conversion complete: {data['output_filename']}")
    
    # Download file
    output_file = data['output_filename']
    print(f"Downloading {output_file}...")
    response = requests.get(f"{base_url}/download/{conversion_id}")
    
    with open(output_file, 'wb') as f:
        f.write(response.content)
    
    print(f"Saved to: {output_file}")
    
    # Cleanup
    requests.delete(f"{base_url}/cleanup/{conversion_id}")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input_file> <target_format>")
        print("Example: python convert.py image.png jpg")
        sys.exit(1)
    
    input_file = sys.argv[1]
    target_format = sys.argv[2]
    
    if convert_file(input_file, target_format):
        print("✅ Conversion successful!")
    else:
        print("❌ Conversion failed!")
        sys.exit(1)
```

**Usage:**
```bash
# Save the script as convert.py
python convert.py input.png jpg
python convert.py data.json csv
python convert.py archive.zip tar
```

## Batch Conversion Example

```python
#!/usr/bin/env python3
"""
Batch convert multiple files
"""
import requests
import os
import glob

def batch_convert(pattern, target_format):
    """Convert multiple files matching pattern"""
    base_url = "http://localhost:5000/api"
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} files to convert")
    
    for input_file in files:
        print(f"\nProcessing: {input_file}")
        
        # Upload
        with open(input_file, 'rb') as f:
            response = requests.post(
                f"{base_url}/upload",
                files={'file': f}
            )
        
        if response.status_code != 200:
            print(f"  ❌ Upload failed")
            continue
        
        conversion_id = response.json()['conversion_id']
        
        # Convert
        response = requests.post(
            f"{base_url}/convert",
            json={
                'conversion_id': conversion_id,
                'target_format': target_format
            }
        )
        
        if response.status_code != 200:
            print(f"  ❌ Conversion failed")
            continue
        
        output_filename = response.json()['output_filename']
        
        # Download
        response = requests.get(f"{base_url}/download/{conversion_id}")
        output_path = os.path.join('converted', output_filename)
        
        os.makedirs('converted', exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"  ✅ Saved to: {output_path}")
        
        # Cleanup
        requests.delete(f"{base_url}/cleanup/{conversion_id}")

if __name__ == '__main__':
    # Example: Convert all PNG files to JPG
    batch_convert("*.png", "jpg")
    
    # Example: Convert all JSON files to CSV
    # batch_convert("*.json", "csv")
```

## Integration Examples

### JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function convertFile(inputFile, targetFormat) {
    const baseUrl = 'http://localhost:5000/api';
    
    // Upload
    const formData = new FormData();
    formData.append('file', fs.createReadStream(inputFile));
    
    const uploadResponse = await axios.post(`${baseUrl}/upload`, formData, {
        headers: formData.getHeaders()
    });
    
    const conversionId = uploadResponse.data.conversion_id;
    
    // Convert
    const convertResponse = await axios.post(`${baseUrl}/convert`, {
        conversion_id: conversionId,
        target_format: targetFormat
    });
    
    const outputFilename = convertResponse.data.output_filename;
    
    // Download
    const downloadResponse = await axios.get(
        `${baseUrl}/download/${conversionId}`,
        { responseType: 'stream' }
    );
    
    downloadResponse.data.pipe(fs.createWriteStream(outputFilename));
    
    console.log(`Converted: ${outputFilename}`);
}

convertFile('input.png', 'jpg');
```

## Additional Resources

- API Documentation: See DEVELOPER.md
- Supported Formats: Visit http://localhost:5000/api/supported-formats
- Troubleshooting: See README.md
