import functions_framework
from flask import request, jsonify
import json

# HTMLコンテンツをここに埋め込み
HTML_CONTENT = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>電卓</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-500 to-purple-600 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-sm">
        <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">電卓</h1>

        <div class="mb-6">
            <input
                type="text"
                id="display"
                readonly
                class="w-full px-6 py-4 text-right text-4xl font-bold border-2 border-gray-300 rounded-xl bg-gray-50 focus:outline-none focus:border-blue-500"
                value="0"
            >
        </div>

        <div class="grid grid-cols-4 gap-3">
            <button onclick="clearDisplay()" class="col-span-2 bg-red-500 hover:bg-red-600 active:bg-red-700 text-white font-bold py-4 rounded-lg transition duration-150">AC</button>
            <button onclick="deleteLast()" class="bg-orange-500 hover:bg-orange-600 active:bg-orange-700 text-white font-bold py-4 rounded-lg transition duration-150">DEL</button>
            <button onclick="appendOperator('/')" class="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-bold py-4 rounded-lg transition duration-150">÷</button>

            <button onclick="appendNumber('7')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">7</button>
            <button onclick="appendNumber('8')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">8</button>
            <button onclick="appendNumber('9')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">9</button>
            <button onclick="appendOperator('*')" class="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-bold py-4 rounded-lg transition duration-150">×</button>

            <button onclick="appendNumber('4')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">4</button>
            <button onclick="appendNumber('5')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">5</button>
            <button onclick="appendNumber('6')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">6</button>
            <button onclick="appendOperator('-')" class="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-bold py-4 rounded-lg transition duration-150">−</button>

            <button onclick="appendNumber('1')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">1</button>
            <button onclick="appendNumber('2')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">2</button>
            <button onclick="appendNumber('3')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">3</button>
            <button onclick="appendOperator('+')" class="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 text-white font-bold py-4 rounded-lg transition duration-150">+</button>

            <button onclick="appendNumber('0')" class="col-span-2 bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">0</button>
            <button onclick="appendNumber('.')" class="bg-gray-200 hover:bg-gray-300 active:bg-gray-400 font-bold py-4 rounded-lg transition duration-150">.</button>
            <button onclick="calculate()" class="bg-green-500 hover:bg-green-600 active:bg-green-700 text-white font-bold py-4 rounded-lg transition duration-150">=</button>
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
            const lastChar = currentInput.slice(-1);
            if (lastChar === '+' || lastChar === '-' || lastChar === '*' || lastChar === '/') {
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
            fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ expression: currentInput })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    currentInput = data.error;
                } else {
                    currentInput = String(data.result);
                }
                updateDisplay();
            })
            .catch(() => {
                currentInput = 'エラー';
                updateDisplay();
            });
        }

        updateDisplay();
    </script>
</body>
</html>"""

@functions_framework.http
def main(request_obj):
    """HTTP Cloud Function."""
    # CORS対応
    if request_obj.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # ルートはHTMLを返す
    if request_obj.path == '/' and request_obj.method == 'GET':
        return (HTML_CONTENT, 200, {**headers, 'Content-Type': 'text/html; charset=utf-8'})

    # 計算API
    if request_obj.path == '/calculate' and request_obj.method == 'POST':
        try:
            data = request_obj.get_json()
            expression = data.get('expression', '')
            result = eval_expression(expression)
            response = json.dumps({'result': result})
            return (response, 200, {**headers, 'Content-Type': 'application/json'})
        except ValueError as e:
            response = json.dumps({'error': str(e)})
            return (response, 400, {**headers, 'Content-Type': 'application/json'})
        except Exception as e:
            response = json.dumps({'error': '計算エラー'})
            return (response, 400, {**headers, 'Content-Type': 'application/json'})

    return ('Not Found', 404, headers)

def eval_expression(expression):
    """Safely evaluate mathematical expression."""
    expression = expression.replace(' ', '')

    # 許可された文字のみ
    allowed_chars = set('0123456789+-*/.()%')
    if not all(c in allowed_chars for c in expression):
        raise ValueError('無効な文字が含まれています')

    try:
        result = eval(expression)
        return round(float(result), 10)
    except ZeroDivisionError:
        raise ValueError('ゼロで除算できません')
    except:
        raise ValueError('無効な式です')
