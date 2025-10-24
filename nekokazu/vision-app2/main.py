import os
import base64
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from io import BytesIO

app = Flask(__name__)
CORS(app)

# OpenAI API設定
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/', methods=['GET'])
def index():
    """HTMLを提供"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "index.html not found", 404

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """カメラから送られた画像をAIが分析"""
    try:
        data = request.get_json()

        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        # Base64エンコードされた画像データを取得
        image_data = data['image']
        question = data.get('question', 'この画像に何が写っていますか？')

        # base64プレフィックスを削除
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        # OpenAI Vision APIを使用（GPT-4o を使用）
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": question
                        }
                    ]
                }
            ],
            max_tokens=1024
        )

        result = response.choices[0].message.content

        return jsonify({
            'success': True,
            'result': result,
            'question': question
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """チャットエンドポイント"""
    try:
        data = request.get_json()
        message = data.get('message', '')

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=1024
        )

        result = response.choices[0].message.content

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """ヘルスチェック"""
    return jsonify({
        'status': 'ok',
        'model': 'camera-ai-app'
    })

if __name__ == '__main__':
    # Cloud Functionsでは自動でポート3000にバインドされます
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
