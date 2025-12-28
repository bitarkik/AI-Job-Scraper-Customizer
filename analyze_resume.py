import os
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_pdf_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

def run():
    print("📂 Reading resume...")
    
    # CHANGE THIS to match your actual file name inside the resume folder
    resume_path = "resume/my_resume.pdf" 
    
    resume_text = get_pdf_text(resume_path)
    
    if not resume_text:
        return

    print(f"✅ Extracted {len(resume_text)} characters from your resume.")
    print("🧠 Analyzing with Gemini to find the best Job Titles...")

    # 2. Ask Gemini for Job Titles
    prompt = f"""
    Here is my resume text:
    {resume_text}
    
    Based strictly on my skills, education, and experience in this text, 
    list the top 5 Job Titles I should search for.
    
    Format the output as a simple list of titles, nothing else.
    """

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest", 
            contents=prompt
        )
        
        print("\n" + "="*40)
        print("🎯 RECOMMENDED JOB SEARCH TITLES")
        print("="*40)
        print(response.text)
        print("="*40)
        
    except Exception as e:
        print(f"❌ AI Error: {e}")

if __name__ == "__main__":
    run()