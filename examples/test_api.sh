#!/bin/bash

# Docling Document Analysis API - Test Script
# This script demonstrates various API calls using curl

API_URL="http://localhost:8000"

echo "🚀 Testing Docling Document Analysis API"
echo "========================================="
echo ""

# Check if server is running
echo "1️⃣  Checking server health..."
curl -s "${API_URL}/health" | python3 -m json.tool
echo ""

# Get supported formats
echo "2️⃣  Getting supported formats..."
curl -s "${API_URL}/api/supported-formats" | python3 -m json.tool
echo ""

# Get processing modes
echo "3️⃣  Getting processing modes..."
curl -s "${API_URL}/api/modes" | python3 -m json.tool
echo ""

# Test document analysis (requires a sample PDF file)
if [ -f "sample.pdf" ]; then
    echo "4️⃣  Testing document analysis with sample.pdf..."
    
    # Text extraction
    echo "   📄 Text Extraction..."
    curl -X POST "${API_URL}/api/analyze" \
      -F "file=@sample.pdf" \
      -F "mode=text_extraction" \
      -o text_result.json
    echo "   ✓ Saved to text_result.json"
    
    # Full analysis
    echo "   📊 Full Analysis..."
    curl -X POST "${API_URL}/api/analyze" \
      -F "file=@sample.pdf" \
      -F "mode=full_analysis" \
      -F "extract_tables=true" \
      -F "extract_images=true" \
      -F "ocr_enabled=true" \
      -o full_result.json
    echo "   ✓ Saved to full_result.json"
    
    # Markdown conversion
    echo "   📝 Markdown Conversion..."
    curl -X POST "${API_URL}/api/analyze" \
      -F "file=@sample.pdf" \
      -F "mode=markdown_conversion" \
      -o markdown_result.json
    echo "   ✓ Saved to markdown_result.json"
    
else
    echo "⚠️  No sample.pdf found. Skipping document analysis tests."
    echo "   Create a sample.pdf file to test document processing."
fi

echo ""
echo "✅ API tests completed!"
echo ""
echo "📖 View interactive docs at: ${API_URL}/docs"
