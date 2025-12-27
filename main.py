from playwright.sync_api import sync_playwright
import time
import random

def run():
    print("🤖 Bot is starting job search...")
    
    with sync_playwright() as p:
        # Launch browser (headless=False so we can see what it's doing)
        browser = p.chromium.launch(headless=False)
        
        # Create a new context with a realistic "User Agent" so we don't look like a robot
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # 1. Define the URL (Indeed Canada)
        # We are searching for "Computer Science" in "Canada"
        url = "https://ca.indeed.com/jobs?q=Computer+Science&l=Canada"
        
        print(f"🌍 Visiting: {url}")
        page.goto(url)
        
        # 2. Wait for the job cards to load (Simulate human reading time)
        # Random wait between 3 and 6 seconds is safer than a fixed number
        time.sleep(random.uniform(3, 6))
        
        # 3. Handle potential pop-ups (Like "Sign in with Google")
        try:
            # If a close button exists for a popup, click it
            page.locator("button[aria-label='close']").click(timeout=2000)
            print("🚫 Closed a pop-up")
        except:
            pass # No popup found, continue
            
        # 4. Find all job cards (This 'selector' is the tricky part that changes often!)
        # As of late 2024/2025, Indeed often uses 'h2.jobTitle' for the headers
        jobs = page.locator("h2.jobTitle span").all()
        
        print(f"\n✅ Found {len(jobs)} jobs on the first page! Here are the top ones:\n")
        print("-" * 40)
        
        # 5. Loop through and print them
        for i, job in enumerate(jobs):
            # Get the text inside the element
            title = job.inner_text()
            print(f"{i+1}. {title}")
            
        print("-" * 40)
        
        # Keep browser open for 10 seconds so you can admire your work
        time.sleep(10)
        browser.close()
        print("Bot finished.")

if __name__ == "__main__":
    run()