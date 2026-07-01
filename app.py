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

level = st.selectbox("Chọn Level", ["B2", "C1", "C2"], index=1, key="level")

st.header("Nhập Authentic Material")
method = st.radio("Chọn cách nhập", ["Paste Text", "URL", "Upload File"], horizontal=True)

text_content = st.session_state.get("text_content", "")

if method == "Paste Text":
    text_content = st.text_area("Dán văn bản gốc", value=text_content, height=400, key="paste_input")
elif method == "URL":
    url = st.text_input("Nhập URL bài báo", key="url_input")
    if st.button("📥 Fetch Content") and url:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, 'html.parser')
            for script in soup(["script", "style"]): script.decompose()
            text_content = soup.get_text(separator='\n', strip=True)
            st.session_state.text_content = text_content
            st.success("✅ Đã lấy nội dung thành công!")
        except:
            st.error("Lỗi khi lấy URL")
elif method == "Upload File":
    uploaded = st.file_uploader("Upload PDF, DOCX, TXT", type=["pdf","docx","txt"], key="file_input")
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
            st.session_state.text_content = text_content
            st.success("✅ File processed!")
        except Exception as e:
            st.error(str(e))

# Nút Generate luôn hiển thị nếu có nội dung
if text_content:
    if st.button("🚀 Generate Full Prompt for Gemini", type="primary", use_container_width=True):
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

        st.subheader("📋 Prompt")
        st.code(prompt, language=None)

        st.info("**Cách copy:** Click vào hộp code xám → Ctrl + A → Ctrl + C")

        if 'lessons' not in st.session_state:
            st.session_state.lessons = []
        st.session_state.lessons.append({
            "title": f"Full Lesson - {datetime.now().strftime('%d/%m %H:%M')}",
            "prompt": prompt,
            "level": level
        })
else:
    st.info("Vui lòng nhập nội dung trước khi Generate.")

st.caption("Mr. Khánh . SHGS - 2026")