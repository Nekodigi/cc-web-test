import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
import os

# Set up page config
st.set_page_config(
    page_title="Image Recognition App",
    page_icon="🖼️",
    layout="wide"
)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY environment variable is not set")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("🖼️ Image Recognition App")
st.write("Upload an image or take a photo to recognize its contents using AI")

# Create tabs for different input methods
tab1, tab2 = st.tabs(["Upload Image", "Camera"])

with tab1:
    st.subheader("Upload an Image")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png", "gif", "webp"],
        key="file_uploader"
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze Image", key="analyze_uploaded"):
            with st.spinner("Analyzing image..."):
                # Convert image to base64
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_base64 = base64.standard_b64encode(buffered.getvalue()).decode("utf-8")

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{img_base64}"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "Please analyze this image and describe what you see. Include details about objects, people, text, colors, and any other relevant information."
                                    }
                                ]
                            }
                        ],
                        max_tokens=1024
                    )

                    # Display results
                    st.subheader("Analysis Results")
                    st.write(response.choices[0].message.content)

                except Exception as e:
                    st.error(f"Error analyzing image: {str(e)}")

with tab2:
    st.subheader("Take a Photo")
    camera_image = st.camera_input("Take a picture")

    if camera_image:
        image = Image.open(camera_image)
        st.image(image, caption="Camera Image", use_column_width=True)

        if st.button("Analyze Image", key="analyze_camera"):
            with st.spinner("Analyzing image..."):
                # Convert image to base64
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_base64 = base64.standard_b64encode(buffered.getvalue()).decode("utf-8")

                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{img_base64}"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": "Please analyze this image and describe what you see. Include details about objects, people, text, colors, and any other relevant information."
                                    }
                                ]
                            }
                        ],
                        max_tokens=1024
                    )

                    # Display results
                    st.subheader("Analysis Results")
                    st.write(response.choices[0].message.content)

                except Exception as e:
                    st.error(f"Error analyzing image: {str(e)}")

# Footer
st.divider()
st.write("💡 Tips:")
st.write("- Supported formats: JPG, JPEG, PNG, GIF, WEBP")
st.write("- For best results, use clear, well-lit images")
st.write("- The AI will describe objects, text, people, and other visual elements")
