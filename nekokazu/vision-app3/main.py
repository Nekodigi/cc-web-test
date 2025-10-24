import os
import json
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI
import functions_framework

app = Flask(__name__)
CORS(app)

# OpenAI client initialization
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@app.route('/')
def index():
    """Serve the index.html file"""
    return send_file('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    """Analyze image with OpenAI Vision API and answer user's question"""
    try:
        data = request.json

        if not data or 'image' not in data or 'question' not in data:
            return jsonify({'error': 'Image and question are required'}), 400

        image_data = data['image']
        question = data['question']

        # Remove data URL prefix if present
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        # Call OpenAI Vision API with GPT-4 Vision
        response = client.chat.completions.create(
            model="gpt-4o",  # Latest vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        answer = response.choices[0].message.content

        return jsonify({
            'success': True,
            'answer': answer
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@functions_framework.http
def main(request):
    """Cloud Functions entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    # For local testing
    app.run(host='0.0.0.0', port=3000, debug=True)
