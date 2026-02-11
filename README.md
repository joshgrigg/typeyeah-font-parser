# Font Parser Service

FastAPI service for extracting metadata from font files using fontTools.

## Features

- Extracts comprehensive metadata from font files
- Supports TTF, OTF, WOFF, and WOFF2 formats
- Returns structured JSON with font details
- CORS-enabled for Next.js integration

## Setup

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
python main.py
```

The service will be available at http://localhost:8000

## API Documentation

Once running, visit:
- API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Endpoints

### `GET /`
Health check endpoint

### `POST /parse`
Upload a font file and receive extracted metadata

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (font file)

**Response:**
```json
{
  "family": "Helvetica Neue",
  "subfamily": "Bold",
  "full_name": "Helvetica Neue Bold",
  "postscript_name": "HelveticaNeue-Bold",
  "manufacturer": "Linotype GmbH",
  "designer": "Max Miedinger",
  "copyright": "© 2020 Linotype GmbH",
  "vendor_url": "http://www.linotype.com",
  "licence_description": "...",
  "licence_url": "http://www.linotype.com/eula",
  "vendor_id": "LINO",
  "fs_type": 8,
  "version": "Version 1.00",
  "unique_id": "...",
  "file_format": "OTTO",
  "num_glyphs": 1200
}
```

## Deployment

### Vercel (Recommended)

1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to service directory: `cd services/font-parser`
3. Deploy: `vercel --prod`
4. Note the deployment URL (e.g., `https://font-parser-xxx.vercel.app`)
5. Add to Portal environment variables:
   ```
   NEXT_PUBLIC_FONT_PARSER_URL=https://font-parser-xxx.vercel.app
   ```

The `vercel.json` configuration is already set up for Python FastAPI deployment.

### Docker

```bash
docker build -t font-parser .
docker run -p 8000:8000 font-parser
```

### Local Development

For local development with the portal:
1. Run the service locally: `python main.py`
2. Service runs at `http://localhost:8000`
3. No environment variable needed (defaults to localhost)

## Integration with Portal

The portal app will use the Python service URL from:
- Production: `NEXT_PUBLIC_FONT_PARSER_URL` environment variable
- Development: Defaults to `http://localhost:8000`

To test the integration:
1. Start the Python service
2. Navigate to Portal `/dashboard/fonts/new`
3. Upload a font file
4. Metadata will be extracted and form fields pre-populated

## Testing

```bash
curl -X POST "http://localhost:8000/parse" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/font.ttf"
```
