import streamlit as st
import os
from openai import OpenAI
from PIL import Image
import io
import base64

# OpenAI APIクライアントの初期化
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ページ設定
st.set_page_config(
    page_title="画像認識アプリ",
    page_icon="🖼️",
    layout="centered"
)

st.title("🖼️ 画像認識アプリ")
st.markdown("画像をアップロードして、AIに認識させてみましょう")

# サイドバーで認識モードを選択
recognition_mode = st.sidebar.radio(
    "認識モード",
    ["画像の説明", "オブジェクト検出", "テキスト認識", "カスタム質問"]
)

# アップロードファイルの処理
uploaded_file = st.file_uploader("画像をアップロード", type=["jpg", "jpeg", "png", "gif", "webp"])

if uploaded_file:
    # 画像の表示
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    # 画像のプリビューサイズ（表示用）
    display_image = image.copy()
    display_image.thumbnail((200, 200))

    # 分析ボタン
    if st.button("🔍 画像を分析", key="analyze_button"):
        with st.spinner("分析中..."):
            try:
                # 画像をBase64エンコード
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

                # 認識モードに応じたプロンプトの設定
                prompts = {
                    "画像の説明": "この画像の詳細な説明をしてください。画像に何が写っているか、どんな状況かを説明してください。",
                    "オブジェクト検出": "この画像に含まれるすべてのオブジェクト（物体）を検出し、リストアップしてください。各オブジェクトについて簡潔に説明してください。",
                    "テキスト認識": "この画像に含まれるすべてのテキストを抽出して、そのまま転記してください。テキストが見つからない場合は、その旨を報告してください。",
                    "カスタム質問": "この画像について、何か特徴的なことはありますか？教えてください。"
                }

                prompt = prompts[recognition_mode]

                # GPT-4 Visionを使用して画像を分析
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
                                        "data": image_base64
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

                # 結果の表示
                st.success("分析完了!")
                st.markdown("### 📋 認識結果")
                st.markdown(response.content[0].text)

            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
else:
    st.info("📤 上にファイルをアップロードしてください")

# フッター
st.markdown("---")
st.markdown("✨ Powered by OpenAI GPT-4 Vision")
