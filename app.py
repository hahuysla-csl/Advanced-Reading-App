import streamlit as st
import docx
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pymupdf
from PIL import Image

st.set_page_config(page_title="Mr. Khánh . SHGS - 2026", layout="wide", page_icon="📖")

st.title("Mr. Khánh . SHGS - 2026")
st.subheader("Advanced Reading Generator")

st.divider()

with st.sidebar:
    st.header("Hướng dẫn")
    st.markdown("1. Nhập URL\n2. Fetch Content\n3. Generate Prompt")
    level = st.selectbox("Level", ["B2", "C1", "C2"], index=1)

tab1, tab2 = st.tabs(["Tạo Prompt", "My Lessons"])

with tab1:
    st.header("Nhập Authentic Material")
    input_method = st.radio("Cách nhập", ["Paste Text", "URL", "Upload File"], horizontal=True)

    if 'text_content' not in st.session_state:
        st.session_state.text_content = ""

    if input_method == "Paste Text":
        st.session_state.text_content = st.text_area("Dán văn bản gốc", value=st.session_state.text_content, height=400, key="paste")
    elif input_method == "URL":
        url = st.text_input("Nhập URL bài báo")
        if st.button("📥 Fetch Content") and url:
            try:
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Xóa hoàn toàn các phần thừa
                for tag in soup(["script", "style", "nav", "header", "footer", "aside", "ad", "comment", "form", "button", "img"]):
                    tag.decompose