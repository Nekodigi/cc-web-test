import streamlit as st

st.set_page_config(page_title="電卓", layout="centered")
st.title("簡単電卓")

col1, col2 = st.columns(2)
with col1:
    num1 = st.number_input("数値1", value=0.0, format="%.2f")
with col2:
    num2 = st.number_input("数値2", value=0.0, format="%.2f")

operation = st.selectbox("演算", ["＋", "－", "×", "÷"])

if st.button("計算"):
    if operation == "＋":
        result = num1 + num2
    elif operation == "－":
        result = num1 - num2
    elif operation == "×":
        result = num1 * num2
    elif operation == "÷":
        result = num1 / num2 if num2 != 0 else None

    if result is not None:
        st.success(f"結果: {result}")
    else:
        st.error("ゼロで除算はできません")
