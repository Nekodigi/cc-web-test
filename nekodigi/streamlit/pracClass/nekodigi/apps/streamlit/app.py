import streamlit as st
import anthropic
from PIL import Image
import io
import base64
import os

# Streamlit設定
st.set_page_config(page_title="Image Recognition App", layout="centered")

st.title("🖼️ Image Recognition App")
st.write("画像をアップロードして、AI が内容を認識します")

# APIキーの確認
api_key = st.secrets.get("openai_api_key") or os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("APIキーが設定されていません")
    st.stop()

# 画像アップロード
uploaded_file = st.file_uploader("画像を選択してください", type=["jpg", "jpeg", "png", "gif", "webp"])

if uploaded_file is not None:
    # 画像表示
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロード画像", use_column_width=True)

    # 画像をBase64エンコード
    image_data = base64.standard_b64encode(uploaded_file.getvalue()).decode("utf-8")

    # 画像形式の判定
    ext = uploaded_file.name.lower().split('.')[-1]
    media_type_map = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    media_type = media_type_map.get(ext, 'image/jpeg')

    if st.button("🔍 画像を認識する"):
        with st.spinner("分析中..."):
            try:
                # Claude API を使用して画像認識
                client = anthropic.Anthropic(api_key=api_key)

                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": media_type,
                                        "data": image_data,
                                    },
                                },
                                {
                                    "type": "text",
                                    "text": "この画像について詳しく説明してください。画像に何が写っているか、どのような特徴があるか、背景は何か、など詳細に分析してください。"
                                }
                            ],
                        }
                    ],
                )

                # 結果表示
                st.success("✅ 認識完了")
                st.subheader("認識結果")
                st.write(message.content[0].text)

            except anthropic.APIError as e:
                st.error(f"API エラー: {str(e)}")
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

st.divider()
st.markdown("### 📋 使い方")
st.write("""
1. 画像ファイルをアップロード
2. 「画像を認識する」ボタンをクリック
3. AI による画像認識結果が表示されます
""")
