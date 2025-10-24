import os
import json
import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from werkzeug.exceptions import BadRequest

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

# Initialize Google Generative AI
# Use GoogleAIStudio API key (not OpenAI key)
api_key = os.environ.get('GOOGLE_AI_KEY') or os.environ.get('GoogleAIStudio')
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GoogleAIStudio API key not set. Set GOOGLE_AI_KEY or GoogleAIStudio environment variable")

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    """
    Analyze an image and answer questions about it using Google Generative AI

    Expected JSON payload:
    {
        "image": "base64-encoded-image-data",
        "question": "Question about the image",
        "imageType": "image/jpeg" or "image/png" (optional)
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data provided'}), BadRequest.code

        image_data = data.get('image')
        question = data.get('question')
        image_type = data.get('imageType', 'image/jpeg')

        if not image_data:
            return jsonify({'error': 'No image data provided'}), BadRequest.code

        if not question:
            return jsonify({'error': 'No question provided'}), BadRequest.code

        # Remove data URL prefix if present
        if image_data.startswith('data:'):
            image_data = image_data.split(',')[1]

        # Decode base64 image
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            return jsonify({'error': f'Invalid base64 image data: {str(e)}'}), BadRequest.code

        # Get the model
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Convert image bytes to PIL Image for proper handling
        from PIL import Image
        from io import BytesIO

        try:
            image = Image.open(BytesIO(image_bytes))
        except Exception as e:
            return jsonify({'error': f'Failed to process image: {str(e)}'}), BadRequest.code

        # Create content with image and question
        message = model.generate_content([
            image,
            question
        ])

        answer = message.text if message.text else "回答を生成できませんでした。"

        return jsonify({
            'success': True,
            'answer': answer,
            'question': question
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def main(request):
    """HTTP Cloud Function entry point for Google Cloud Functions"""
    return app(request.environ, lambda status, headers: None)


if __name__ == '__main__':
    # Run on port 3000 as specified
    app.run(host='0.0.0.0', port=3000, debug=False)
