import functions_framework
from flask import Flask
import json

@functions_framework.http
def main(request):
    """HTTP Cloud Function for calculator app"""

    # CORS対応
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return '', 204, headers

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
    }

    # ルートへのアクセス
    if request.path == '/' and request.method == 'GET':
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content, 200, {'Content-Type': 'text/html; charset=utf-8', 'Access-Control-Allow-Origin': '*'}

    # 計算API
    if request.path == '/api/calculate' and request.method == 'POST':
        try:
            data = request.get_json()
            expression = data.get('expression', '')

            if not expression:
                return json.dumps({'error': 'No expression provided'}), 400, headers

            # 基本的な数式評価
            result = eval(expression, {"__builtins__": {}}, {})
            return json.dumps({'result': result}), 200, headers
        except Exception as e:
            return json.dumps({'error': str(e)}), 400, headers

    return json.dumps({'error': 'Not found'}), 404, headers
