from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder='.', static_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        expression = data.get('expression', '')

        # 安全な数式評価（基本的な四則演算のみ）
        result = eval(expression)
        return jsonify({'result': result, 'error': None})
    except ZeroDivisionError:
        return jsonify({'result': None, 'error': '0で割ることはできません'})
    except Exception as e:
        return jsonify({'result': None, 'error': '計算エラーが発生しました'})

def main(request):
    """Cloud Functions entry point"""
    return app(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
