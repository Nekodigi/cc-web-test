import functions_framework
from flask import Flask, send_from_directory, jsonify, request
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        expression = data.get('expression', '')
        # 安全な計算のためにeval使用（本番環境では注意が必要）
        result = eval(expression)
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': '0で割ることはできません'}), 400
    except Exception as e:
        return jsonify({'error': '計算エラー'}), 400

@functions_framework.http
def main(request):
    with app.app_context():
        return app.full_dispatch_request()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
