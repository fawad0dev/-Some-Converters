#!/bin/bash
# Universal File Converter - Start Script

echo "🔄 Starting Universal File Converter..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p uploads converted

# Start the application
echo ""
echo "🚀 Starting Flask application..."
echo "🌐 Open your browser and navigate to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
