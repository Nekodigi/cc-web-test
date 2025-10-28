import functions_framework
from flask import Flask, render_template

app = Flask(__name__, template_folder='.', static_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@functions_framework.http
def main(request):
    return app(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
