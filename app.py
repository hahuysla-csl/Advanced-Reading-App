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
    st.markdown("1. Nhập văn bản\n2. Nhấn Generate\n3. Copy prompt bên dưới\n4. Dán vào Gemini")
    level = st.selectbox("Level", ["B2", "C1", "C2"], index=1)

text_content = st.text_area("📝 Dán văn bản gốc vào đây", height=300)

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

    st.success("✅ Prompt đã sẵn sàng!")

    st.subheader("📋 Prompt (Copy từ đây):")
    st.code(prompt, language=None)

    st.info("💡 **Cách copy nhanh:**\n1. Click vào hộp code xám bên trên\n2. Nhấn Ctrl + A (chọn hết)\n3. Nhấn Ctrl + C (copy)\n4. Dán vào Gemini")

    if 'lessons' not in st.session_state:
        st.session_state.lessons = []
    st.session_state.lessons.append({
        "title": f"Lesson - {datetime.now().strftime('%d/%m %H:%M')}",
        "prompt": prompt
    })

st.caption("Mr. Khánh . SHGS - 2026")