import functions_framework
import os
from openai import OpenAI
from PIL import Image
import io
import base64
import json
from flask import Request

# OpenAI APIクライアントの初期化
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def analyze_image(image_data_base64: str, recognition_mode: str) -> str:
    """画像をOpenAI APIで分析"""
    try:
        # 認識モードに応じたプロンプトの設定
        prompts = {
            "description": "この画像の詳細な説明をしてください。画像に何が写っているか、どんな状況かを説明してください。",
            "objects": "この画像に含まれるすべてのオブジェクト（物体）を検出し、リストアップしてください。各オブジェクトについて簡潔に説明してください。",
            "text": "この画像に含まれるすべてのテキストを抽出して、そのまま転記してください。テキストが見つからない場合は、その旨を報告してください。",
            "custom": "この画像について、何か特徴的なことはありますか？教えてください。"
        }

        prompt = prompts.get(recognition_mode, prompts["description"])

        # GPT-4o Visionを使用して画像を分析
        response = client.messages.create(
            model="gpt-4o",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )

        return response.content[0].text
    except Exception as e:
        raise Exception(f"分析エラー: {str(e)}")


@functions_framework.http
def main(request: Request):
    """HTTP Cloud Function entry point"""

    # CORSヘッダーの設定
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
        return ("", 204, headers)

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        # リクエストデータの取得
        if request.method == "GET":
            # HTMLUIを返す
            html_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖼️ 画像認識アプリ</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .form-group {
            margin-bottom: 25px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            color: #333;
            font-weight: 600;
            font-size: 1.05em;
        }
        select, input[type="file"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        select:focus, input[type="file"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .image-preview {
            margin-top: 15px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 8px;
            text-align: center;
            min-height: 200px;
            display: none;
        }
        .image-preview.active {
            display: block;
        }
        .image-preview img {
            max-width: 100%;
            max-height: 300px;
            border-radius: 8px;
        }
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 30px;
        }
        button {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-analyze {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-analyze:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        .btn-analyze:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .btn-clear {
            background: #f0f0f0;
            color: #333;
            border: 2px solid #ddd;
        }
        .btn-clear:hover {
            background: #e0e0e0;
        }
        .results {
            margin-top: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            display: none;
        }
        .results.active {
            display: block;
        }
        .results h3 {
            color: #333;
            margin-bottom: 15px;
        }
        .results p {
            color: #666;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            font-weight: 600;
        }
        .loading.active {
            display: block;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            display: none;
        }
        .error.active {
            display: block;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            color: #999;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ 画像認識アプリ</h1>
        <p class="subtitle">画像をアップロードして、AIに認識させてみましょう</p>

        <form id="imageForm">
            <div class="form-group">
                <label for="modeSelect">認識モード:</label>
                <select id="modeSelect">
                    <option value="description">画像の説明</option>
                    <option value="objects">オブジェクト検出</option>
                    <option value="text">テキスト認識</option>
                    <option value="custom">カスタム質問</option>
                </select>
            </div>

            <div class="form-group">
                <label for="imageInput">画像をアップロード:</label>
                <input type="file" id="imageInput" accept="image/jpeg,image/png,image/gif,image/webp" />
                <div class="image-preview" id="imagePreview">
                    <img id="previewImage" src="" alt="Preview" />
                </div>
            </div>

            <div class="button-group">
                <button type="button" class="btn-analyze" id="analyzeBtn" disabled>🔍 画像を分析</button>
                <button type="reset" class="btn-clear" id="clearBtn">🗑️ クリア</button>
            </div>

            <div class="loading" id="loading">
                <p>分析中...</p>
            </div>

            <div class="error" id="errorMsg"></div>

            <div class="results" id="results">
                <h3>📋 認識結果</h3>
                <p id="resultsText"></p>
            </div>
        </form>

        <div class="footer">
            <p>✨ Powered by OpenAI GPT-4 Vision</p>
        </div>
    </div>

    <script>
        const imageInput = document.getElementById('imageInput');
        const previewImage = document.getElementById('previewImage');
        const imagePreview = document.getElementById('imagePreview');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const clearBtn = document.getElementById('clearBtn');
        const modeSelect = document.getElementById('modeSelect');
        const loading = document.getElementById('loading');
        const errorMsg = document.getElementById('errorMsg');
        const results = document.getElementById('results');
        const resultsText = document.getElementById('resultsText');

        imageInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    previewImage.src = event.target.result;
                    imagePreview.classList.add('active');
                    analyzeBtn.disabled = false;
                };
                reader.readAsDataURL(file);
            }
        });

        clearBtn.addEventListener('click', () => {
            imageInput.value = '';
            imagePreview.classList.remove('active');
            analyzeBtn.disabled = true;
            results.classList.remove('active');
            errorMsg.classList.remove('active');
        });

        analyzeBtn.addEventListener('click', async () => {
            const file = imageInput.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = async (event) => {
                const base64Data = event.target.result.split(',')[1];

                try {
                    loading.classList.add('active');
                    errorMsg.classList.remove('active');
                    results.classList.remove('active');

                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            image: base64Data,
                            mode: modeSelect.value
                        })
                    });

                    const data = await response.json();
                    loading.classList.remove('active');

                    if (response.ok) {
                        resultsText.textContent = data.result;
                        results.classList.add('active');
                    } else {
                        throw new Error(data.error || 'エラーが発生しました');
                    }
                } catch (error) {
                    loading.classList.remove('active');
                    errorMsg.textContent = '❌ ' + error.message;
                    errorMsg.classList.add('active');
                }
            };
            reader.readAsDataURL(file);
        });
    </script>
</body>
</html>
            """
            return (html_content, 200, {"Content-Type": "text/html; charset=utf-8"})

        elif request.method == "POST":
            # JSONリクエストの処理
            data = request.get_json()

            if not data:
                return (json.dumps({"error": "リクエストボディが空です"}), 400, headers)

            image_base64 = data.get("image")
            mode = data.get("mode", "description")

            if not image_base64:
                return (json.dumps({"error": "画像データが必要です"}), 400, headers)

            # 画像を分析
            result = analyze_image(image_base64, mode)

            return (json.dumps({"result": result}, ensure_ascii=False), 200, headers)

        else:
            return (json.dumps({"error": "メソッドが許可されていません"}), 405, headers)

    except Exception as e:
        return (json.dumps({"error": str(e)}, ensure_ascii=False), 500, headers)
