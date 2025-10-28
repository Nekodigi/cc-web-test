import functions_framework
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        if not expression:
            return jsonify({'error': '式が空です'}), 400

        result = eval(expression)
        return jsonify({'result': result})
    except ZeroDivisionError:
        return jsonify({'error': '0で割ることはできません'}), 400
    except Exception as e:
        return jsonify({'error': f'計算エラー: {str(e)}'}), 400

@functions_framework.http
def main(request):
    with app.app_context():
        return app(request.environ, lambda *args: None)
