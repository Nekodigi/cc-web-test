# Cloud Run デプロイガイド

## 前提条件
- Google Cloud SDK がインストールされていること
- プロジェクトが設定されていること
- 環境変数が設定可能な状態であること

## デプロイ手順

### 1. ローカルでテスト
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 2. イメージをビルド
```bash
# PROJECT_ID を自分のプロジェクトIDに置き換えてください
PROJECT_ID=your-project-id
IMAGE_NAME=image-recognition-app

docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME .
```

### 3. イメージを Artifact Registry にプッシュ
```bash
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME
```

### 4. Cloud Run にデプロイ
```bash
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

### 5. デプロイ確認
```bash
gcloud run services describe image-recognition-app --region us-central1
```

## 環境変数の設定

Cloud Run の UI から、または以下のコマンドで環境変数を設定できます：

```bash
gcloud run services update image-recognition-app \
  --region us-central1 \
  --update-env-vars OPENAI_API_KEY=$OPENAI_API_KEY,DEVELOPER_ID=$DEVELOPER_ID,APP_ID=$APP_ID
```

## リソース設定

推奨設定：
- **CPU:** 2
- **メモリ:** 1GB
- **タイムアウト:** 3600秒（1時間）
- **最大インスタンス数:** 100（必要に応じて調整）

## トラブルシューティング

### イメージが大きすぎる場合
```bash
# .dockerignore で不要なファイルを除外していることを確認
cat .dockerignore
```

### メモリ不足エラーが発生する場合
メモリを増やしてデプロイ：
```bash
gcloud run deploy image-recognition-app \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --memory 2Gi \
  --region us-central1
```

### ポート設定
- Streamlit は 8501 ポートで起動します
- Cloud Run は自動的にこのポートをマッピングします
- ヘルスチェックも自動で設定されます

## ローカル Docker での実行確認

```bash
docker build -t image-recognition-app .

# 環境変数を設定して実行
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e DEVELOPER_ID=$DEVELOPER_ID \
  -e APP_ID=$APP_ID \
  image-recognition-app
```

ブラウザで `http://localhost:8501` にアクセス。

## 注意点

1. **API キーの管理**
   - 環境変数経由で安全に渡します
   - コード内にハードコードしません

2. **Firebase接続**
   - `pracClass/{DEVELOPER_ID}/apps/{APP_ID}` にデータを保存
   - Firebaseルールで適切なアクセス制御を設定してください

3. **ファイアウォール**
   - Cloud Run は自動的にファイアウォールで保護されます
   - 必要に応じて認証を追加できます

4. **コスト**
   - 使用量に応じて課金されます
   - 無料枠内での使用を推奨
