from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        # セキュリティのため、許可された文字のみを処理
        allowed_chars = set('0123456789+-*/().% ')
        if not all(c in allowed_chars for c in expression):
            return jsonify({'error': '無効な文字が含まれています'}), 400

        # 計算実行
        result = eval(expression)
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
