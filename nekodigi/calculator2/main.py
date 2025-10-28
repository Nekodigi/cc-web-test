import functions_framework
from flask import Flask, render_template, request, jsonify
import os
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        if not expression:
            return jsonify({'error': '式が空です'}), 400

        # 危険な関数を除外
        if any(func in expression for func in ['__', 'import', 'eval', 'exec', 'open', 'lambda']):
            return jsonify({'error': '無効な式です'}), 400

        # 数字と演算子のみ許可
        if not re.match(r'^[\d+\-*/().%\s]+$', expression):
            return jsonify({'error': '無効な式です'}), 400

        result = eval(expression, {"__builtins__": {}})
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': '0で割ることはできません'}), 400
    except Exception as e:
        return jsonify({'error': '計算エラーが発生しました'}), 400

@functions_framework.http
def main(request):
    with app.app_context():
        return app(request.environ, lambda *args: None)
