import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder='.', static_folder='.')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        expression = data.get('expression', '')

        # セキュリティ: 数字、演算子、括弧のみを許可
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return jsonify({'error': '無効な入力'}), 400

        # eval を使用して計算
        result = eval(expression)
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': '0で除算することはできません'}), 400
    except Exception as e:
        return jsonify({'error': '計算エラー'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
