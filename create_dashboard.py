import os
import csv
import time
import warnings

# 1. Hide the "FutureWarning"
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai

# ================= CONFIGURATION =================
# 🔴 PASTE YOUR API KEY HERE 🔴
API_KEY = "AIzaSyA6hZOUCd_gAa4e--oWdE8uTO_TKUWX2i4" 

# Path to your CSV file
CSV_FILE = r"D:\JobAutoApplier\jobs_with_details.csv"

# Output HTML file path
OUTPUT_FILE = r"D:\JobAutoApplier\dashboard.html"

# Limit how many jobs to process for this test (set to 64 to do all)
JOB_LIMIT = 5 
# =================================================

def setup_gemini():
    """Configures the Gemini API."""
    if API_KEY == "YOUR_API_KEY_GOES_HERE":
        print("\n❌ STOP! You forgot to paste your API Key.")
        print("   Please edit create_dashboard.py and add your key on line 15.")
        return None
    
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel('gemini-1.5-flash')

def clean_text(text):
    if not text: return ""
    return text.replace("```html", "").replace("```", "").strip()

def generate_resume_points(model, job_description):
    """Asks AI to generate resume points."""
    # If description is too short, skip it
    if len(job_description) < 50:
        return "<ul><li><em>Job description was missing or too short.</em></li></ul>"

    prompt = f"""
    You are an expert Resume Writer.
    Read this job description and generate 3-4 impressive, results-oriented resume bullet points.
    
    JOB DESCRIPTION:
    {job_description[:8000]} 
    
    Output format: Return ONLY the bullet points as an HTML unordered list (<ul><li>...</li></ul>).
    """
    try:
        response = model.generate_content(prompt)
        return clean_text(response.text)
    except Exception as e:
        return f"<p style='color:red'>⚠️ Error: {str(e)}</p>"

def find_columns(headers):
    """Smartly figures out which columns are Title and Description."""
    title_idx = -1
    desc_idx = -1
    
    # Convert headers to lowercase for easy matching
    headers_lower = [h.lower() for h in headers]
    
    # Look for title column
    for i, h in enumerate(headers_lower):
        if "title" in h or "role" in h or "position" in h:
            title_idx = i
            break
            
    # Look for description column
    for i, h in enumerate(headers_lower):
        if "desc" in h or "summary" in h or "content" in h:
            desc_idx = i
            break
            
    return title_idx, desc_idx

def main():
    print("\n🎨 BUILDING DASHBOARD FROM CSV (Gemini 1.5 Flash)...")
    
    model = setup_gemini()
    if not model: return

    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: Could not find file: {CSV_FILE}")
        return

    # Start HTML
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Job Application Dashboard</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; padding: 20px; background: #f0f2f5; }
            h1 { text-align: center; color: #333; }
            .card { background: white; padding: 25px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h2 { color: #0056b3; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 0; }
            ul { line-height: 1.6; color: #444; padding-left: 20px; }
            li { margin-bottom: 8px; }
            .meta { font-size: 0.9em; color: #666; margin-bottom: 15px; }
        </style>
    </head>
    <body>
        <h1>🚀 Application Dashboard (Top matches)</h1>
    """

    # Read CSV
    with open(CSV_FILE, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader) # Read first row (headers)
        except StopIteration:
            print("❌ Error: CSV file is empty.")
            return

        # Figure out which columns are which
        title_col, desc_col = find_columns(headers)
        
        if title_col == -1 or desc_col == -1:
            print(f"❌ Error: Could not automatically identify 'Title' or 'Description' columns in your CSV.")
            print(f"   Found headers: {headers}")
            return

        print(f"   Found columns -> Title: '{headers[title_col]}', Description: '{headers[desc_col]}'")
        
        count = 0
        for row in reader:
            if count >= JOB_LIMIT: break
            
            # extract data safely
            try:
                job_title = row[title_col]
                job_desc = row[desc_col]
            except IndexError:
                continue # Skip bad rows

            count += 1
            print(f"   [{count}] Processing: {job_title[:40]}...")

            resume_points = generate_resume_points(model, job_desc)

            html_content += f"""
            <div class="card">
                <h2>{job_title}</h2>
                <div class="meta">Based on job description data</div>
                <div>{resume_points}</div>
            </div>
            """
            
            # Sleep to be nice to the API
            time.sleep(1.5)

    html_content += "</body></html>"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("\n✅ DASHBOARD READY!")
    print(f"👉 Go to D:\\JobAutoApplier and open 'dashboard.html'")

if __name__ == "__main__":
    main()