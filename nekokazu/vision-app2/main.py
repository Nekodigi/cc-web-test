import os
import base64
import json
import functions_framework
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    logger.warning("OPENAI_API_KEY not found in environment variables")
    client = None
else:
    client = OpenAI(api_key=openai_api_key)


def analyze_image_with_context(base64_image: str, question: str) -> str:
    """Analyze image using GPT-4o Vision and answer the question"""
    if not client:
        return "Error: OpenAI API key not configured"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "text",
                            "text": question or "この画像の内容について詳しく説明してください。"
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        return f"Error: {str(e)}"


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Endpoint to analyze image and answer questions"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        base64_image = data.get('image', '')
        question = data.get('question', '')
        
        # Remove data URI prefix if present
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
        
        # Analyze the image
        answer = analyze_image_with_context(base64_image, question)
        
        return jsonify({
            'success': True,
            'answer': answer,
            'question': question
        })
    except Exception as e:
        logger.error(f"Error in /api/analyze: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Camera AI Analyzer'})


@app.route('/', methods=['GET'])
def index():
    """Serve the main HTML file"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "index.html not found", 404


@functions_framework.http
def main(request):
    """Cloud Functions entry point"""
    with app.request_context(request.environ):
        try:
            return app.full_dispatch_request()
        except Exception as e:
            logger.error(f"Error in request handling: {str(e)}")
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Get port from environment variable or default to 3000
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
