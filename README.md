# Docling Document Analysis API

A powerful, unified REST API for document analysis, text extraction, table parsing, and image processing using the Docling library. Built with FastAPI and optimized for performance with UV package manager.

## 🚀 Features

- **Single Unified API Endpoint** - One endpoint (`/api/analyze`) handles all document processing tasks
- **Multi-Format Support** - PDF, DOCX, PPTX, Images (PNG, JPG, TIFF), HTML, Markdown
- **Intelligent Processing Modes**:
  - Text Extraction
  - Table Extraction & Parsing
  - Image Extraction
  - Markdown Conversion
  - JSON Export
  - OCR Processing for scanned documents
  - Full Analysis (all features combined)
- **Advanced Features**:
  - OCR support for scanned documents and images
  - Accurate table structure recognition
  - Document metadata extraction
  - Automatic format detection
- **Production Ready**:
  - Docker & Docker Compose support
  - Health check endpoints
  - Comprehensive error handling
  - Request validation

## 📋 Requirements

- Python 3.9+
- Docker & Docker Compose (for containerized deployment)
- UV package manager (for local development)

## 🛠️ Installation & Setup

### Option 1: Docker Compose (Recommended)

1. **Clone the repository:**
```bash
git clone <repository-url>
cd dockling
```

2. **Build and start the service:**
```bash
docker compose up -d --build
```

3. **Check service health:**
```bash
curl http://localhost:8000/health
```

The API will be available at `http://localhost:8000`

### Option 2: Local Development with UV

1. **Install UV if not already installed:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Install dependencies:**
```bash
uv sync
```

3. **Run the server:**
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📖 API Documentation

### Interactive API Docs
Once running, access the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### 1. Document Analysis (Main Endpoint)
```
POST /api/analyze
```

**Upload a document and analyze it based on the specified mode.**

**Parameters:**
- `file` (required): Document file (PDF, DOCX, PPTX, PNG, JPG, etc.)
- `mode` (optional): Processing mode (default: `full_analysis`)
  - `text_extraction`
  - `table_extraction`
  - `image_extraction`
  - `markdown_conversion`
  - `json_export`
  - `ocr_processing`
  - `full_analysis`
- `extract_tables` (optional): Extract tables (default: `true`)
- `extract_images` (optional): Extract images (default: `true`)
- `ocr_enabled` (optional): Enable OCR (default: `true`)
- `table_mode` (optional): `fast` or `accurate` (default: `accurate`)
- `export_format` (optional): `json`, `markdown`, `text` (default: `json`)

**Example using cURL:**
```bash
# Text extraction from PDF
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@document.pdf" \
  -F "mode=text_extraction"

# Full analysis with all features
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@document.pdf" \
  -F "mode=full_analysis" \
  -F "extract_tables=true" \
  -F "extract_images=true" \
  -F "ocr_enabled=true"

# Table extraction only
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@spreadsheet.pdf" \
  -F "mode=table_extraction" \
  -F "table_mode=accurate"

# OCR processing for scanned documents
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@scanned.jpg" \
  -F "mode=ocr_processing"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/api/analyze"

with open("document.pdf", "rb") as f:
    files = {"file": f}
    data = {
        "mode": "full_analysis",
        "extract_tables": "true",
        "extract_images": "true",
        "ocr_enabled": "true",
        "table_mode": "accurate"
    }
    response = requests.post(url, files=files, data=data)
    result = response.json()
    print(result)
```

**Response Structure:**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "mode": "full_analysis",
  "pages_processed": 10,
  "content": {
    "text": "Extracted text content...",
    "markdown": "# Markdown formatted content...",
    "tables": [
      {
        "page": 1,
        "data": {...}
      }
    ],
    "images": [
      {
        "page": 2,
        "image_id": 0
      }
    ]
  },
  "metadata": {
    "file_type": "PDF",
    "processing_mode": "full_analysis"
  },
  "message": "Document processed successfully using full_analysis mode"
}
```

#### 2. Get Processing Modes
```
GET /api/modes
```

Returns all available processing modes with descriptions.

**Example:**
```bash
curl http://localhost:8000/api/modes
```

#### 3. Get Supported Formats
```
GET /api/supported-formats
```

Returns all supported document formats with OCR support information.

**Example:**
```bash
curl http://localhost:8000/api/supported-formats
```

#### 4. Health Check
```
GET /health
```

Check service health status.

**Example:**
```bash
curl http://localhost:8000/health
```

## 🎯 Processing Modes Explained

### 1. Text Extraction
Extracts plain text content from documents.
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@document.pdf" \
  -F "mode=text_extraction"
```

### 2. Table Extraction
Extracts and parses tables from documents with structure preservation.
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@report.pdf" \
  -F "mode=table_extraction" \
  -F "table_mode=accurate"
```

### 3. Image Extraction
Extracts images from documents with metadata.
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@presentation.pptx" \
  -F "mode=image_extraction"
```

### 4. Markdown Conversion
Converts documents to markdown format.
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@document.docx" \
  -F "mode=markdown_conversion"
```

### 5. JSON Export
Exports document as structured JSON.
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@document.pdf" \
  -F "mode=json_export"
```

### 6. OCR Processing
Applies OCR to scanned documents or images.
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@scanned_page.jpg" \
  -F "mode=ocr_processing" \
  -F "ocr_enabled=true"
```

### 7. Full Analysis
Complete analysis with all features enabled.
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@document.pdf" \
  -F "mode=full_analysis"
```

## 📦 Supported File Formats

| Format | Extension | OCR Support | Description |
|--------|-----------|-------------|-------------|
| PDF | .pdf | ✅ | PDF documents |
| Word | .docx | ❌ | Microsoft Word documents |
| PowerPoint | .pptx | ❌ | Microsoft PowerPoint presentations |
| PNG | .png | ✅ | PNG images |
| JPEG | .jpg, .jpeg | ✅ | JPEG images |
| TIFF | .tiff | ✅ | TIFF images |
| HTML | .html | ❌ | HTML documents |
| Markdown | .md | ❌ | Markdown files |

## 🐳 Docker Commands

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f

# Stop service
docker compose down

# Restart service
docker compose restart

# Check status
docker compose ps

# Rebuild after code changes
docker compose up -d --build
```

## 🔧 Configuration

### Environment Variables
You can customize the service using environment variables in `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - MAX_UPLOAD_SIZE=50MB  # Optional: Set max file upload size
  - LOG_LEVEL=INFO        # Optional: Set logging level
```

### Development Mode
For development with hot reload, uncomment the volumes section in `docker-compose.yml`:

```yaml
volumes:
  - ./main.py:/app/main.py
```

## 📊 Performance Considerations

- **Table Extraction**: Use `table_mode=fast` for quicker processing with slightly lower accuracy
- **Large Files**: The API processes files in memory; consider file size limits for production
- **OCR**: OCR processing is CPU-intensive and may take longer for high-resolution images
- **Concurrent Requests**: Docker Compose configuration can be scaled with replicas

## 🛡️ Error Handling

The API provides detailed error messages:

- **400 Bad Request**: Invalid file type or missing parameters
- **500 Internal Server Error**: Processing errors with details

Example error response:
```json
{
  "detail": "Unsupported file type: .txt. Supported: .pdf, .docx, .pptx, ..."
}
```

## 🧪 Testing

Test the API with sample documents:

```bash
# Test with a PDF
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@sample.pdf" \
  -F "mode=text_extraction" \
  -o result.json

# Verify response
cat result.json | python -m json.tool
```

## 📝 License

This project uses the Docling library. Please check Docling's license for commercial use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📧 Support

For issues and questions, please open an issue in the repository.