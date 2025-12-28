import pandas as pd
import time
import random
import os
from dotenv import load_dotenv
from google import genai
from playwright.sync_api import sync_playwright

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def force_kill_edge():
    """Kills all running Edge processes to unlock the profile."""
    print("🔪 Force-killing lingering Edge processes...")
    try:
        # /F = Force, /IM = Image Name, /T = Tree (kill child processes)
        os.system("taskkill /F /IM msedge.exe /T >nul 2>&1")
        time.sleep(2) # Wait for files to unlock
        print("   ✅ Edge killed. Profile unlocked.")
    except Exception as e:
        print(f"   ⚠️ Warning: Could not kill Edge (might be already closed).")

def get_job_description(page, url):
    try:
        page.goto(url, timeout=60000)
        time.sleep(random.uniform(4, 8)) 
        desc = page.locator("#jobDescriptionText").inner_text()
        return desc
    except:
        return None

def check_experience_with_ai(description):
    prompt = f"""
    Analyze this job description.
    Does it STRICTLY require MORE than 2 years of professional work experience?
    
    Rules:
    - If it says "3+ years", "5 years", "Senior": Answer YES.
    - If it says "0-2 years", "1 year", "Entry Level", "New Grad", or doesn't mention years: Answer NO.
    - If it lists "2 years" exactly: Answer NO (it fits the user).
    
    Job Text:
    {description[:2000]}
    
    Respond with exactly one word: YES or NO.
    """
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest", 
            contents=prompt
        )
        answer = response.text.strip().upper()
        if "YES" in answer: return True
        return False
    except:
        return False 

def run():
    print("🛡️ GATEKEEPER STARTING (Edge Mode + Auto-Kill)...")
    
    # STEP 0: KILL EDGE
    force_kill_edge()
    
    try:
        df = pd.read_csv("jobs.csv")
    except:
        print("❌ No jobs.csv found.")
        return

    print(f"📋 Loaded {len(df)} jobs.")
    
    valid_jobs = []
    
    # Edge Data Path
    user_data_dir = os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data")
    
    # Find Edge Exe
    possible_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    
    executable_path = None
    for path in possible_paths:
        if os.path.exists(path):
            executable_path = path
            break
            
    if not executable_path:
        print("❌ Error: Could not find msedge.exe.")
        return

    with sync_playwright() as p:
        try:
            # Launch with specific arguments to prevent crashes
            browser = p.chromium.launch_persistent_context(
                user_data_dir,
                executable_path=executable_path,
                headless=False,
                channel="msedge",
                # 'no-sandbox' helps prevent permission crashes
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"] 
            )
            page = browser.pages[0] 
        except Exception as e:
            print(f"❌ Error launching Edge: {e}")
            print("👉 Try restarting your computer if this keeps happening.")
            return

        for index, row in df.iterrows():
            title = row['Title']
            url = row['Link']
            
            print(f"\n[{index+1}/{len(df)}] Checking: {title}")
            
            desc = get_job_description(page, url)
            
            if not desc:
                print("   ⚠️ Skipped (No text found or blocked).")
                continue
                
            is_too_senior = check_experience_with_ai(desc)
            
            if is_too_senior:
                print("   ⛔ REJECTED: Too Senior.")
            else:
                print("   ✅ APPROVED: Entry Level!")
                row['Description'] = desc
                valid_jobs.append(row)

        browser.close()

    if valid_jobs:
        new_df = pd.DataFrame(valid_jobs)
        new_df.to_csv("filtered_jobs.csv", index=False)
        print(f"\n🎉 DONE! Saved {len(new_df)} valid jobs.")
    else:
        print("\n😔 No jobs survived.")

if __name__ == "__main__":
    run()