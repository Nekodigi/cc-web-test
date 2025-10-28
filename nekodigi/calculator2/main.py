import functions_framework
import json
import os

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

    cors_headers = {
        'Access-Control-Allow-Origin': '*',
    }

    # ルートへのアクセス
    if request.path == '/' and request.method == 'GET':
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            return html_content, 200, {
                'Content-Type': 'text/html; charset=utf-8',
                **cors_headers
            }
        except FileNotFoundError:
            return '<!DOCTYPE html><html><body>index.html not found</body></html>', 404, {
                'Content-Type': 'text/html; charset=utf-8',
                **cors_headers
            }

    # 計算API
    if request.path == '/api/calculate' and request.method == 'POST':
        try:
            data = request.get_json()
            expression = data.get('expression', '').strip()

            if not expression:
                return json.dumps({'error': 'No expression provided'}), 400, {
                    'Content-Type': 'application/json',
                    **cors_headers
                }

            # 安全な数式評価（許可されたものだけ）
            allowed_names = {
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                'sum': sum,
            }
            result = eval(expression, {"__builtins__": {}}, allowed_names)

            return json.dumps({'result': result}), 200, {
                'Content-Type': 'application/json',
                **cors_headers
            }
        except ZeroDivisionError:
            return json.dumps({'error': 'Division by zero'}), 400, {
                'Content-Type': 'application/json',
                **cors_headers
            }
        except Exception as e:
            return json.dumps({'error': str(e)}), 400, {
                'Content-Type': 'application/json',
                **cors_headers
            }

    return json.dumps({'error': 'Not found'}), 404, {
        'Content-Type': 'application/json',
        **cors_headers
    }
