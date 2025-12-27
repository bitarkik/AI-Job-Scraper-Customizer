from playwright.sync_api import sync_playwright
import time
import random
import csv  # New library to handle saving data

def run():
    print("🤖 Bot is starting job search...")
    
    # Prepare the CSV file to save data
    # 'w' means write, 'newline=""' prevents empty lines in Excel
    file = open('jobs.csv', 'w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    # Create the headers (columns)
    writer.writerow(["Title", "Company", "Link"])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Search Indeed Canada
        page.goto("https://ca.indeed.com/jobs?q=Computer+Science&l=Canada")
        
        # Wait randomly
        time.sleep(random.uniform(3, 5))
        
        # Try to close popups
        try:
            page.locator("button[aria-label='close']").click(timeout=2000)
        except:
            pass
        
        # Get all the job cards (the container that holds title, company, link)
        # Note: Indeed changes classes often. 'td.resultContent' is a common container.
        job_cards = page.locator("td.resultContent").all()
        
        print(f"\n✅ Found {len(job_cards)} jobs. Extracting details...\n")
        
        for job in job_cards:
            try:
                # 1. Get Title
                title_element = job.locator("h2.jobTitle span")
                title = title_element.inner_text()
                
                # 2. Get Company Name
                # 'span[data-testid="company-name"]' is the standard tag
                company_element = job.locator('span[data-testid="company-name"]')
                if company_element.count() > 0:
                    company = company_element.inner_text()
                else:
                    company = "Unknown"

                # 3. Get Link
                # The link is usually on the <a> tag inside the title header
                link_element = job.locator("a").first
                link = "https://ca.indeed.com" + link_element.get_attribute("href")
                
                # Print to terminal so we see progress
                print(f"saved: {title} @ {company}")
                
                # Save to CSV file
                writer.writerow([title, company, link])
                
            except Exception as e:
                # If one job fails, don't crash the whole bot!
                print(f"⚠️ Error extracting a job: {e}")

        print("-" * 40)
        print("🎉 Success! Data saved to 'jobs.csv'.")
        
        file.close() # Close the file so we can open it
        browser.close()

if __name__ == "__main__":
    run()