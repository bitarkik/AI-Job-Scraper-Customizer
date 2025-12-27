import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key not found!")
else:
    print(f"✅ Key found. Connecting to Gemini Stable...")

    try:
        client = genai.Client(api_key=api_key)
        
        # "gemini-flash-latest" points to the reliable 1.5 Flash model
        response = client.models.generate_content(
            model="gemini-flash-latest", 
            contents="Say 'Hello! I am the stable Gemini model and I am working!'"
        )
        
        print(f"\n🤖 AI Response: {response.text}")
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")