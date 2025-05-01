# ---- Base image with Python 3.10
FROM python:3.10-slim

# ---- Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ---- Create working directory
WORKDIR /app

# ---- Copy files
COPY . /app

# ---- Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python -m spacy download en_core_web_sm

# ---- Default command (you can override this)
CMD ["streamlit", "run", "src/dashboard.py"]
