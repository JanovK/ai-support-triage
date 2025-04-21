#!/bin/bash

echo "🔧 Creating virtual environment..."
python3 -m venv venv

echo "✅ Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🌐 Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo "✅ Setup complete! To activate the venv later, run: source venv/bin/activate"
