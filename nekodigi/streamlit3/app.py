import streamlit as st
import anthropic
import base64
from io import BytesIO
from PIL import Image
import os

st.set_page_config(layout="wide", page_title="Image Recognizer")
st.title("🖼️ Image Recognizer")

uploaded_file = st.file_uploader("画像をアップロード", type=["jpg", "jpeg", "png", "gif", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="アップロード画像", use_column_width=True)

    if st.button("認識開始"):
        with st.spinner("分析中..."):
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            image_data = base64.standard_b64encode(buffer.read()).decode("utf-8")

            client = anthropic.Anthropic(api_key=os.getenv("OPENAI_API_KEY"))

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
                                    "media_type": "image/png",
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": "この画像に何が写っているか、日本語で簡潔に説明してください。"
                            }
                        ],
                    }
                ],
            )

            with col2:
                st.subheader("認識結果")
                st.write(message.content[0].text)
