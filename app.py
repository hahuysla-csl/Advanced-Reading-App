import streamlit as st
import docx
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pymupdf
from PIL import Image

st.set_page_config(page_title="Mr. Khánh . SHGS - 2026", layout="wide", page_icon="📖")

# Theme
st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    h1 {color: #0f172a;}
    .stButton>button {background-color: #0f172a; color: #d4af37; border-radius: 8px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 5])
with col1:
    try:
        logo = Image.open("logo.png")
        st.image(logo, width=130)
    except:
        st.markdown("# 📖")
with col2:
    st.title("Mr. Khánh . SHGS - 2026")
    st.subheader("Advanced Reading Generator")

st.divider()

with st.sidebar:
    st.header("Hướng dẫn")
    st.markdown("1. Nhập material\n2. Generate Prompt\n3. Copy vào Gemini")
    level = st.selectbox("Level", ["B2", "C1", "C2"], index=1)

tab1, tab2, tab3 = st.tabs(["Tạo Prompt", "My Lessons", "Export"])

with tab1:
    st.header("Nhập Authentic Material")
    input_method = st.radio("Cách nhập", ["Paste Text", "URL", "Upload File"], horizontal=True)
    text_content = ""

    if input_method == "Paste Text":
        text_content = st.text_area("Dán văn bản gốc", height=350)
    elif input_method == "URL":
        url = st.text_input("Nhập URL")
        if st.button("Fetch Content") and url:
            try:
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(r.text, 'html.parser')
                for script in soup(["script", "style"]): script.decompose()
                text_content = soup.get_text(separator='\n', strip=True)
                st.success("✅ Fetched!")
            except:
                st.error("Lỗi URL")
    elif input_method == "Upload File":
        uploaded = st.file_uploader("Upload PDF/DOCX/TXT", type=["pdf","docx","txt"])
        if uploaded:
            try:
                if uploaded.type == "application/pdf":
                    doc = pymupdf.open(stream=uploaded.read(), filetype="pdf")
                    text_content = "".join(page.get_text() for page in doc)
                elif uploaded.type.endswith("wordprocessingml.document"):
                    doc = docx.Document(uploaded)
                    text_content = "\n".join(para.text for para in doc.paragraphs)
                else:
                    text_content = uploaded.getvalue().decode()
                st