# resume-analyzer-gemini
Upload a resume + job summary → get an AI-powered match %, rating, and explanation.

# 🤖 Resume Analyzer with Gemini 1.5 Pro

This is an AI-powered Resume Analyzer built using **Streamlit** and **Gemini 1.5 Pro**. Upload a resume and a job summary (either as text or file), and get:
- A **match percentage**
- A **rating out of 5**
- A **reason** explaining the score

### 🔍 Key Features

- Upload resumes as `.pdf` or `.docx`
- Upload or paste job summaries (`.txt` or `.pdf`)
- Uses Gemini AI to evaluate candidates
- Clean, responsive UI built with Streamlit

---

## 🖥️ Demo

> Coming soon – host this on Streamlit Cloud or locally to test it!

---

## 📸 Screenshots

### 🖥️ Main UI
![Main UI](screenshots/ui_demo.png)

### ✅ Output Example
![AI Output](screenshots/output_example.png)


## 🚀 How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/divyam8333/resume-analyzer-gemini.git
cd resume-analyzer-gemini

2. Install dependencies: pip install -r requirements.txt

3. Set up Gemini API key: genai.configure(api_key="YOUR_API_KEY")

Replace YOUR_API_KEY in resume_analyzer_app.py with your actual Google AI Studio API key.

4. Run the app: "streamlit run resume_analyzer_app.py"
