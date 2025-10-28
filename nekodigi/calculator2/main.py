import functions_framework
from flask import Flask, send_from_directory, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        expression = data.get('expression', '')
        result = eval(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@functions_framework.http
def main(request):
    with app.app_context():
        return app.full_dispatch_request()
