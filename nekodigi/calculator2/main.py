import functions_framework
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>電卓</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-sm">
        <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">電卓</h1>

        <div class="mb-6">
            <input
                id="display"
                type="text"
                readonly
                class="w-full p-4 text-right text-4xl font-bold bg-gray-100 rounded-lg border-2 border-indigo-200 focus:border-indigo-500 focus:outline-none"
                value="0"
            >
        </div>

        <div class="grid grid-cols-4 gap-3">
            <!-- Row 1 -->
            <button class="btn-clear col-span-2 bg-red-500 hover:bg-red-600 text-white font-bold py-4 px-6 rounded-lg transition">AC</button>
            <button class="btn-op bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 px-6 rounded-lg transition">/</button>
            <button class="btn-op bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 px-6 rounded-lg transition">*</button>

            <!-- Row 2 -->
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">7</button>
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">8</button>
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">9</button>
            <button class="btn-op bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 px-6 rounded-lg transition">-</button>

            <!-- Row 3 -->
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">4</button>
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">5</button>
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">6</button>
            <button class="btn-op bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 px-6 rounded-lg transition">+</button>

            <!-- Row 4 -->
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">1</button>
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">2</button>
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">3</button>
            <button class="btn-equal bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-6 rounded-lg transition row-span-2">=</button>

            <!-- Row 5 -->
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition col-span-2">0</button>
            <button class="btn-num bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 px-6 rounded-lg transition">.</button>
        </div>
    </div>

    <script>
        const display = document.getElementById('display');
        let currentValue = '0';
        let previousValue = '';
        let operator = null;
        let shouldResetDisplay = false;

        document.querySelectorAll('.btn-num').forEach(btn => {
            btn.addEventListener('click', function() {
                const num = this.textContent;

                if (shouldResetDisplay) {
                    currentValue = num === '.' ? '0.' : num;
                    shouldResetDisplay = false;
                } else {
                    if (num === '.') {
                        if (!currentValue.includes('.')) {
                            currentValue += num;
                        }
                    } else {
                        currentValue = currentValue === '0' ? num : currentValue + num;
                    }
                }

                display.value = currentValue;
            });
        });

        document.querySelectorAll('.btn-op').forEach(btn => {
            btn.addEventListener('click', function() {
                const newOp = this.textContent;

                if (operator !== null && !shouldResetDisplay) {
                    calculate();
                }

                previousValue = currentValue;
                operator = newOp;
                shouldResetDisplay = true;
            });
        });

        document.querySelector('.btn-equal').addEventListener('click', function() {
            if (operator !== null) {
                calculate();
            }
        });

        document.querySelector('.btn-clear').addEventListener('click', function() {
            currentValue = '0';
            previousValue = '';
            operator = null;
            shouldResetDisplay = false;
            display.value = '0';
        });

        function calculate() {
            const prev = parseFloat(previousValue);
            const current = parseFloat(currentValue);
            let result;

            switch(operator) {
                case '+':
                    result = prev + current;
                    break;
                case '-':
                    result = prev - current;
                    break;
                case '*':
                    result = prev * current;
                    break;
                case '/':
                    result = current !== 0 ? prev / current : 0;
                    break;
                default:
                    return;
            }

            currentValue = result.toString();
            operator = null;
            previousValue = '';
            shouldResetDisplay = true;
            display.value = currentValue;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@functions_framework.http
def main(request):
    with app.app_context():
        return app.full_dispatch_request()
