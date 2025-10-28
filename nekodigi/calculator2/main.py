import functions_framework
from flask import Flask, request, jsonify, send_file
import io

app = Flask(__name__)

@functions_framework.http
def main(request_obj):
    """HTTP Cloud Function."""
    if request_obj.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    if request_obj.path == '/' and request_obj.method == 'GET':
        return send_file(io.BytesIO(get_html()), mimetype='text/html')

    if request_obj.path == '/calculate' and request_obj.method == 'POST':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        try:
            data = request_obj.get_json()
            expression = data.get('expression', '')

            # Safe evaluation
            result = eval_expression(expression)
            return (jsonify({'result': result}), 200, headers)
        except Exception as e:
            return (jsonify({'error': str(e)}), 400, headers)

    return ('Not Found', 404)

def eval_expression(expression):
    """Safely evaluate mathematical expression."""
    # Remove spaces
    expression = expression.replace(' ', '')

    # Allow only numbers, operators, and parentheses
    allowed_chars = set('0123456789+-*/.()%')
    if not all(c in allowed_chars for c in expression):
        raise ValueError('Invalid characters in expression')

    try:
        result = eval(expression)
        return round(result, 10)
    except:
        raise ValueError('Invalid expression')

def get_html():
    """Return HTML content."""
    html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>電卓</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-500 to-purple-600 min-h-screen flex items-center justify-center">
    <div class="bg-white rounded-lg shadow-2xl p-8 w-80">
        <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">電卓</h1>

        <div class="mb-6">
            <input
                type="text"
                id="display"
                class="w-full p-4 text-right text-3xl border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 bg-gray-100"
                value="0"
                readonly
            >
        </div>

        <div class="grid grid-cols-4 gap-2">
            <button onclick="clearDisplay()" class="col-span-2 bg-red-500 hover:bg-red-600 text-white font-bold py-4 rounded-lg transition">AC</button>
            <button onclick="deleteLast()" class="bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 rounded-lg transition">DEL</button>
            <button onclick="appendOperator('/')" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-lg transition">÷</button>

            <button onclick="appendNumber('7')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">7</button>
            <button onclick="appendNumber('8')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">8</button>
            <button onclick="appendNumber('9')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">9</button>
            <button onclick="appendOperator('*')" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-lg transition">×</button>

            <button onclick="appendNumber('4')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">4</button>
            <button onclick="appendNumber('5')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">5</button>
            <button onclick="appendNumber('6')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">6</button>
            <button onclick="appendOperator('-')" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-lg transition">−</button>

            <button onclick="appendNumber('1')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">1</button>
            <button onclick="appendNumber('2')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">2</button>
            <button onclick="appendNumber('3')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">3</button>
            <button onclick="appendOperator('+')" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-lg transition">+</button>

            <button onclick="appendNumber('0')" class="col-span-2 bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">0</button>
            <button onclick="appendNumber('.')" class="bg-gray-200 hover:bg-gray-300 font-bold py-4 rounded-lg transition">.</button>
            <button onclick="calculate()" class="bg-green-500 hover:bg-green-600 text-white font-bold py-4 rounded-lg transition">=</button>
        </div>
    </div>

    <script>
        const display = document.getElementById('display');
        let currentInput = '0';

        function updateDisplay() {
            display.value = currentInput;
        }

        function appendNumber(num) {
            if (currentInput === '0' && num !== '.') {
                currentInput = num;
            } else if (num === '.' && currentInput.includes('.')) {
                return;
            } else {
                currentInput += num;
            }
            updateDisplay();
        }

        function appendOperator(op) {
            if (currentInput === '' || currentInput.endsWith('+') || currentInput.endsWith('-') || currentInput.endsWith('*') || currentInput.endsWith('/')) {
                return;
            }
            currentInput += op;
            updateDisplay();
        }

        function deleteLast() {
            if (currentInput.length > 1) {
                currentInput = currentInput.slice(0, -1);
            } else {
                currentInput = '0';
            }
            updateDisplay();
        }

        function clearDisplay() {
            currentInput = '0';
            updateDisplay();
        }

        function calculate() {
            try {
                fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ expression: currentInput })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        currentInput = 'エラー';
                    } else {
                        currentInput = String(data.result);
                    }
                    updateDisplay();
                });
            } catch (error) {
                currentInput = 'エラー';
                updateDisplay();
            }
        }

        updateDisplay();
    </script>
</body>
</html>"""
    return html.encode('utf-8')
