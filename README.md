# OCR Translation Backend

A Flask-based backend service for OCR and translation of text from images.

## Features

- Image text extraction using Tesseract OCR
- Text translation using Groq API
- Support for multiple languages
- RESTful API endpoints
- CORS enabled
- Production-ready configuration

## Prerequisites

- Python 3.9 or higher
- Tesseract OCR installed
- Groq API key

## Local Development Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:

```
GROQ_API_KEY=your_groq_api_key
PORT=7860
```

4. Run the development server:

```bash
python app.py
```

## Deployment to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following settings:

   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --config gunicorn_config.py`
   - Add environment variable: `GROQ_API_KEY`

4. Deploy!

## API Endpoints

- `GET /languages` - Get available languages
- `POST /translate/text` - Translate text
- `POST /translate/image` - Extract and translate text from images
- `GET /health` - Health check endpoint

## Environment Variables

- `GROQ_API_KEY`: Your Groq API key
- `PORT`: Port number (default: 7860)

## Production Considerations

- The service uses Gunicorn for production deployment
- Configured with 4 workers and 2 threads per worker
- Includes health check endpoint for monitoring
- Implements proper error handling and logging
- Uses environment variables for configuration
