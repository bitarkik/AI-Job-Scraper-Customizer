from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random

def run():
    # Load the CSV
    try:
        df = pd.read_csv("jobs.csv")
    except:
        print("❌ Error: Could not find jobs.csv.")
        return

    print(f"Loaded {len(df)} jobs.")
    descriptions = []

    with sync_playwright() as p:
        # Launch browser (Headless=False is required to see the CAPTCHA)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # We only try the FIRST job now to get one good sample
        # We grab the first row
        row = df.iloc[0] 
        url = row['Link']
            
        print(f"\nmagnifying_glass_tilted_left Visiting: {row['Title']}")
        print("-------------------------------------------------")
        print("🚨 IMPORTANT: If you see a 'Verify you are human' box:")
        print("1. Click the box manually in the browser.")
        print("2. Wait for the job description to load.")
        print("3. Come back here and press ENTER.")
        print("-------------------------------------------------")
        
        page.goto(url)
        
        # === THE MANUAL PAUSE ===
        input("Press ENTER in this terminal once the page is loaded...")
        # ========================

        try:
            # Now we try to copy the text
            desc_element = page.locator("#jobDescriptionText")
            description_text = desc_element.inner_text()
            print("✅ Copied description!")
        except:
            print("⚠️ Still couldn't find description.")
            description_text = "N/A"
        
        descriptions.append(description_text)
        browser.close()

    # Save just this one result for now
    df_small = df.head(1).copy()
    df_small["Description"] = descriptions
    df_small.to_csv("jobs_with_details.csv", index=False)
    print("\n🎉 Saved the first job to 'jobs_with_details.csv'")

if __name__ == "__main__":
    run()