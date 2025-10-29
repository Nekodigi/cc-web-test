import streamlit as st
import os
from PIL import Image
import io
import json
from datetime import datetime
import firebase_admin
from firebase_admin import db
from openai import OpenAI
import base64

# ページ設定
st.set_page_config(
    page_title="画像認識アプリ",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 環境変数の読み込み
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEVELOPER_ID = os.getenv("DEVELOPER_ID")
APP_ID = os.getenv("APP_ID")

# Firebase初期化
@st.cache_resource
def initialize_firebase():
    try:
        if not firebase_admin._apps:
            firebase_admin.initialize_app(options={
                "databaseURL": "https://sandbox-35d1d-default-rtdb.firebaseio.com"
            })
    except Exception as e:
        st.warning(f"Firebase初期化: {e}")

initialize_firebase()

# OpenAI クライアント初期化
@st.cache_resource
def get_openai_client():
    if not OPENAI_API_KEY:
        st.error("OPENAI_API_KEY が設定されていません")
        st.stop()
    return OpenAI(api_key=OPENAI_API_KEY)

client = get_openai_client()

# Firebaseに結果を保存
def save_to_firebase(image_name: str, analysis_result: dict):
    try:
        if not DEVELOPER_ID or not APP_ID:
            st.warning("DEVELOPER_ID または APP_ID が設定されていません")
            return False

        ref_path = f"pracClass/{DEVELOPER_ID}/apps/{APP_ID}/results/{datetime.now().isoformat()}"
        db.reference(ref_path).set({
            "image_name": image_name,
            "analysis": analysis_result,
            "timestamp": datetime.now().isoformat()
        })
        return True
    except Exception as e:
        st.warning(f"Firebase保存エラー: {e}")
        return False

# 画像をBase64エンコード
def encode_image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

# Vision APIで画像認識を実行
def analyze_image(image: Image.Image, prompt: str) -> dict:
    try:
        # 画像をBase64エンコード
        image_data = encode_image_to_base64(image)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1024
        )

        return {
            "success": True,
            "analysis": response.choices[0].message.content,
            "model": "gpt-4o"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis": None
        }

# UIレイアウト
st.title("🖼️ 画像認識アプリ")
st.markdown("画像をアップロードしてOpenAI Vision APIで認識させます")

# サイドバー設定
with st.sidebar:
    st.header("⚙️ 設定")

    # API キー表示
    if OPENAI_API_KEY:
        st.success("✓ OpenAI API キー: 設定済み")
    else:
        st.error("✗ OpenAI API キー: 未設定")

    if DEVELOPER_ID and APP_ID:
        st.success(f"✓ Developer ID: {DEVELOPER_ID[:10]}...")
        st.success(f"✓ App ID: {APP_ID[:10]}...")
    else:
        st.warning("Developer ID または App ID が未設定です")

    # プリセット質問
    st.subheader("📝 プリセット質問")
    preset = st.radio(
        "質問を選択:",
        [
            "カスタム",
            "画像に何が写っているか説明してください",
            "この画像からテキストを抽出してください",
            "この画像の色の特徴を説明してください",
            "この画像に含まれるオブジェクトをリストアップしてください"
        ]
    )

# メインコンテンツ
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 アップロード")

    uploaded_file = st.file_uploader(
        "画像をアップロード (JPG, PNG, GIF, WebP)",
        type=["jpg", "jpeg", "png", "gif", "webp"],
        help="認識したい画像を選択してください"
    )

    if uploaded_file is not None:
        # 画像を表示
        image = Image.open(uploaded_file)
        st.image(image, caption="アップロードされた画像", use_column_width=True)

        # 画像情報
        st.info(f"**ファイル名:** {uploaded_file.name}\n**サイズ:** {uploaded_file.size / 1024:.1f} KB\n**寸法:** {image.size}")

with col2:
    st.subheader("⚙️ 分析設定")

    if preset == "カスタム":
        user_prompt = st.text_area(
            "質問を入力:",
            value="この画像について説明してください",
            height=100,
            help="画像に対する質問を自由に入力してください"
        )
    else:
        user_prompt = preset
        st.text_area(
            "質問 (プリセット):",
            value=preset,
            height=100,
            disabled=True
        )

# 分析実行
if st.button("🚀 分析を実行", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.error("❌ 画像をアップロードしてください")
    elif not OPENAI_API_KEY:
        st.error("❌ OPENAI_API_KEY が設定されていません")
    elif user_prompt.strip() == "":
        st.error("❌ 質問を入力してください")
    else:
        with st.spinner("🔄 分析中..."):
            image = Image.open(uploaded_file)
            result = analyze_image(image, user_prompt)

        if result["success"]:
            st.success("✓ 分析完了")

            # 結果表示
            st.subheader("📊 分析結果")
            st.markdown(result["analysis"])

            # Firebaseに保存
            if st.button("💾 結果をFirebaseに保存"):
                if save_to_firebase(uploaded_file.name, {
                    "prompt": user_prompt,
                    "analysis": result["analysis"],
                    "model": result["model"]
                }):
                    st.success("✓ Firebaseに保存しました")
                else:
                    st.warning("⚠️ Firebaseへの保存に失敗しました")
        else:
            st.error(f"❌ 分析エラー: {result['error']}")

# フッター
st.markdown("---")
st.markdown("""
### ℹ️ 使用方法
1. 画像をアップロード
2. 質問を選択 (またはカスタム入力)
3. 「分析を実行」をクリック
4. 結果が表示されます

### 🔧 技術情報
- **フレームワーク:** Streamlit
- **Vision API:** OpenAI GPT-4 Vision
- **データベース:** Firebase Realtime Database
- **デプロイ:** Cloud Run
""")
