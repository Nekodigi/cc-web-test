# 画像認識アプリ (Streamlit + Claude Vision)

シンプルな画像認識アプリケーションです。Claude の Vision API を使用して、アップロードされた画像を分析します。

## 実行方法

### Docker で実行（推奨）
```bash
docker build -t my-app . && docker run -p 8080:8080 my-app
```

ブラウザで http://localhost:8080 にアクセスしてください。

### ローカルで実行
```bash
pip install -r requirements.txt
streamlit run app.py --server.port=8080
```

## 機能

- 🖼️ 画像のアップロード（JPG, PNG, GIF, WebP）
- 🤖 Claude Vision API による画像認識
- 📝 詳細な分析結果の表示

## 環境変数

以下の環境変数が必要です:

- `OPENAI_API_KEY`: Claude API キー（自動的に検出されます）

## ファイル構成

```
.
├── app.py                    # メインアプリケーション
├── requirements.txt          # Python 依存関係
├── Dockerfile               # Docker イメージ定義
├── .env                     # 環境変数（開発用）
├── .streamlit/
│   └── config.toml         # Streamlit 設定
└── README.md               # このファイル
```

## 技術スタック

- **Streamlit**: Web UI フレームワーク
- **Claude API**: 画像認識エンジン
- **Pillow**: 画像処理
- **Docker**: コンテナ化

## ブラウザでのアクセス

Docker で実行した場合:
```
http://localhost:8080
```

ローカル実行の場合:
```
http://localhost:8501 (デフォルトポート)
http://localhost:8080 (--server.port=8080 指定時)
```
