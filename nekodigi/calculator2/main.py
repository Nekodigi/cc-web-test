import os
import functions_framework
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@functions_framework.http
def main(request_obj):
    """HTTP Cloud Function."""
    if request_obj.method == 'OPTIONS':
        return '', 204

    # Serve index.html for root path
    if request_obj.path in ('/', ''):
        with open('index.html', 'r') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}

    # API endpoint for calculation
    if request_obj.path == '/api/calculate':
        if request_obj.method != 'POST':
            return jsonify({'error': 'Method not allowed'}), 405

        data = request_obj.get_json()
        expression = data.get('expression', '')

        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Not found'}), 404
