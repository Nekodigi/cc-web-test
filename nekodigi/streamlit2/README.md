# 画像認識アプリ（Streamlit + Cloud Run）

OpenAI Vision APIを使用した画像認識アプリケーション。Streamlitで構築され、Google Cloud Runでホストできます。

## 機能

- **画像アップロード**: JPG、PNG、GIF、WebP形式に対応
- **AIによる画像認識**: OpenAI GPT-4 Visionを使用した高精度な画像分析
- **複数の分析オプション**:
  - 画像の内容説明
  - テキスト抽出
  - 色の特徴分析
  - オブジェクトの検出
  - カスタムプロンプト対応

- **Firebaseデータベース統合**: 認識結果をクラウドデータベースに保存
- **環境変数対応**: APIキーを安全に管理

## 必要な環境変数

```bash
OPENAI_API_KEY      # OpenAI APIキー（GPT-4 Vision対応）
DEVELOPER_ID        # Firebase内のディレクトリID
APP_ID              # アプリケーションID
```

## ローカル実行

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

```bash
export OPENAI_API_KEY="your-openai-api-key"
export DEVELOPER_ID="your-developer-id"
export APP_ID="your-app-id"
```

### 3. Streamlitアプリの起動

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` にアクセスしてください。

## Cloud Runへのデプロイ

詳細は [DEPLOYMENT.md](./DEPLOYMENT.md) を参照してください。

### 簡単デプロイコマンド

```bash
PROJECT_ID=your-project-id
IMAGE_NAME=image-recognition-app

# ビルド
docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME .

# プッシュ
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME

# デプロイ
gcloud run deploy image-recognition-app \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 2 \
  --timeout 3600 \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY,DEVELOPER_ID=$DEVELOPER_ID,APP_ID=$APP_ID
```

## アーキテクチャ

```
┌─────────────────┐
│  Streamlit UI   │
│   (Web App)     │
└────────┬────────┘
         │
    ┌────▼─────┐
    │  app.py   │
    └────┬──────┘
         │
    ┌────▼────────────────┐
    │  OpenAI Vision API   │
    │   (GPT-4 Vision)     │
    └─────────────────────┘
         │
    ┌────▼──────────────────┐
    │  Firebase Realtime DB │
    │ (Results Storage)     │
    └───────────────────────┘
```

## ファイル構成

```
.
├── app.py                    # メインアプリケーション
├── requirements.txt          # Python依存関係
├── Dockerfile               # Cloud Run用コンテナ構成
├── .dockerignore           # Docker無視ファイル
├── .streamlit/config.toml   # Streamlit設定
├── README.md               # このファイル
└── DEPLOYMENT.md           # デプロイメントガイド
```

## Cloud Run対応の特徴

- ✅ **ポート8080**: Cloud Run標準ポートで自動起動
- ✅ **ステートレス設計**: 複数インスタンスで動作可能
- ✅ **ヘルスチェック対応**: 自動リスタート機能対応
- ✅ **軽量イメージ**: 最新ライブラリで最適化
- ✅ **環境変数管理**: `OPENAI_API_KEY`など安全に統合

## Firebase接続情報

データベースパス:
```
pracClass/{DEVELOPER_ID}/apps/{APP_ID}/results/
```

Web SDK apiKey:
```
AIzaSyChB7eBjMaX_lRpfIgUxQDi39Qh82R4oyQ
```

Database URL:
```
https://sandbox-35d1d-default-rtdb.firebaseio.com
```

## トラブルシューティング

### APIキーエラー
- 環境変数が正しく設定されていることを確認
- `echo $OPENAI_API_KEY` で確認可能

### Firebase接続エラー
- Developer ID と App ID が設定されていることを確認
- Firebase Realtime DBのセキュリティルール設定を確認

### メモリ不足
- Cloud Runでメモリを2GB以上に設定してください
- 複数の同時リクエストを避ける

## ライセンス

MIT

## サポート

問題が発生した場合は、以下を確認してください：
1. 環境変数が正しく設定されているか
2. OpenAI APIキーが有効か
3. Firebase接続情報が正しいか
4. Cloud Runのリソースが十分か
