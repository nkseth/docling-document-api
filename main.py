from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
import tempfile
import os
import shutil
from pathlib import Path
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import Docling components
try:
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
except ImportError as e:
    logger.error(f"Error importing Docling: {e}")
    logger.info("Please install docling: pip install docling")

# Create FastAPI instance
app = FastAPI(
    title="Docling Document Analysis API",
    description="A unified API for document analysis, extraction, and processing using Docling",
    version="1.0.0"
)

# Processing modes
class ProcessingMode(str, Enum):
    TEXT_EXTRACTION = "text_extraction"
    TABLE_EXTRACTION = "table_extraction"
    IMAGE_EXTRACTION = "image_extraction"
    FULL_ANALYSIS = "full_analysis"
    MARKDOWN_CONVERSION = "markdown_conversion"
    JSON_EXPORT = "json_export"
    OCR_PROCESSING = "ocr_processing"

# Request models
class DocumentProcessingRequest(BaseModel):
    mode: ProcessingMode = Field(
        default=ProcessingMode.FULL_ANALYSIS,
        description="Processing mode to apply to the document"
    )
    extract_tables: bool = Field(default=True, description="Extract tables from document")
    extract_images: bool = Field(default=True, description="Extract images from document")
    ocr_enabled: bool = Field(default=True, description="Enable OCR for scanned documents")
    table_mode: str = Field(default="accurate", description="Table extraction mode: fast or accurate")
    export_format: Optional[str] = Field(default="json", description="Export format: json, markdown, text")
    page_range: Optional[str] = Field(default=None, description="Page range to process (e.g., '1-5' or '1,3,5')")

# Response models
class DocumentAnalysisResponse(BaseModel):
    status: str
    filename: str
    mode: str
    pages_processed: int
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    message: Optional[str] = None

# Global document converter
converter = None

def initialize_converter(
    extract_tables: bool = True,
    ocr_enabled: bool = True,
    table_mode: str = "accurate"
):
    """Initialize the document converter with specified options"""
    try:
        # Configure pipeline options
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_table_structure = extract_tables
        pipeline_options.do_ocr = ocr_enabled
        
        if table_mode == "accurate":
            pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
        else:
            pipeline_options.table_structure_options.mode = TableFormerMode.FAST
        
        # Create converter with format options
        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        
        return converter
    except Exception as e:
        logger.error(f"Error initializing converter: {e}")
        raise

def process_document(
    file_path: str,
    mode: ProcessingMode,
    extract_tables: bool,
    extract_images: bool,
    ocr_enabled: bool,
    table_mode: str,
    export_format: str
) -> Dict[str, Any]:
    """Process document based on the specified mode"""
    
    # Initialize converter with options
    conv = initialize_converter(extract_tables, ocr_enabled, table_mode)
    
    # Convert document
    result = conv.convert(file_path)
    
    # Get document info
    doc = result.document
    num_pages = len(doc.pages) if hasattr(doc, 'pages') else 0
    
    # Process based on mode
    output = {
        "pages": num_pages,
        "content": {},
        "metadata": {}
    }
    
    try:
        if mode == ProcessingMode.TEXT_EXTRACTION:
            # Extract text only (using markdown with strict_text for plain text)
            output["content"]["text"] = doc.export_to_markdown(strict_text=True)
            
        elif mode == ProcessingMode.TABLE_EXTRACTION:
            # Export document and extract table information
            output["content"]["markdown"] = doc.export_to_markdown()
            output["content"]["text"] = doc.export_to_markdown(strict_text=True)
            output["metadata"]["note"] = "Tables are embedded in the markdown output"
            
        elif mode == ProcessingMode.IMAGE_EXTRACTION:
            # Export document with image information
            output["content"]["markdown"] = doc.export_to_markdown()
            output["metadata"]["note"] = "Image references are embedded in the markdown output"
            output["metadata"]["num_pages"] = num_pages
            
        elif mode == ProcessingMode.MARKDOWN_CONVERSION:
            # Convert to markdown
            output["content"]["markdown"] = doc.export_to_markdown()
            
        elif mode == ProcessingMode.JSON_EXPORT:
            # Export to JSON/dict
            output["content"]["json"] = doc.export_to_dict()
            
        elif mode == ProcessingMode.OCR_PROCESSING:
            # OCR processing - extract text
            output["content"]["text"] = doc.export_to_markdown(strict_text=True)
            output["content"]["markdown"] = doc.export_to_markdown()
            output["metadata"]["ocr_applied"] = ocr_enabled
            
        elif mode == ProcessingMode.FULL_ANALYSIS:
            # Full analysis - extract everything
            output["content"]["text"] = doc.export_to_markdown(strict_text=True)
            output["content"]["markdown"] = doc.export_to_markdown()
            output["content"]["json"] = doc.export_to_dict()
            output["metadata"]["num_pages"] = num_pages
            
        # Add metadata
        output["metadata"]["file_type"] = str(type(doc).__name__)
        output["metadata"]["processing_mode"] = mode.value
        output["metadata"]["conversion_status"] = str(result.status)
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        output["content"]["error"] = str(e)
        import traceback
        output["content"]["traceback"] = traceback.format_exc()
    
    return output

