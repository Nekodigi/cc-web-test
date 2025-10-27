import streamlit as st
import os
from streamlit.web import cli as stcli
import sys

def calculator_app():
    """電卓アプリケーション"""

    # ページ設定
    st.set_page_config(
        page_title="電卓",
        page_icon="🧮",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Tailwind CSSの読み込み
    st.markdown("""
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {
                margin: 0;
                padding: 0;
            }
            .stApp {
                max-width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    # セッションステート初期化
    if 'display' not in st.session_state:
        st.session_state.display = '0'
    if 'previous_value' not in st.session_state:
        st.session_state.previous_value = None
    if 'operation' not in st.session_state:
        st.session_state.operation = None
    if 'new_number' not in st.session_state:
        st.session_state.new_number = True

    def clear_display():
        st.session_state.display = '0'
        st.session_state.previous_value = None
        st.session_state.operation = None
        st.session_state.new_number = True

    def append_digit(digit):
        if st.session_state.new_number:
            st.session_state.display = str(digit)
            st.session_state.new_number = False
        else:
            if st.session_state.display == '0':
                st.session_state.display = str(digit)
            else:
                st.session_state.display += str(digit)

    def append_decimal():
        if st.session_state.new_number:
            st.session_state.display = '0.'
            st.session_state.new_number = False
        elif '.' not in st.session_state.display:
            st.session_state.display += '.'

    def set_operation(op):
        if st.session_state.operation is not None and not st.session_state.new_number:
            calculate()
        st.session_state.previous_value = float(st.session_state.display)
        st.session_state.operation = op
        st.session_state.new_number = True

    def calculate():
        if st.session_state.operation is None or st.session_state.previous_value is None:
            return

        try:
            current_value = float(st.session_state.display)
            result = None

            if st.session_state.operation == '+':
                result = st.session_state.previous_value + current_value
            elif st.session_state.operation == '-':
                result = st.session_state.previous_value - current_value
            elif st.session_state.operation == '×':
                result = st.session_state.previous_value * current_value
            elif st.session_state.operation == '÷':
                if current_value != 0:
                    result = st.session_state.previous_value / current_value
                else:
                    st.session_state.display = 'エラー'
                    st.session_state.new_number = True
                    return

            if result is not None:
                # 整数の場合は小数点を付けない
                if result == int(result):
                    st.session_state.display = str(int(result))
                else:
                    st.session_state.display = str(result)

            st.session_state.operation = None
            st.session_state.previous_value = None
            st.session_state.new_number = True
        except Exception as e:
            st.session_state.display = 'エラー'
            st.session_state.new_number = True

    def toggle_sign():
        try:
            value = float(st.session_state.display)
            st.session_state.display = str(-value if value != int(value) else int(-value))
        except:
            pass

    def get_percentage():
        try:
            value = float(st.session_state.display)
            st.session_state.display = str(value / 100)
            st.session_state.new_number = True
        except:
            pass

    # UIレイアウト
    st.markdown("""
        <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <div class="w-full max-w-sm px-4">
    """, unsafe_allow_html=True)

    # ディスプレイ
    st.markdown(f"""
        <div class="bg-white rounded-lg shadow-xl overflow-hidden">
            <div class="bg-gradient-to-r from-indigo-600 to-blue-600 p-6">
                <div class="text-right text-white text-5xl font-bold font-mono break-words" style="word-break: break-all;">
                    {st.session_state.display}
                </div>
            </div>
    """, unsafe_allow_html=True)

    # ボタングリッド
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button('C', key='c', use_container_width=True):
            clear_display()

    with col2:
        if st.button('±', key='sign', use_container_width=True):
            toggle_sign()

    with col3:
        if st.button('%', key='percent', use_container_width=True):
            get_percentage()

    with col4:
        if st.button('÷', key='div', use_container_width=True):
            set_operation('÷')

    # 数字行1
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button('7', key='7', use_container_width=True):
            append_digit(7)

    with col2:
        if st.button('8', key='8', use_container_width=True):
            append_digit(8)

    with col3:
        if st.button('9', key='9', use_container_width=True):
            append_digit(9)

    with col4:
        if st.button('×', key='mul', use_container_width=True):
            set_operation('×')

    # 数字行2
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button('4', key='4', use_container_width=True):
            append_digit(4)

    with col2:
        if st.button('5', key='5', use_container_width=True):
            append_digit(5)

    with col3:
        if st.button('6', key='6', use_container_width=True):
            append_digit(6)

    with col4:
        if st.button('-', key='sub', use_container_width=True):
            set_operation('-')

    # 数字行3
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button('1', key='1', use_container_width=True):
            append_digit(1)

    with col2:
        if st.button('2', key='2', use_container_width=True):
            append_digit(2)

    with col3:
        if st.button('3', key='3', use_container_width=True):
            append_digit(3)

    with col4:
        if st.button('+', key='add', use_container_width=True):
            set_operation('+')

    # 数字行4
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button('0', key='0', use_container_width=True):
            append_digit(0)

    with col2:
        if st.button('.', key='dot', use_container_width=True):
            append_decimal()

    with col3:
        col3_1, col3_2 = st.columns(2)
        with col3_1:
            if st.button('', key='empty', use_container_width=True, disabled=True):
                pass
        with col3_2:
            if st.button('', key='empty2', use_container_width=True, disabled=True):
                pass

    with col4:
        if st.button('=', key='equals', use_container_width=True):
            calculate()

    st.markdown("""
            </div>
        </div>
        </div>
    """, unsafe_allow_html=True)


def main(request=None):
    """Cloud Functions のエントリーポイント (port=3000)"""
    # Streamlit アプリを起動
    sys.argv = [
        "streamlit",
        "run",
        __file__,
        "--server.port=3000",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]

    # アプリを実行
    calculator_app()


if __name__ == "__main__":
    # ローカル実行時
    if len(sys.argv) == 1:
        sys.argv = [
            "streamlit",
            "run",
            __file__,
            "--server.port=3000",
            "--server.address=0.0.0.0",
        ]
        sys.exit(stcli.main())
    else:
        # Streamlit から呼び出された場合
        calculator_app()
