import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import math
import re

app = Flask(__name__, static_folder='.')
CORS(app)

def safe_eval(expression):
    """安全に数式を評価する"""
    try:
        # 許可する関数と定数
        safe_dict = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sinh': math.sinh,
            'cosh': math.cosh,
            'tanh': math.tanh,
            'sqrt': math.sqrt,
            'log': math.log10,
            'ln': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'pow': pow,
            'abs': abs,
            'pi': math.pi,
            'e': math.e,
            'ceil': math.ceil,
            'floor': math.floor,
            'factorial': math.factorial,
            'degrees': math.degrees,
            'radians': math.radians,
        }

        # 危険な文字列をチェック
        dangerous = ['__', 'import', 'exec', 'eval', 'open', 'file']
        for d in dangerous:
            if d in expression.lower():
                raise ValueError("不正な式です")

        # 式を処理
        expr = expression.replace('^', '**')
        expr = expr.replace('π', str(math.pi))
        expr = expr.replace('√', 'sqrt')

        # 暗黙の乗算を明示的に（例: 2π → 2*π, 2(3) → 2*(3)）
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
        expr = re.sub(r'(\))(\d|[a-zA-Z(])', r'\1*\2', expr)

        # 評価
        result = eval(expr, {"__builtins__": {}}, safe_dict)

        return float(result)
    except ZeroDivisionError:
        raise ValueError("ゼロ除算エラー")
    except Exception as e:
        raise ValueError(f"計算エラー: {str(e)}")

@app.route('/')
def index():
    """index.htmlを返す"""
    return send_from_directory('.', 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """計算APIエンドポイント"""
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        if not expression:
            return jsonify({'error': '式が空です'}), 400

        result = safe_eval(expression)

        return jsonify({
            'result': result,
            'expression': expression
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500

@app.route('/health')
def health():
    """ヘルスチェック"""
    return jsonify({'status': 'ok'})

def main(request):
    """Cloud Functions用のエントリーポイント"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
