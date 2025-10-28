import functions_framework
from flask import Flask, render_template, request, jsonify
import os
import openai

app = Flask(__name__, template_folder='.', static_folder='.')

openai.api_key = os.environ.get("OPENAI_API_KEY")
DEVELOPER_ID = os.environ.get("DEVELOPER_ID")
APP_ID = os.environ.get("APP_ID")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "Message is required"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        result = response.choices[0].message.content
        return jsonify({"response": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@functions_framework.http
def main(request):
    with app.app_context():
        return app(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
