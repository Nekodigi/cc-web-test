import functions_framework
from flask import send_file, jsonify
import os
import math
import re

@functions_framework.http
def main(request):
    """HTTP Cloud Function entry point (port 3000)"""

    # Enable CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    # Serve index.html for root path
    if request.path == '/' or request.path == '':
        return send_file('index.html', mimetype='text/html'), 200, headers

    # API endpoint for calculation
    if request.path == '/api/calculate' and request.method == 'POST':
        try:
            data = request.get_json()
            expression = data.get('expression', '')

            if not expression:
                return jsonify({'success': False, 'error': '式が入力されていません'}), 400, headers

            # Calculate the result
            result = safe_eval(expression)

            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            return jsonify({
                'success': True,
                'result': result
            }), 200, headers

        except ZeroDivisionError:
            return jsonify({
                'success': False,
                'error': '0で割ることはできません'
            }), 400, headers
        except Exception as e:
            return jsonify({
                'success': False,
                'error': '計算エラー'
            }), 400, headers

    return jsonify({'error': 'Not found'}), 404, headers


def safe_eval(expression):
    """Safely evaluate mathematical expressions"""

    # Replace symbols
    expression = expression.replace('π', str(math.pi))
    expression = expression.replace('^', '**')
    expression = expression.replace('÷', '/')
    expression = expression.replace('×', '*')

    # Replace function names with math module equivalents
    expression = re.sub(r'\bsin\(', 'math.sin(', expression)
    expression = re.sub(r'\bcos\(', 'math.cos(', expression)
    expression = re.sub(r'\btan\(', 'math.tan(', expression)
    expression = re.sub(r'\basin\(', 'math.asin(', expression)
    expression = re.sub(r'\bacos\(', 'math.acos(', expression)
    expression = re.sub(r'\batan\(', 'math.atan(', expression)
    expression = re.sub(r'\bsqrt\(', 'math.sqrt(', expression)
    expression = re.sub(r'\blog\(', 'math.log10(', expression)
    expression = re.sub(r'\bln\(', 'math.log(', expression)
    expression = re.sub(r'\bexp\(', 'math.exp(', expression)
    expression = re.sub(r'\babs\(', 'abs(', expression)
    expression = re.sub(r'\bpow\(', 'math.pow(', expression)

    # Create a safe namespace with only math functions
    safe_dict = {
        'math': math,
        'abs': abs,
        '__builtins__': {}
    }

    # Evaluate the expression
    result = eval(expression, safe_dict)

    return result


if __name__ == '__main__':
    # For local testing
    from flask import Flask, request as flask_request
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
    def catch_all(path):
        return main(flask_request)

    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
