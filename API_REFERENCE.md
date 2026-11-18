# API Endpoint Reference

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Root
```
GET /
```
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "Docling Document Analysis API",
  "version": "1.0.0",
  "docs": "/docs",
  "endpoints": {
    "analyze": "/api/analyze - POST - Upload and analyze documents"
  }
}
```

---

### 2. Health Check
```
GET /health
```
Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "docling-analysis-server",
  "docling_available": true
}
```

---

### 3. Document Analysis (Main Endpoint)
```
POST /api/analyze
```
Upload and analyze documents with configurable processing modes.

**Content-Type:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file` | File | Yes | - | Document file to analyze |
| `mode` | String | No | `full_analysis` | Processing mode |
| `extract_tables` | Boolean | No | `true` | Extract tables |
| `extract_images` | Boolean | No | `true` | Extract images |
| `ocr_enabled` | Boolean | No | `true` | Enable OCR |
| `table_mode` | String | No | `accurate` | `fast` or `accurate` |
| `export_format` | String | No | `json` | Export format |

**Processing Modes:**
- `text_extraction` - Extract text content only
- `table_extraction` - Extract tables from document
- `image_extraction` - Extract images and metadata
- `markdown_conversion` - Convert to markdown format
- `json_export` - Export structured JSON
- `ocr_processing` - Apply OCR to images/scanned docs
- `full_analysis` - Complete analysis with all features

**Response:**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "mode": "full_analysis",
  "pages_processed": 10,
  "content": {
    "text": "Extracted text...",
    "markdown": "# Markdown content...",
    "tables": [...],
    "images": [...]
  },
  "metadata": {
    "file_type": "PDF",
    "processing_mode": "full_analysis"
  },
  "message": "Document processed successfully"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@document.pdf" \
  -F "mode=full_analysis" \
  -F "extract_tables=true" \
  -F "extract_images=true" \
  -F "ocr_enabled=true" \
  -F "table_mode=accurate"
```

**Example Python:**
```python
import requests

with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/analyze",
        files={"file": f},
        data={
            "mode": "full_analysis",
            "extract_tables": "true",
            "ocr_enabled": "true"
        }
    )
    result = response.json()
```

---

### 4. Get Processing Modes
```
GET /api/modes
```
Returns all available processing modes with descriptions.

**Response:**
```json
{
  "modes": [
    {
      "name": "text_extraction",
      "description": "Extract plain text content from document"
    },
    ...
  ]
}
```

---

### 5. Get Supported Formats
```
GET /api/supported-formats
```
Returns all supported document formats with OCR support information.

**Response:**
```json
{
  "formats": [
    {
      "extension": ".pdf",
      "type": "PDF Document",
      "ocr_support": true
    },
    ...
  ]
}
```

---

## Error Responses

### 400 Bad Request
Invalid file type or missing parameters.

```json
{
  "detail": "Unsupported file type: .txt. Supported: .pdf, .docx, ..."
}
```

### 500 Internal Server Error
Processing error.

```json
{
  "detail": "Error processing document: <error message>"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider adding rate limiting middleware.

---

## File Size Limits

- Default: No explicit limit set
- Recommended: Files under 50MB for optimal performance
- Large files may require increased timeout settings

---

## Supported File Types

| Extension | Type | OCR Support |
|-----------|------|-------------|
| `.pdf` | PDF Document | ✅ |
| `.docx` | Microsoft Word | ❌ |
| `.pptx` | Microsoft PowerPoint | ❌ |
| `.png` | PNG Image | ✅ |
| `.jpg`, `.jpeg` | JPEG Image | ✅ |
| `.tiff` | TIFF Image | ✅ |
| `.html` | HTML Document | ❌ |
| `.md` | Markdown | ❌ |

---

## Response Times

Typical response times (approximate):
- Text extraction: 2-5 seconds
- Table extraction: 5-10 seconds
- Full analysis: 10-30 seconds
- OCR processing: 5-15 seconds per page

*Note: Times vary based on document size and complexity*
