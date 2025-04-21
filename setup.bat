@echo off
echo 🔧 Creating virtual environment...
python -m venv venv

echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

echo 📦 Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo 🌐 Downloading spaCy model...
python -m spacy download en_core_web_sm

echo ✅ Setup complete! To activate later, run: venv\Scripts\activate
pause
