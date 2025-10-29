#!/usr/bin/env python3
"""
Streamlit Image Recognition App
Simple image recognition application using OpenAI's Vision API
"""

import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import os

# Page configuration
st.set_page_config(
    page_title="🖼️ 画像認識アプリ",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
        .main { max-width: 1000px; }
        .stTitle { font-size: 2.5rem !important; }
        .result-box {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #667eea;
        }
        .image-container {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🖼️ 画像認識アプリ")
st.markdown("AIを使用して画像を分析します。複数の認識モードから選択できます。")

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    """Initialize OpenAI client with API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ OPENAI_API_KEY環境変数が設定されていません")
        st.stop()
    return OpenAI(api_key=api_key)

def analyze_image(image_data: Image.Image, recognition_mode: str, client: OpenAI) -> str:
    """
    Analyze image using OpenAI Vision API

    Args:
        image_data: PIL Image object
        recognition_mode: Type of analysis to perform
        client: OpenAI client instance

    Returns:
        Analysis result string
    """
    # Convert image to base64
    buffer = io.BytesIO()
    image_data.save(buffer, format="PNG")
    image_base64 = __import__('base64').b64encode(buffer.getvalue()).decode()

    # Define prompts for different recognition modes
    prompts = {
        "description": "この画像の詳細な説明をしてください。画像に何が写っているか、どんな状況かを説明してください。",
        "objects": "この画像に含まれるすべてのオブジェクト（物体）を検出し、リストアップしてください。各オブジェクトについて簡潔に説明してください。",
        "text": "この画像に含まれるすべてのテキストを抽出して、そのまま転記してください。テキストが見つからない場合は、その旨を報告してください。",
        "custom": "この画像について分析してください。特に興味深い特徴があれば教えてください。"
    }

    prompt = prompts.get(recognition_mode, prompts["description"])

    # Call OpenAI Vision API
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

    return response.content[0].text

def main():
    """Main application logic"""

    # Get OpenAI client
    client = get_openai_client()

    # Sidebar configuration
    st.sidebar.header("⚙️ 設定")

    recognition_mode = st.sidebar.selectbox(
        "認識モードを選択:",
        [
            ("画像の説明", "description"),
            ("オブジェクト検出", "objects"),
            ("テキスト認識", "text"),
            ("カスタム分析", "custom")
        ],
        format_func=lambda x: x[0]
    )
    recognition_mode = recognition_mode[1]

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📤 画像のアップロード")
        uploaded_file = st.file_uploader(
            "画像を選択してください",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            help="JPG, PNG, GIF, WebP形式に対応しています"
        )

        if uploaded_file is not None:
            # Display image preview
            image = Image.open(uploaded_file)
            st.image(image, caption="アップロードされた画像", use_column_width=True)

            # Image info
            st.info(f"📏 サイズ: {image.size[0]}×{image.size[1]} px | 形式: {image.format}")

    with col2:
        st.subheader("📋 分析結果")

        if uploaded_file is not None:
            if st.button("🔍 画像を分析", key="analyze_btn", use_container_width=True):
                try:
                    with st.spinner("分析中..."):
                        image = Image.open(uploaded_file)
                        result = analyze_image(image, recognition_mode, client)

                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.success("✅ 分析完了")
                    st.markdown(f"**認識モード:** {dict([('description', '画像の説明'), ('objects', 'オブジェクト検出'), ('text', 'テキスト認識'), ('custom', 'カスタム分析')])[recognition_mode]}")
                    st.markdown(f"\n{result}")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Download result as text
                    st.download_button(
                        label="💾 結果をダウンロード",
                        data=result,
                        file_name="analysis_result.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"❌ エラーが発生しました: {str(e)}")
        else:
            st.info("📤 左側から画像をアップロードしてください")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.9em;">
            ✨ Powered by OpenAI GPT-4 Vision | Streamlit
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
