import functions_framework
from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
DEVELOPER_ID = os.environ.get("DEVELOPER_ID")
APP_ID = os.environ.get("APP_ID")

# HTML コンテンツをキャッシュ
HTML_CONTENT = None

def load_html():
    global HTML_CONTENT
    if HTML_CONTENT is None:
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                HTML_CONTENT = f.read()
        except:
            HTML_CONTENT = ""
    return HTML_CONTENT

@app.route('/')
def index():
    return load_html()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "Message is required"}), 400

        response = openai_client.chat.completions.create(
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
    return app(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
