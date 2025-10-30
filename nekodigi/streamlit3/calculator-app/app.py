import streamlit as st

st.set_page_config(page_title="Calculator", layout="centered")

st.title("Calculator")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("7", use_container_width=True, key="7"):
        st.session_state.display = st.session_state.get("display", "") + "7"
    if st.button("4", use_container_width=True, key="4"):
        st.session_state.display = st.session_state.get("display", "") + "4"
    if st.button("1", use_container_width=True, key="1"):
        st.session_state.display = st.session_state.get("display", "") + "1"
    if st.button("0", use_container_width=True, key="0"):
        st.session_state.display = st.session_state.get("display", "") + "0"

with col2:
    if st.button("8", use_container_width=True, key="8"):
        st.session_state.display = st.session_state.get("display", "") + "8"
    if st.button("5", use_container_width=True, key="5"):
        st.session_state.display = st.session_state.get("display", "") + "5"
    if st.button("2", use_container_width=True, key="2"):
        st.session_state.display = st.session_state.get("display", "") + "2"
    if st.button(".", use_container_width=True, key="."):
        st.session_state.display = st.session_state.get("display", "") + "."

with col3:
    if st.button("9", use_container_width=True, key="9"):
        st.session_state.display = st.session_state.get("display", "") + "9"
    if st.button("6", use_container_width=True, key="6"):
        st.session_state.display = st.session_state.get("display", "") + "6"
    if st.button("3", use_container_width=True, key="3"):
        st.session_state.display = st.session_state.get("display", "") + "3"
    if st.button("=", use_container_width=True, key="equals"):
        try:
            result = eval(st.session_state.get("display", "0"))
            st.session_state.display = str(result)
        except:
            st.session_state.display = "Error"

with col4:
    if st.button("+", use_container_width=True, key="+"):
        st.session_state.display = st.session_state.get("display", "") + "+"
    if st.button("-", use_container_width=True, key="-"):
        st.session_state.display = st.session_state.get("display", "") + "-"
    if st.button("*", use_container_width=True, key="*"):
        st.session_state.display = st.session_state.get("display", "") + "*"
    if st.button("/", use_container_width=True, key="/"):
        st.session_state.display = st.session_state.get("display", "") + "/"

if st.button("Clear", use_container_width=True):
    st.session_state.display = ""

st.text_input("Display", value=st.session_state.get("display", ""), disabled=True, key="display_input")
