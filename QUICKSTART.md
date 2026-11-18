# Quick Start Guide - Docling Document Analysis API

## 🚀 Getting Started in 3 Steps

### Step 1: Start the Service

```bash
docker compose up -d --build
```

Wait 30-40 seconds for the service to fully initialize.

### Step 2: Verify Service is Running

```bash
curl http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "docling-analysis-server",
  "docling_available": true
}
```

### Step 3: Analyze Your First Document

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@your-document.pdf" \
  -F "mode=full_analysis" \
  | python3 -m json.tool
```

## 📊 Common Use Cases

### Extract Text from PDF
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@document.pdf" \
  -F "mode=text_extraction" \
  -o output.json
```

### Extract Tables from Document
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@report.pdf" \
  -F "mode=table_extraction" \
  -F "table_mode=accurate" \
  -o tables.json
```

### OCR on Scanned Image
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@scanned-page.jpg" \
  -F "mode=ocr_processing" \
  -F "ocr_enabled=true" \
  -o ocr_result.json
```

### Convert to Markdown
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@document.docx" \
  -F "mode=markdown_conversion" \
  -o markdown.json
```

## 🐍 Python Example

```python
import requests

# Analyze a document
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/analyze",
        files={"file": f},
        data={
            "mode": "full_analysis",
            "extract_tables": "true",
            "extract_images": "true",
            "ocr_enabled": "true"
        }
    )
    
result = response.json()
print(f"Processed {result['pages_processed']} pages")
print(f"Text: {result['content']['text'][:100]}...")
```

## 🌐 Web Interface

Access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from your browser!

## 📝 Processing Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `text_extraction` | Extract text only | Quick text retrieval |
| `table_extraction` | Extract tables | Data analysis, reports |
| `image_extraction` | Extract images | Media extraction |
| `markdown_conversion` | Convert to markdown | Documentation, publishing |
| `json_export` | Structured JSON | Data processing |
| `ocr_processing` | OCR for scanned docs | Scanned documents/images |
| `full_analysis` | All features | Complete document analysis |

## 🛠️ Troubleshooting

### Service won't start?
```bash
# Check Docker is running
docker ps

# View logs
docker compose logs -f
```

### Can't connect to localhost:8000?
```bash
# Ensure port mapping is correct
docker port <container_id>

# Should show: 8000/tcp -> 0.0.0.0:8000
```

### File upload fails?
- Check file format is supported (PDF, DOCX, PPTX, PNG, JPG, etc.)
- Ensure file size is reasonable (<50MB recommended)
- Verify file exists and is readable

## 🔄 Stopping the Service

```bash
# Stop the service
docker compose down

# Stop and remove volumes
docker compose down -v
```

## 📚 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore [examples/](examples/) for more code samples
3. Check the interactive docs at http://localhost:8000/docs
4. Customize `docker-compose.yml` for your needs

## 💡 Tips

- Use `table_mode=fast` for quicker processing
- Enable `ocr_enabled=true` for scanned documents
- Check supported formats at `/api/supported-formats`
- Monitor health with `/health` endpoint
- View all modes with `/api/modes`

Enjoy analyzing documents! 🎉
