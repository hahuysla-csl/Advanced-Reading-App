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
    st.markdown("1. Nhập material\n2. Fetch URL\n3. Generate Prompt")
    level = st.selectbox("Level", ["B2", "C1", "C2"], index=1)

tab1, tab2 = st.tabs(["Tạo Prompt", "My Lessons"])

with tab1:
    st.header("Nhập Authentic Material")
    input_method = st.radio("Cách nhập", ["Paste Text", "URL", "Upload File"], horizontal=True)
    text_content = st.session_state.get("text_content", "")

    if input_method == "Paste Text":
        text_content = st.text_area("Dán văn bản gốc", value=text_content, height=400, key="paste")
    elif input_method == "URL":
        url = st.text_input("Nhập URL bài báo")
        if st.button("📥 Fetch Content") and url:
            try:
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Xóa các phần thừa
                for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "button", "img"]):
                    tag.decompose()
                
                # Tìm nội dung chính
                article = (soup.find('article') or 
                          soup.find('main') or 
                          soup.find('div', {'class': lambda x: x and any(word in x.lower() for word in ['article', 'content', 'post', 'story', 'body'])}))
                
                if article:
                    text_content = article.get_text(separator='\n', strip=True)
                else:
                    text_content = soup.get_text(separator='\n', strip=True)
                
                # Làm sạch
                lines = [line.strip() for line in text_content.split('\n') if line.strip() and len(line.strip()) > 20]
                text_content = '\n\n'.join(lines[:50])  # Giới hạn để tránh quá dài
                
                st.session_state.text_content = text_content
                st.success("✅ Đã lấy nội dung!")
                st.text_area("Nội dung đã lấy (có thể chỉnh)", text_content, height=300, key="preview")
            except Exception as e:
                st.error(f"Lỗi: {e}")
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
                st.session_state.text_content = text_content
                st.success("✅ File processed!")
            except Exception as e:
                st.error(f"Lỗi: {e}")

    if text_content and st.button("🚀 Generate Full Prompt for Gemini", type="primary"):
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

with tab2:
    st.header("My Lessons")
    for lesson in st.session_state.get('lessons', []):
        with st.expander(lesson["title"]):
            st.text_area("Prompt:", lesson["prompt"], height=300)

st.caption("Mr. Khánh . SHGS - 2026")