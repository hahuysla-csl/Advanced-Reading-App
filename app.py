import streamlit as st
import docx
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pymupdf
from PIL import Image

st.set_page_config(
    page_title="Mr. Khánh . SHGS - 2026",
    layout="wide",
    page_icon="📖",
    initial_sidebar_state="expanded"
)

# Theme Navy + Gold
st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    h1 {color: #0f172a; font-weight: bold;}
    .stButton>button {
        background-color: #0f172a;
        color: #d4af37;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header với Logo
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
    st.header("🎯 Hướng dẫn sử dụng")
    st.markdown("""
    1. Nhập văn bản / URL / File  
    2. Chọn loại bài tập  
    3. Nhấn Generate Prompt  
    4. Copy prompt → Dán vào Gemini/ChatGPT  
    5. Dán kết quả vào Save Result
    """)
    level = st.selectbox("📊 Target CEFR Level", ["B2", "C1", "C2"], index=1)

tab1, tab2, tab3 = st.tabs(["✍️ Tạo Prompt", "📚 My Lessons", "💾 Export"])

with tab1:
    st.header("Nhập Authentic Material")
    input_method = st.radio("Cách nhập", ["Paste Text", "URL", "Upload File"], horizontal=True)
    text_content = ""
    
    if input_method == "Paste Text":
        text_content = st.text_area("Dán văn bản vào đây", height=300)
    elif input_method == "URL":
        url = st.text_input("Nhập URL bài báo")
        if st.button("📥 Fetch Content") and url:
            with st.spinner("Đang tải..."):
                try:
                    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                    soup = BeautifulSoup(r.text, 'html.parser')
                    for script in soup(["script", "style"]): script.decompose()
                    text_content = soup.get_text(separator='\n', strip=True)
                    st.success("✅ Đã lấy nội dung!")
                except:
                    st.error("Lỗi khi lấy URL")
    elif input_method == "Upload File":
        uploaded = st.file_uploader("Upload PDF, DOCX, TXT", type=["pdf","docx","txt"])
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
                st.success("✅ File processed!")
            except Exception as e:
                st.error(str(e))

    prompt_type = st.selectbox("🎯 Loại bài tập", [
        "Full Lesson Package (Toàn diện)",
        "Vocabulary Focus Only",
        "Reading Comprehension Only",
        "Grammar & Inference Only",
        "Cloze & Summary Only"
    ])

    if text_content and st.button("🚀 Generate Prompt", type="primary"):
        prompt = f"""You are an expert Advanced English teacher for {level} students.

Original Text:
{text_content}

Create a complete advanced reading lesson package with summary, vocabulary, comprehension, grammar, and activities. Use professional Markdown."""

        st.success("✅ Prompt ready!")
        st.text_area("Copy prompt này:", prompt, height=400)

        if 'lessons' not in st.session_state:
            st.session_state.lessons = []
        st.session_state.lessons.append({
            "title": f"{prompt_type[:25]}... - {datetime.now().strftime('%d/%m %H:%M')}",
            "prompt": prompt,
            "level": level
        })

with tab2:
    st.header("📚 My Lessons")
    for i, lesson in enumerate(st.session_state.get('lessons', [])):
        with st.expander(lesson["title"]):
            result = st.text_area("Dán kết quả AI sinh ra:", key=f"res_{i}")
            if st.button("💾 Save Result", key=f"save_{i}"):
                lesson["result"] = result
                st.success("✅ Đã lưu!")

with tab3:
    st.header("💾 Export")
    st.info("Kết quả được lưu tại tab My Lessons.")

st.caption("Mr. Khánh . SHGS - 2026 • Advanced Reading Tool")