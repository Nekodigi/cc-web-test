import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

# 環境変数
DEVELOPER_ID = os.environ.get('DEVELOPER_ID', 'default_dev')
APP_ID = os.environ.get('APP_ID', 'default_app')

@app.route('/')
def index():
    """HTMLファイルを返す"""
    return send_from_directory('.', 'index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    """フロントエンド用の設定を返す"""
    return jsonify({
        'firebaseConfig': {
            'apiKey': 'AIzaSyChB7eBjMaX_lRpfIgUxQDi39Qh82R4oyQ',
            'authDomain': 'sandbox-35d1d.firebaseapp.com',
            'databaseURL': 'https://sandbox-35d1d-default-rtdb.firebaseio.com',
            'projectId': 'sandbox-35d1d',
            'storageBucket': 'sandbox-35d1d.appspot.com',
            'messagingSenderId': '906287459396',
            'appId': '1:906287459396:web:c931c95d943157cae36011',
            'measurementId': 'G-LE2Q0XC7B6'
        },
        'developerId': DEVELOPER_ID,
        'appId': APP_ID,
        'dbPath': f'pracClass/{DEVELOPER_ID}/apps/{APP_ID}'
    })

@app.route('/health')
def health():
    """ヘルスチェック"""
    return jsonify({'status': 'ok'})

def main(request):
    """Cloud Functions エントリーポイント"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    # ローカル開発用
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
