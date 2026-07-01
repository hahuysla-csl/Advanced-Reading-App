import streamlit as st
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
    st.markdown("1. Chọn cách nhập\n2. Nhập nội dung\n3. Nhấn Generate\n4. Copy prompt")
    level = st.selectbox("Level", ["B2", "C1", "C2"], index=1)

text_content = ""

col1, col2 = st.columns(2)
with col1:
    method = st.radio("Cách nhập", ["Paste Text", "URL", "Upload File"])

if method == "Paste Text":
    text_content = st.text_area("Dán văn bản gốc vào đây", height=400)
elif method == "URL":
    url = st.text_input("Nhập URL bài báo")
    if st.button("Fetch Content") and url:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, 'html.parser')
            for script in soup(["script", "style"]): script.decompose()
            text_content = soup.get_text(separator='\n', strip=True)
            st.success("✅ Đã lấy nội dung!")
        except:
            st.error("Lỗi URL")
elif method == "Upload File":
    uploaded = st.file_uploader("Upload file", type=["pdf","docx","txt"])
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

if text_content and st.button("🚀 Generate Full Prompt", type="primary"):
    prompt = f"""Task: Create a complete, professional advanced reading lesson.

Level: {level} students

Original Text:
{text_content}

Include ALL the following sections:
1. Text Analysis (CEFR level, Summary 150-200 words, Key words/phrases)
2. Vocabulary in Context (10-15 items: word formation, synonyms, collocations, guessing meaning, AWL)
3. Reading Comprehension (8 MCQ, 5 T/F/Not Given, 5 Short Answer)
4. Inference & Critical Thinking (6 questions)
5. Grammar Focus (advanced structures from the text)
6. Cloze test (10 gaps)
7. Matching Headings / Information matching
8. A Complete Lesson Plan with Pre-reading, While-reading, Post-reading activities
9. Suggested simplified version for lower level: Tasks and Questions

Output in clean professional Markdown with clear headings, numbered questions, and answer key if appropriate."""

    st.success("✅ Prompt đã được tạo!")

    st.subheader("📋 Prompt - Copy từ đây")
    st.code(prompt, language=None)

    st.info("**Cách copy:** Click vào hộp code xám → Ctrl + A → Ctrl + C")

if 'lessons' not in st.session_state:
    st.session_state.lessons = []
if text_content and st.button("💾 Save this lesson"):
    st.session_state.lessons.append({
        "title": f"Lesson - {datetime.now().strftime('%d/%m %H:%M')}",
        "prompt": prompt if 'prompt' in locals() else ""
    })

st.caption("Mr. Khánh . SHGS - 2026")