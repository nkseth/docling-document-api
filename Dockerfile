FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Docling (including OCR and image processing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libgomp1 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgeos-dev \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv
RUN pip install --no-cache-dir uv

# Sync dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY main.py ./

# Create uploads directory for temporary files
RUN mkdir -p /app/uploads

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application using uvicorn directly
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
