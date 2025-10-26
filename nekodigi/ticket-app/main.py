import os
import json
import uuid
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import qrcode
import io
import base64
from firebase_admin import credentials, initialize_app, db
import firebase_admin

# Firebase初期化
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "sandbox-35d1d",
        "private_key_id": "dummy",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDummy\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk@sandbox-35d1d.iam.gserviceaccount.com",
        "client_id": "dummy",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    })

    # Admin SDKなしでRealtimeデータベースを使用
    # Firebaseの設定
    DATABASE_URL = "https://sandbox-35d1d-default-rtdb.firebaseio.com"

app = Flask(__name__)
CORS(app)

DEVELOPER_ID = os.environ.get('DEVELOPER_ID', 'default_dev')
APP_ID = os.environ.get('APP_ID', 'default_app')
BASE_PATH = f"pracClass/{DEVELOPER_ID}/apps/{APP_ID}"

# Firebaseクライアントライブラリを使わず、REST APIを直接使用
import requests

def get_firebase_ref(path):
    """Firebaseパスの完全URLを取得"""
    return f"{DATABASE_URL}/{BASE_PATH}/{path}.json"

def firebase_get(path):
    """Firebaseからデータを取得"""
    try:
        response = requests.get(get_firebase_ref(path))
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Firebase GET error: {e}")
        return None

def firebase_put(path, data):
    """Firebaseにデータを保存"""
    try:
        response = requests.put(get_firebase_ref(path), json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Firebase PUT error: {e}")
        return False

def firebase_patch(path, data):
    """Firebaseのデータを更新"""
    try:
        response = requests.patch(get_firebase_ref(path), json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Firebase PATCH error: {e}")
        return False

def generate_qr_code(data):
    """QRコードを生成してBase64エンコード"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Base64エンコード
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"

@app.route('/')
def index():
    """HTMLページを返す"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "index.html not found", 404

@app.route('/api/create-ticket', methods=['POST'])
def create_ticket():
    """チケットを作成"""
    try:
        data = request.json
        event_name = data.get('event_name', 'イベント')
        ticket_count = int(data.get('ticket_count', 1))

        tickets = []
        for _ in range(ticket_count):
            ticket_id = str(uuid.uuid4())
            ticket_data = {
                'id': ticket_id,
                'event_name': event_name,
                'created_at': datetime.now().isoformat(),
                'used': False,
                'used_at': None
            }

            # Firebaseに保存
            if firebase_put(f"tickets/{ticket_id}", ticket_data):
                # QRコード生成
                qr_data = json.dumps({
                    'ticket_id': ticket_id,
                    'event_name': event_name
                })
                qr_image = generate_qr_code(qr_data)

                tickets.append({
                    'ticket_id': ticket_id,
                    'event_name': event_name,
                    'qr_code': qr_image,
                    'created_at': ticket_data['created_at']
                })

        return jsonify({
            'success': True,
            'tickets': tickets
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/validate-ticket', methods=['POST'])
def validate_ticket():
    """チケットを検証・使用"""
    try:
        data = request.json
        ticket_id = data.get('ticket_id')

        if not ticket_id:
            return jsonify({
                'success': False,
                'error': 'チケットIDが必要です'
            }), 400

        # チケット情報を取得
        ticket = firebase_get(f"tickets/{ticket_id}")

        if not ticket:
            return jsonify({
                'success': False,
                'valid': False,
                'error': 'チケットが見つかりません'
            })

        if ticket.get('used'):
            return jsonify({
                'success': True,
                'valid': False,
                'error': '既に使用済みのチケットです',
                'used_at': ticket.get('used_at')
            })

        # チケットを使用済みにする
        firebase_patch(f"tickets/{ticket_id}", {
            'used': True,
            'used_at': datetime.now().isoformat()
        })

        return jsonify({
            'success': True,
            'valid': True,
            'ticket': ticket
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/check-ticket', methods=['POST'])
def check_ticket():
    """チケット状態を確認（使用しない）"""
    try:
        data = request.json
        ticket_id = data.get('ticket_id')

        if not ticket_id:
            return jsonify({
                'success': False,
                'error': 'チケットIDが必要です'
            }), 400

        ticket = firebase_get(f"tickets/{ticket_id}")

        if not ticket:
            return jsonify({
                'success': False,
                'found': False,
                'error': 'チケットが見つかりません'
            })

        return jsonify({
            'success': True,
            'found': True,
            'ticket': ticket
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """統計情報を取得"""
    try:
        tickets = firebase_get("tickets")

        if not tickets:
            return jsonify({
                'success': True,
                'total': 0,
                'used': 0,
                'unused': 0
            })

        total = len(tickets)
        used = sum(1 for t in tickets.values() if t.get('used'))

        return jsonify({
            'success': True,
            'total': total,
            'used': used,
            'unused': total - used
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def main(request):
    """Cloud Functions エントリーポイント"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
