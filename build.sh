#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Tesseract and language data
apt-get update
apt-get install -y tesseract-ocr
apt-get install -y tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-deu tesseract-ocr-spa tesseract-ocr-ita tesseract-ocr-por tesseract-ocr-rus tesseract-ocr-pol tesseract-ocr-ukr tesseract-ocr-bel tesseract-ocr-bul tesseract-ocr-hrv tesseract-ocr-ces tesseract-ocr-dan tesseract-ocr-est tesseract-ocr-fin tesseract-ocr-grc tesseract-ocr-hun tesseract-ocr-isl tesseract-ocr-lav tesseract-ocr-lit tesseract-ocr-nld tesseract-ocr-nor tesseract-ocr-ron tesseract-ocr-slk tesseract-ocr-slv tesseract-ocr-swe tesseract-ocr-tur tesseract-ocr-chi-sim tesseract-ocr-chi-tra tesseract-ocr-jpn tesseract-ocr-kor tesseract-ocr-tha tesseract-ocr-vie tesseract-ocr-hin tesseract-ocr-mar tesseract-ocr-guj tesseract-ocr-ben tesseract-ocr-tam tesseract-ocr-tel tesseract-ocr-kan tesseract-ocr-mal tesseract-ocr-pan tesseract-ocr-urd tesseract-ocr-ara tesseract-ocr-heb tesseract-ocr-fas tesseract-ocr-lat tesseract-ocr-epo

# Install Python dependencies
pip install -r requirements.txt 