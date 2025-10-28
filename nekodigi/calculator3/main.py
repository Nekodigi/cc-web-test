from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

def main(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
