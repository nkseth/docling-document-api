#!/usr/bin/env python3
"""
Example script demonstrating how to use the Docling Analysis API
"""

import requests
import json
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8000/api/analyze"

def analyze_document(file_path: str, mode: str = "full_analysis", **kwargs):
    """
    Analyze a document using the Docling API
    
    Args:
        file_path: Path to the document file
        mode: Processing mode (default: full_analysis)
        **kwargs: Additional parameters (extract_tables, extract_images, etc.)
    
    Returns:
        dict: Analysis results
    """
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Prepare the request
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'mode': mode}
        data.update(kwargs)
        
        # Make the request
        response = requests.post(API_URL, files=files, data=data)
        response.raise_for_status()
        
        return response.json()

def main():
    """Example usage"""
    
    print("🚀 Docling Document Analysis API Examples\n")
    
    # Example 1: Text extraction
    print("Example 1: Text Extraction")
    print("-" * 50)
    try:
        result = analyze_document(
            file_path="sample.pdf",
            mode="text_extraction"
        )
        print(f"✓ Processed {result['filename']}")
        print(f"✓ Pages: {result['pages_processed']}")
        print(f"✓ Text preview: {result['content']['text'][:200]}...\n")
    except FileNotFoundError:
        print("⚠ sample.pdf not found. Skipping this example.\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    # Example 2: Table extraction
    print("Example 2: Table Extraction")
    print("-" * 50)
    try:
        result = analyze_document(
            file_path="report.pdf",
            mode="table_extraction",
            table_mode="accurate"
        )
        print(f"✓ Processed {result['filename']}")
        print(f"✓ Tables found: {len(result['content'].get('tables', []))}\n")
    except FileNotFoundError:
        print("⚠ report.pdf not found. Skipping this example.\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    # Example 3: Full analysis
    print("Example 3: Full Analysis")
    print("-" * 50)
    try:
        result = analyze_document(
            file_path="document.pdf",
            mode="full_analysis",
            extract_tables=True,
            extract_images=True,
            ocr_enabled=True
        )
        print(f"✓ Processed {result['filename']}")
        print(f"✓ Mode: {result['mode']}")
        print(f"✓ Pages: {result['pages_processed']}")
        print(f"✓ Content keys: {list(result['content'].keys())}\n")
    except FileNotFoundError:
        print("⚠ document.pdf not found. Skipping this example.\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    # Example 4: OCR processing
    print("Example 4: OCR Processing for Images")
    print("-" * 50)
    try:
        result = analyze_document(
            file_path="scanned.jpg",
            mode="ocr_processing",
            ocr_enabled=True
        )
        print(f"✓ Processed {result['filename']}")
        print(f"✓ OCR text extracted\n")
    except FileNotFoundError:
        print("⚠ scanned.jpg not found. Skipping this example.\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    # Example 5: Markdown conversion
    print("Example 5: Markdown Conversion")
    print("-" * 50)
    try:
        result = analyze_document(
            file_path="document.docx",
            mode="markdown_conversion"
        )
        print(f"✓ Processed {result['filename']}")
        print(f"✓ Markdown preview: {result['content']['markdown'][:200]}...\n")
    except FileNotFoundError:
        print("⚠ document.docx not found. Skipping this example.\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    print("✅ Examples completed!")

if __name__ == "__main__":
    main()
