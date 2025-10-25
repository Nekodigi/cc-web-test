import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import qrcode
from io import BytesIO

app = Flask(__name__)
CORS(app)

# メモリ内ストレージ（登録不要・シンプル・高可用性）
tickets_storage = {}

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

        # メモリに保存
        tickets_storage[ticket_id] = ticket_data

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
        ticket = tickets_storage.get(ticket_id)

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
        ticket = tickets_storage.get(ticket_id)

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
            tickets_storage[ticket_id] = ticket

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
        if not tickets_storage:
            return jsonify({'success': True, 'tickets': []})

        # 辞書から配列に変換
        ticket_list = list(tickets_storage.values())
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
