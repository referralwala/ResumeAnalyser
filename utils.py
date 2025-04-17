import PyPDF2
import docx
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def analyze_resume_with_gemini(resume_text):
    prompt = f"""
    Analyze the following resume for a candidate preparing for both technical and behavioral interviews.
    Provide the following:
    1. An overall score out of 100.
    2. Scores out of 10 for key parameters like clarity, relevance, skills, experience, and formatting.
    3. Specific suggestions for improvement.

    Resume:
    {resume_text}
    """

    model = genai.GenerativeModel("gemini-1.5-pro-002")
    response = model.generate_content(prompt)
    return response.text
