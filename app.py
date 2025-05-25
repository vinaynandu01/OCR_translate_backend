from flask import Flask, request, jsonify
import base64
import os
import requests
from flask_cors import CORS
from PIL import Image
import pytesseract
import json
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API key from environment variable
groq_api_key = os.getenv("GROQ_API_KEY", "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")
api_url = "https://api.groq.com/openai/v1/chat/completions"

# Configure Tesseract path based on environment
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:  # Linux/Unix
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Available languages in Tesseract
TESSERACT_LANGUAGES = {
    # European Languages
    'eng': 'English',
    'fra': 'French',
    'deu': 'German',
    'spa': 'Spanish',
    'ita': 'Italian',
    'por': 'Portuguese',
    'rus': 'Russian',
    'pol': 'Polish',
    'ukr': 'Ukrainian',
    'bel': 'Belarusian',
    'bul': 'Bulgarian',
    'hrv': 'Croatian',
    'ces': 'Czech',
    'dan': 'Danish',
    'est': 'Estonian',
    'fin': 'Finnish',
    'grc': 'Greek',
    'hun': 'Hungarian',
    'isl': 'Icelandic',
    'lav': 'Latvian',
    'lit': 'Lithuanian',
    'nld': 'Dutch',
    'nor': 'Norwegian',
    'ron': 'Romanian',
    'slk': 'Slovak',
    'slv': 'Slovenian',
    'swe': 'Swedish',
    'tur': 'Turkish',

    # Asian Languages
    'chi_sim': 'Chinese (Simplified)',
    'chi_tra': 'Chinese (Traditional)',
    'jpn': 'Japanese',
    'kor': 'Korean',
    'tha': 'Thai',
    'vie': 'Vietnamese',
    'hin': 'Hindi',
    'mar': 'Marathi',
    'guj': 'Gujarati',
    'ben': 'Bengali',
    'tam': 'Tamil',
    'tel': 'Telugu',
    'kan': 'Kannada',
    'mal': 'Malayalam',
    'pan': 'Punjabi',
    'urd': 'Urdu',

    # Middle Eastern Languages
    'ara': 'Arabic',
    'heb': 'Hebrew',
    'fas': 'Persian',

    # Other Languages
    'lat': 'Latin',
    'epo': 'Esperanto'
}

def translate_text(text, target_lang):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a translator. Translate the given text to the specified language. Only provide the translation, no explanations or additional text."
            },
            {
                "role": "user",
                "content": f"Translate this text to {target_lang}: {text}"
            }
        ]

        payload = {
            "model": "llama3-8b-8192",
            "messages": messages,
            "max_tokens": 300
        }

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(api_url, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            response_data = response.json()
            response_text = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response")
            return response_text.strip()
        else:
            app.logger.error(f"Translation API error: {response.status_code} - {response.text}")
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        app.logger.error(f"Translation error: {str(e)}")
        return f"Error: {str(e)}"

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "status": "running",
        "message": "OCR Translation API is running",
        "endpoints": {
            "languages": "/languages",
            "translate_text": "/translate/text",
            "translate_image": "/translate/image",
            "health": "/health"
        }
    })

@app.route("/languages", methods=["GET"])
def get_languages():
    return jsonify(TESSERACT_LANGUAGES)

@app.route("/translate/text", methods=["POST"])
def translate_text_input():
    try:
        data = request.json
        text = data.get("text", "")
        target_lang = data.get("target_lang", "en")
        
        if not text:
            return jsonify({"error": "No text provided"}), 400

        translated_text = translate_text(text, target_lang)
        return jsonify({
            "original_text": text,
            "translated_text": translated_text
        })
    except Exception as e:
        app.logger.error(f"Text translation error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/translate/image", methods=["POST"])
def translate_image():
    try:
        if "images" not in request.files:
            return jsonify({"error": "No images provided"}), 400
        
        files = request.files.getlist("images")
        if len(files) > 5:
            return jsonify({"error": "Maximum 5 images allowed"}), 400

        source_lang = request.form.get("source_lang", "eng")
        target_lang = request.form.get("target_lang", "en")
        
        results = []
        
        for file in files:
            if file.filename == "":
                continue

            try:
                # Read the image directly into memory
                image_bytes = file.read()
                image = Image.open(BytesIO(image_bytes))

                # Perform OCR on the image
                text = pytesseract.image_to_string(
                    image,
                    lang=source_lang,
                    config='--psm 6'
                )
                
                if text.strip():
                    # Translate the extracted text
                    translated_text = translate_text(text, target_lang)
                    results.append({
                        "original_text": text.strip(),
                        "translated_text": translated_text
                    })
            except Exception as e:
                app.logger.error(f"Image processing error: {str(e)}")
                continue

        if not results:
            return jsonify({"error": "No text found in any of the images"}), 400

        return jsonify({
            "results": results
        })

    except Exception as e:
        app.logger.error(f"Image translation error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
