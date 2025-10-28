import functions_framework
from flask import request, jsonify
import os

@functions_framework.http
def main(request_obj):
    """HTTP Cloud Function."""
    # CORS対応
    if request_obj.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # ルートはindex.htmlを返す
    if request_obj.path == '/' and request_obj.method == 'GET':
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            return (html_content, 200, {**headers, 'Content-Type': 'text/html'})
        except FileNotFoundError:
            return ('index.html not found', 404, headers)

    # 計算API
    if request_obj.path == '/calculate' and request_obj.method == 'POST':
        try:
            data = request_obj.get_json()
            expression = data.get('expression', '')
            result = eval_expression(expression)
            return (jsonify({'result': result}).get_data(as_text=True), 200, headers)
        except ValueError as e:
            return (jsonify({'error': str(e)}).get_data(as_text=True), 400, headers)
        except Exception as e:
            return (jsonify({'error': '計算エラー'}).get_data(as_text=True), 400, headers)

    return ('Not Found', 404, headers)

def eval_expression(expression):
    """Safely evaluate mathematical expression."""
    expression = expression.replace(' ', '')

    # 許可された文字のみ
    allowed_chars = set('0123456789+-*/.()%')
    if not all(c in allowed_chars for c in expression):
        raise ValueError('無効な文字が含まれています')

    try:
        result = eval(expression)
        return round(float(result), 10)
    except ZeroDivisionError:
        raise ValueError('ゼロで除算できません')
    except:
        raise ValueError('無効な式です')
