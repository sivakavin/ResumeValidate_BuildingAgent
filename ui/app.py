
import streamlit as st
import tempfile
import os
# Add project root to sys.path for module imports
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from graph.resume_flow import ResumeFlow
from dotenv import load_dotenv


import docx2txt
from PyPDF2 import PdfReader
import io
from docx import Document
import re

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text
    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        text = docx2txt.process(tmp_path)
        os.unlink(tmp_path)
        return text
    else:
        return uploaded_file.read().decode("utf-8")

# Helper to highlight improvements (simple diff)
def highlight_changes(original, refined):
    orig_lines = set(original.splitlines())
    refined_lines = set(refined.splitlines())
    added = refined_lines - orig_lines
    highlighted = []
    for line in refined.splitlines():
        if line.strip() in added and line.strip():
            highlighted.append(f":green[**{line}**]")
        else:
            highlighted.append(line)
    return "\n".join(highlighted)

# Wrapper for processing resume
def process_resume(jd_text, resume_text):
    result = flow.run(jd_text, resume_text)
    supervisor_feedback = result["evaluation"].get("feedback", "No feedback.")
    refined_resume = result["resume"]
    return supervisor_feedback, refined_resume

# Helper to create DOCX for download
def create_docx(text):
    doc = Document()
    # Try to split and add headings for Skills, Experience, Education
    sections = {"Skills": [], "Experience": [], "Education": [], "Other": []}
    current = "Other"
    for line in text.splitlines():
        l = line.strip()
        if re.match(r"skills?[:]?", l, re.I):
            current = "Skills"
            continue
        elif re.match(r"experience[:]?", l, re.I):
            current = "Experience"
            continue
        elif re.match(r"education[:]?", l, re.I):
            current = "Education"
            continue
        if l:
            sections[current].append(l)
    # Add name/title if present
    lines = text.splitlines()
    if lines and lines[0].strip():
        doc.add_heading(lines[0].strip(), 0)
    # Add sections with headings
    for sec in ["Skills", "Experience", "Education", "Other"]:
        if sections[sec]:
            doc.add_heading(sec, level=1)
            for item in sections[sec]:
                doc.add_paragraph(item)
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
flow = ResumeFlow(groq_api_key)

st.set_page_config(page_title="Resume Multi-Agent", layout="wide")
st.title("Resume Multi-Agent Chat")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "refined_resume" not in st.session_state:
    st.session_state.refined_resume = None
if "original_resume" not in st.session_state:
    st.session_state.original_resume = None

st.markdown("""
Upload your resume and paste the job description. Click 'Analyze and Refine Resume' to get feedback and a tailored resume.
""")

uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
jd_text = st.text_area("Paste Job Description", height=200)



# Enhanced process_resume for multiple iterations and chat turns
def process_resume(jd_text, resume_text, max_loops=3):
    chat_turns = []
    current_resume = resume_text
    for i in range(max_loops):
        result = flow.run(jd_text, current_resume, max_loops=1)
        supervisor_feedback = result["evaluation"].get("feedback", "No feedback.")
        refined_resume = result["resume"]
        chat_turns.append({
            "role": "user",
            "content": f"**Job Description:**\n{jd_text}\n\n**Resume:**\n{current_resume}",
            "align": "left"
        })
        chat_turns.append({
            "role": "supervisor",
            "content": f"**Supervisor Feedback:**\n{supervisor_feedback}",
            "align": "right"
        })
        if not result["evaluation"].get("request_rebuild", False):
            break
        current_resume = refined_resume
    return chat_turns, refined_resume, resume_text

if st.button("Analyze and Refine Resume"):
    if not uploaded_file or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        # Reset chat history for a new analysis
        st.session_state.chat_history = []
        with st.spinner("Analyzing and refining resume..."):
            resume_text = extract_text_from_file(uploaded_file)
            chat_turns, refined_resume, original_resume = process_resume(jd_text, resume_text)
            st.session_state.original_resume = original_resume
            st.session_state.refined_resume = refined_resume
            st.session_state.chat_history.extend(chat_turns)




# Show only Supervisor Feedback (right-aligned) in chat window
for msg in st.session_state.chat_history:
    if msg.get("align") == "right":
        with st.container():
            st.markdown(f"<div style='text-align: right; background: #e6f7ff; padding: 10px; border-radius: 10px; margin: 5px 0;'>{msg['content']}</div>", unsafe_allow_html=True)


# Show download button for final refined resume only
if st.session_state.refined_resume:
    st.markdown("---")
    docx_buf = create_docx(st.session_state.refined_resume)
    st.download_button(
        label="Download Refined Resume as DOCX",
        data=docx_buf,
        file_name="refined_resume.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
