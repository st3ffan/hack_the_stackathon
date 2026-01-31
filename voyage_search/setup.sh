#!/bin/bash

echo "================================"
echo "Visual Search Setup Script"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and fill in your credentials"
echo "2. Place your image files (*.jpg) in this directory"
echo "3. Run: python gen_image_embeddings_v2.py (to generate embeddings)"
echo "4. Create the vector search index in MongoDB Atlas (see README.md)"
echo "5. Run: python app.py (to start the web server)"
echo ""
echo "To activate the virtual environment later, run:"
echo "  source venv/bin/activate"
echo ""
