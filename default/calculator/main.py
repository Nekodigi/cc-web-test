from flask import Flask, render_template, request, jsonify
import os
import math

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

def safe_eval(expression):
    """安全に数式を評価する"""
    # π を math.pi に置換
    expression = expression.replace('π', str(math.pi))
    expression = expression.replace('e', str(math.e))

    # 関数名の置換
    expression = expression.replace('sin(', 'math.sin(')
    expression = expression.replace('cos(', 'math.cos(')
    expression = expression.replace('tan(', 'math.tan(')
    expression = expression.replace('asin(', 'math.asin(')
    expression = expression.replace('acos(', 'math.acos(')
    expression = expression.replace('atan(', 'math.atan(')
    expression = expression.replace('log(', 'math.log10(')
    expression = expression.replace('ln(', 'math.log(')
    expression = expression.replace('sqrt(', 'math.sqrt(')
    expression = expression.replace('pow(', 'math.pow(')
    expression = expression.replace('^', '**')

    # 安全性チェック: 許可された文字のみ
    allowed_chars = set('0123456789+-*/().mathsincolgtanqrpwe*,% ')
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Invalid characters in expression")

    # 評価
    result = eval(expression, {"__builtins__": {}}, {"math": math})
    return result

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        if not expression:
            return jsonify({'error': 'No expression provided'}), 400

        result = safe_eval(expression)

        # 結果を適切にフォーマット
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)

        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': '0で割ることはできません'}), 400
    except Exception as e:
        return jsonify({'error': '計算エラー'}), 400

def main(request):
    """Cloud Functions entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
