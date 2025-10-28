import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calculate mathematical expression safely"""
    try:
        data = request.get_json()
        expression = data.get('expression', '').strip()

        if not expression:
            return jsonify({'error': 'Expression is empty'}), 400

        # Allow only safe operations: numbers, operators, parentheses, decimal points
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return jsonify({'error': 'Invalid characters in expression'}), 400

        # Evaluate the expression safely
        result = eval(expression)
        return jsonify({'result': result})

    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except SyntaxError:
        return jsonify({'error': 'Invalid expression syntax'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def main(request):
    """Cloud Functions entry point"""
    return app(request)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
