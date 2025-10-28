import functions_framework
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@functions_framework.http
def main(request):
    request.environ['SCRIPT_NAME'] = ''

    if request.path == '/' and request.method == 'GET':
        return render_template('index.html')

    if request.path == '/api/calculate' and request.method == 'POST':
        try:
            data = request.get_json()
            expression = data.get('expression', '').strip()

            if not expression:
                return jsonify({'error': 'Expression is required'}), 400

            # Simple evaluation with basic security (only numbers and operators)
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return jsonify({'error': 'Invalid characters'}), 400

            result = eval(expression)
            return jsonify({'result': result})
        except ZeroDivisionError:
            return jsonify({'error': 'Division by zero'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return 'Not Found', 404
