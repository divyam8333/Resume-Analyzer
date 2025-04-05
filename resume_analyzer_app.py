import streamlit as st
import fitz  # PyMuPDF
import docx
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="YOUR_API_KEY")  
model = genai.GenerativeModel("gemini-1.5-pro")

# Extracting text from PDF
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Extracting text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Extracting text from TXT
def extract_text_from_txt(file):
    return file.read().decode("utf-8")

# Analyze resume with match percentage, rating, and reason
def analyze_resume(resume_text, job_summary):
    prompt = f"""
You are a resume screening expert.

Given the following:
1. **Job Summary**:
{job_summary}

2. **Candidate Resume**:
{resume_text}

Your task:
- Estimate how well the resume matches the job summary in terms of skills, experience, education, and keywords.
- Provide a **match percentage** (0%–100%).
- Give a **rating out of 5** (whole number).
- Provide a short **reason** for this rating and what skills are missing in resume.

Respond in **this format**:

Match: XX%
Rating: X/5
Reason: [Your reasoning]

Be concise but informative.
"""
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.set_page_config(page_title="Resume Analyzer", layout="centered")
st.title("📄 Resume Analyzer with Gemini")
st.markdown("Upload resumes and a job summary to get match %, rating (out of 5), and reasoning.")

# Job Summary Input
st.header("📝 Job Description")
job_file = st.file_uploader("Upload Job Description (PDF or TXT)", type=["pdf", "txt"])
job_text_input = st.text_area("Or type/paste Job Description here (optional)", height=200)

job_summary = ""
if job_file:
    if job_file.type == "application/pdf":
        job_summary = extract_text_from_pdf(job_file)
    elif job_file.type == "text/plain":
        job_summary = extract_text_from_txt(job_file)
    else:
        st.error("Unsupported file type for job summary.")
elif job_text_input.strip():
    job_summary = job_text_input.strip()

# Resume Upload Section
st.header("📁 Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload Resumes (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# Analyze Button
if st.button("🔍 Analyze Resumes"):
    if not job_summary:
        st.warning("Please upload or type a job summary.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        for file in uploaded_files:
            st.markdown(f"### 📄 {file.name}")
            try:
                # Extract resume text
                if file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(file)
                elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_text = extract_text_from_docx(file)
                else:
                    st.error("Unsupported resume file type.")
                    continue

                with st.spinner("Analyzing..."):
                    result = analyze_resume(resume_text, job_summary)
                    st.success("✅ Analysis complete")
                    st.markdown(f"```{result}```")

            except Exception as e:
                st.error(f"❌ Error analyzing {file.name}: {e}")
