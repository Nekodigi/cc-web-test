import streamlit as st
import os
from PIL import Image
import io
import base64
import requests

st.set_page_config(layout="centered", page_title="Image Recognition")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not set")
    st.stop()

st.title("画像認識")

uploaded_file = st.file_uploader("画像をアップロード", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

    if st.button("認識"):
        with st.spinner("処理中..."):
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            img_base64 = base64.b64encode(buffer.getvalue()).decode()

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "この画像に何が写っていますか？日本語で簡潔に説明してください。"},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                        ]
                    }
                ]
            }

            try:
                response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                result = response.json()
                description = result["choices"][0]["message"]["content"]
                st.success(description)
            except Exception as e:
                st.error(f"エラー: {str(e)}")
