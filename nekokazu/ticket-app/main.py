import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import qrcode
from io import BytesIO
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
CORS(app)

# Firebase初期化
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "sandbox-35d1d",
        "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID", ""),
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY", "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC\n-----END PRIVATE KEY-----\n").replace('\\n', '\n'),
        "client_email": f"firebase-adminsdk@sandbox-35d1d.iam.gserviceaccount.com",
        "client_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
    })
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sandbox-35d1d-default-rtdb.firebaseio.com'
    })

DEVELOPER_ID = os.environ.get('DEVELOPER_ID', 'default')
APP_ID = os.environ.get('APP_ID', 'ticket-app')

def get_db_ref():
    return db.reference(f'pracClass/{DEVELOPER_ID}/apps/{APP_ID}')

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/api/tickets/create', methods=['POST'])
def create_ticket():
    """チケット作成（登録不要）"""
    try:
        data = request.json
        ticket_id = str(uuid.uuid4())

        ticket_data = {
            'id': ticket_id,
            'name': data.get('name', 'チケット'),
            'description': data.get('description', ''),
            'created_at': datetime.now().isoformat(),
            'used': False,
            'used_at': None
        }

        # Firebaseに保存
        ref = get_db_ref()
        ref.child('tickets').child(ticket_id).set(ticket_data)

        return jsonify({
            'success': True,
            'ticket': ticket_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tickets/<ticket_id>/qr', methods=['GET'])
def get_qr_code(ticket_id):
    """QRコード画像生成"""
    try:
        # QRコード生成
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # チケットURL
        base_url = request.host_url.rstrip('/')
        ticket_url = f"{base_url}/api/tickets/{ticket_id}/verify"

        qr.add_data(ticket_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # BytesIOに保存
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tickets/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """チケット情報取得"""
    try:
        ref = get_db_ref()
        ticket = ref.child('tickets').child(ticket_id).get()

        if not ticket:
            return jsonify({'success': False, 'error': 'チケットが見つかりません'}), 404

        return jsonify({
            'success': True,
            'ticket': ticket
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tickets/<ticket_id>/verify', methods=['GET', 'POST'])
def verify_ticket(ticket_id):
    """チケット検証・使用"""
    try:
        ref = get_db_ref()
        ticket_ref = ref.child('tickets').child(ticket_id)
        ticket = ticket_ref.get()

        if not ticket:
            return jsonify({'success': False, 'error': 'チケットが見つかりません'}), 404

        if request.method == 'POST':
            # チケット使用
            if ticket.get('used'):
                return jsonify({
                    'success': False,
                    'error': '既に使用済みのチケットです',
                    'ticket': ticket
                }), 400

            ticket['used'] = True
            ticket['used_at'] = datetime.now().isoformat()
            ticket_ref.update(ticket)

        return jsonify({
            'success': True,
            'ticket': ticket
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tickets', methods=['GET'])
def list_tickets():
    """チケット一覧取得"""
    try:
        ref = get_db_ref()
        tickets = ref.child('tickets').get()

        if not tickets:
            return jsonify({'success': True, 'tickets': []})

        # 辞書から配列に変換
        ticket_list = [v for k, v in tickets.items()]
        # 作成日時でソート（新しい順）
        ticket_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        return jsonify({
            'success': True,
            'tickets': ticket_list
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def main(request):
    """Cloud Functions エントリーポイント"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