@app.get("/")
async def read_root():
    return {
        "message": "Docling Document Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze": "/api/analyze - POST - Upload and analyze documents"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "docling-analysis-server",
        "docling_available": True
    }

@app.post("/api/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(
    file: UploadFile = File(..., description="Document file to analyze (PDF, DOCX, PPTX, images, etc.)"),
    mode: ProcessingMode = Form(ProcessingMode.FULL_ANALYSIS, description="Processing mode"),
    extract_tables: bool = Form(True, description="Extract tables"),
    extract_images: bool = Form(True, description="Extract images"),
    ocr_enabled: bool = Form(True, description="Enable OCR"),
    table_mode: str = Form("accurate", description="Table extraction mode: fast or accurate"),
    export_format: str = Form("json", description="Export format")
):
    """
    Unified endpoint for document analysis and processing.
    
    Supported file types:
    - PDF documents
    - Microsoft Word (DOCX)
    - Microsoft PowerPoint (PPTX)
    - Images (PNG, JPG, TIFF) - with OCR
    - HTML documents
    - Markdown files
    
    Processing modes:
    - text_extraction: Extract text content only
    - table_extraction: Extract tables from document
    - image_extraction: Extract images and metadata
    - markdown_conversion: Convert to markdown format
    - json_export: Export structured JSON
    - ocr_processing: Apply OCR to images/scanned docs
    - full_analysis: Complete analysis with all features
    
    Parameters:
    - file: The document file to process
    - mode: Processing mode (default: full_analysis)
    - extract_tables: Whether to extract tables (default: true)
    - extract_images: Whether to extract images (default: true)
    - ocr_enabled: Enable OCR for scanned documents (default: true)
    - table_mode: Table extraction accuracy (fast/accurate)
    - export_format: Output format preference
    """
    
    temp_file_path = None
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Get file extension
        file_extension = Path(file.filename).suffix.lower()
        supported_extensions = ['.pdf', '.docx', '.pptx', '.png', '.jpg', '.jpeg', '.tiff', '.html', '.md']
        
        if file_extension not in supported_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_extension}. Supported: {', '.join(supported_extensions)}"
            )
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)
        
        logger.info(f"Processing file: {file.filename} with mode: {mode}")
        
        # Process the document
        result = process_document(
            file_path=temp_file_path,
            mode=mode,
            extract_tables=extract_tables,
            extract_images=extract_images,
            ocr_enabled=ocr_enabled,
            table_mode=table_mode,
            export_format=export_format
        )
        
        # Prepare response
        response = DocumentAnalysisResponse(
            status="success",
            filename=file.filename,
            mode=mode.value,
            pages_processed=result["pages"],
            content=result["content"],
            metadata=result["metadata"],
            message=f"Document processed successfully using {mode.value} mode"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Could not delete temp file: {e}")

@app.get("/api/modes")
async def get_processing_modes():
    """Get all available processing modes with descriptions"""
    return {
        "modes": [
            {
                "name": "text_extraction",
                "description": "Extract plain text content from document"
            },
            {
                "name": "table_extraction",
                "description": "Extract and parse tables from document"
            },
            {
                "name": "image_extraction",
                "description": "Extract images and their metadata"
            },
            {
                "name": "markdown_conversion",
                "description": "Convert document to markdown format"
            },
            {
                "name": "json_export",
                "description": "Export document as structured JSON"
            },
            {
                "name": "ocr_processing",
                "description": "Apply OCR to extract text from scanned documents/images"
            },
            {
                "name": "full_analysis",
                "description": "Complete analysis with all extraction features enabled"
            }
        ]
    }

@app.get("/api/supported-formats")
async def get_supported_formats():
    """Get all supported document formats"""
    return {
        "formats": [
            {"extension": ".pdf", "type": "PDF Document", "ocr_support": True},
            {"extension": ".docx", "type": "Microsoft Word", "ocr_support": False},
            {"extension": ".pptx", "type": "Microsoft PowerPoint", "ocr_support": False},
            {"extension": ".png", "type": "PNG Image", "ocr_support": True},
            {"extension": ".jpg/.jpeg", "type": "JPEG Image", "ocr_support": True},
            {"extension": ".tiff", "type": "TIFF Image", "ocr_support": True},
            {"extension": ".html", "type": "HTML Document", "ocr_support": False},
            {"extension": ".md", "type": "Markdown", "ocr_support": False}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)