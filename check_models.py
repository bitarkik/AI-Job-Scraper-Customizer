import os
from dotenv import load_dotenv
from google import genai

# Load key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key missing")
else:
    print(f"✅ Key found. Asking Google for names...")
    try:
        client = genai.Client(api_key=api_key)
        
        # simplified loop - just print the name
        for model in client.models.list():
            print(f"Available: {model.name}")
            
    except Exception as e:
        print(f"❌ Error: {e}")