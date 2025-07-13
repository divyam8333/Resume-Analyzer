import PyPDF2
import json
import os
from groq import Groq

os.environ["GROQ_API_KEY"] = "put_groq_api_key_here"
client = Groq(api_key=os.environ["GROQ_API_KEY"])

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None
    return text.strip()

def evaluate_resume(resume_text, jd_text):
    """Uses a language model to compare a resume with a job description."""
    input_prompt = f"""
    Act as an advanced AI-powered resume analyzer specializing in the engineering field.
    Your task is to evaluate the provided resume against the job description and generate a
    rating out of 5 based on how well they match.

    ### Evaluation Criteria:
    - Higher rating for close alignment with job description (skills, experience, qualifications)
    - Lower rating if important aspects are missing
    - Provide a clear explanation for the rating

    ### Output Format:
    Return ONLY a raw JSON object:
    {{
        "JD Match": "%",
        "CV Rating": "X/5",
        "Summary": "Explain the rating, highlighting key matches and gaps."
    }}

    ### Input Data:
    Resume Content:
    '''{resume_text}'''

    Job Description Content:
    '''{jd_text}'''
    """

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a resume analyzer expert."},
                {"role": "user", "content": input_prompt}
            ]
        )
        content = response.choices[0].message.content.strip()
        cleaned = content.replace("```json", "").replace("```", "").strip()
        result = json.loads(cleaned)
        return result

    except json.JSONDecodeError:
        print("Error: Invalid JSON response. Full content:\n", response.choices[0].message.content)
    except Exception as e:
        print("Error during evaluation:", e)

    return {"JD Match": "0%", "CV Rating": "0/5", "Summary": "Failed to evaluate resume."}

def main():
    """Main function to load PDFs, extract text, evaluate, and print results."""
    resume_pdf = "Aman8333 AI-DS_compressed.pdf"
    jd_pdf = "Python JD.pdf"

    print("📄 Extracting resume text...")
    resume_text = extract_text_from_pdf(resume_pdf)
    print("📄 Extracting job description text...")
    jd_text = extract_text_from_pdf(jd_pdf)

    if not resume_text or not jd_text:
        print("Error: Could not extract text from one or both PDFs.")
        return

    print("🧠 Evaluating resume against job description...")
    match_result = evaluate_resume(resume_text, jd_text)

    print("\n📊 Evaluation Result:")
    print(f"✅ CV Rating: {match_result['CV Rating']}")
    print(f"✅ JD Match: {match_result['JD Match']}")
    print(f"📝 Summary: {match_result['Summary']}")

main()
