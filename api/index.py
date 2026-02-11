"""
Font Parser Service
Extracts metadata from font files using fontTools library.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fontTools.ttLib import TTFont
from pydantic import BaseModel
from typing import Optional
from mangum import Mangum
import tempfile
import os

app = FastAPI(
    title="Font Parser Service",
    description="Extract metadata from font files (TTF, OTF, WOFF, WOFF2)",
    version="1.0.0"
)

# CORS middleware for Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.(vercel\.app|typeyeah\.com)|http://localhost:(3000|3003)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FontMetadata(BaseModel):
    """Font metadata extracted from font file"""
    # Name table fields
    family: Optional[str] = None
    subfamily: Optional[str] = None
    full_name: Optional[str] = None
    postscript_name: Optional[str] = None
    manufacturer: Optional[str] = None
    designer: Optional[str] = None
    copyright: Optional[str] = None
    vendor_url: Optional[str] = None
    licence_description: Optional[str] = None
    licence_url: Optional[str] = None

    # OS/2 table fields
    vendor_id: Optional[str] = None
    fs_type: Optional[int] = None

    # Additional metadata
    version: Optional[str] = None
    unique_id: Optional[str] = None

    # File info
    file_format: Optional[str] = None
    num_glyphs: Optional[int] = None


def extract_font_metadata(font_file_path: str) -> FontMetadata:
    """
    Extract metadata from a font file using fontTools.

    Args:
        font_file_path: Path to the font file

    Returns:
        FontMetadata object with extracted data
    """
    try:
        font = TTFont(font_file_path)

        # Extract name table
        name_table = font.get("name")
        metadata = {}

        if name_table:
            # Name IDs according to OpenType spec
            name_ids = {
                0: "copyright",
                1: "family",
                2: "subfamily",
                3: "unique_id",
                4: "full_name",
                5: "version",
                6: "postscript_name",
                8: "manufacturer",
                9: "designer",
                11: "vendor_url",
                13: "licence_description",
                14: "licence_url",
            }

            for name_id, field_name in name_ids.items():
                try:
                    value = name_table.getDebugName(name_id)
                    if value:
                        metadata[field_name] = value.strip()
                except Exception:
                    pass

        # Extract OS/2 table
        if "OS/2" in font:
            os2 = font["OS/2"]
            try:
                metadata["vendor_id"] = os2.achVendID.strip() if hasattr(os2, 'achVendID') else None
                metadata["fs_type"] = os2.fsType if hasattr(os2, 'fsType') else None
            except Exception:
                pass

        # Get file format and glyph count
        metadata["file_format"] = font.sfntVersion
        metadata["num_glyphs"] = font.get("maxp").numGlyphs if "maxp" in font else None

        font.close()

        return FontMetadata(**metadata)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse font file: {str(e)}"
        )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Font Parser Service",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.post("/parse", response_model=FontMetadata)
async def parse_font(file: UploadFile = File(...)):
    """
    Parse a font file and extract metadata.

    Supports: .ttf, .otf, .woff, .woff2
    """
    # Validate file extension
    allowed_extensions = ['.ttf', '.otf', '.woff', '.woff2']
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Save uploaded file to temporary location
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        # Extract metadata
        metadata = extract_font_metadata(temp_path)

        return metadata

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


# Wrap the FastAPI app with Mangum for Vercel serverless deployment
handler = Mangum(app, lifespan="off")
