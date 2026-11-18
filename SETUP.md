# 🚀 SETUP INSTRUCTIONS

## Prerequisites Check

Before starting, ensure you have:
- ✅ Docker Desktop installed and running
- ✅ Docker in your system PATH

### Fix Docker PATH Issue

If you get "command not found: docker", add Docker to your PATH:

```bash
# Open your .zshrc file
nano ~/.zshrc

# Add this line at the end
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"

# Save and reload
source ~/.zshrc

# Verify Docker works
docker --version
```

## Quick Start (Once Docker is Set Up)

### 1. Build and Start the Service

```bash
cd docling-document-api
docker compose up -d --build
```

This will:
- Build the Docker image with all dependencies
- Install Docling and required libraries
- Start the FastAPI server on port 8000
- Run health checks

**Wait 30-40 seconds** for the service to fully initialize (Docling has large dependencies).

### 2. Verify Service is Running

```bash
# Check health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"docling-analysis-server","docling_available":true}
```

### 3. Test the API

```bash
# Get processing modes
curl http://localhost:8000/api/modes

# Get supported formats
curl http://localhost:8000/api/supported-formats

# Test with a document (replace with your file)
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@your-document.pdf" \
  -F "mode=text_extraction" \
  | python3 -m json.tool
```

### 4. Access Interactive Documentation

Open in your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Alternative: Local Development (Without Docker)

If you prefer running locally without Docker:

```bash
# Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to project
cd docling-document-api

# Install dependencies
uv sync

# Run the server
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Viewing Logs

```bash
# View live logs
docker compose logs -f

# View last 100 lines
docker compose logs --tail=100
```

## Stopping the Service

```bash
# Stop but keep containers
docker compose stop

# Stop and remove containers
docker compose down

# Stop and remove everything including volumes
docker compose down -v
```

## Common Issues & Solutions

### Issue: Docker command not found
**Solution**: Add Docker to PATH (see above) or restart Terminal after installing Docker Desktop

### Issue: Port 8000 already in use
**Solution**: Change port in docker-compose.yml:
```yaml
ports:
  - "8080:8000"  # Use port 8080 instead
```

### Issue: Container starts then stops
**Solution**: Check logs:
```bash
docker compose logs
```

### Issue: Can't connect to localhost:8000
**Solution**:
1. Wait 30-40 seconds for service to initialize
2. Check container is running: `docker compose ps`
3. Verify port mapping: `docker port <container-name>`
4. Try 127.0.0.1:8000 instead of localhost:8000

## Testing Your Setup

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```
✅ Should return `{"status":"healthy",...}`

### Test 2: Get Modes
```bash
curl http://localhost:8000/api/modes | python3 -m json.tool
```
✅ Should return list of processing modes

### Test 3: Upload a Document
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@/path/to/your/document.pdf" \
  -F "mode=text_extraction"
```
✅ Should return JSON with extracted text

### Test 4: Access Web Interface
```
Open: http://localhost:8000/docs
```
✅ Should show Swagger UI with API documentation

## What's Next?

1. ✅ **Read the docs**: Check README.md and QUICKSTART.md
2. ✅ **Try examples**: Run scripts in examples/ folder
3. ✅ **Test with your files**: Upload PDFs, Word docs, images
4. ✅ **Explore modes**: Try different processing modes
5. ✅ **Integrate**: Use the API in your applications

## Files Created

- `main.py` - FastAPI application
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose setup
- `pyproject.toml` - UV dependencies
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick start guide
- `API_REFERENCE.md` - API documentation
- `IMPLEMENTATION_SUMMARY.md` - What was built
- `examples/test_api.py` - Python examples
- `examples/test_api.sh` - Bash examples

## Success!

Your Document Analysis API is ready to use! 🎉

**Key Features**:
- Single endpoint for all document processing
- 7 processing modes
- Support for PDF, DOCX, PPTX, Images
- OCR for scanned documents
- Table extraction
- Markdown conversion
- And more!

**Need Help?**
- Check logs: `docker compose logs -f`
- Read docs: README.md
- Try examples: examples/test_api.sh
- Use interactive docs: http://localhost:8000/docs
