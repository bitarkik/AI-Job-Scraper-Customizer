from playwright.sync_api import sync_playwright
import time
import random
import csv

# We moved the logic inside this function so other scripts can call it
def scrape_jobs(search_term):
    print(f"🤖 Bot is starting search for: '{search_term}'...")
    
    # We will append to the file so we don't overwrite previous searches
    # 'a' mode means append
    file = open('jobs.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(file)
    
    # Only write headers if the file is empty (optional check, skipping for simplicity)
    # writer.writerow(["Title", "Company", "Link"]) 

    found_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # SEARCH for the specific term passed to the function
        # We replace spaces with "+" for the URL (e.g., "Full Stack" -> "Full+Stack")
        query = search_term.replace(" ", "+")
        url = f"https://ca.indeed.com/jobs?q={query}&l=Canada"
        
        page.goto(url)
        time.sleep(random.uniform(3, 5))
        
        try:
            page.locator("button[aria-label='close']").click(timeout=2000)
        except:
            pass
        
        job_cards = page.locator("td.resultContent").all()
        print(f"   ✅ Found {len(job_cards)} jobs for {search_term}.")
        
        for job in job_cards:
            try:
                title = job.locator("h2.jobTitle span").inner_text()
                
                # Get Link
                link_element = job.locator("a").first
                link = "https://ca.indeed.com" + link_element.get_attribute("href")
                
                # Get Company
                company_element = job.locator('span[data-testid="company-name"]')
                if company_element.count() > 0:
                    company = company_element.inner_text()
                else:
                    company = "Unknown"

                # Save to CSV
                writer.writerow([title, company, link])
                found_jobs.append(title)
                
            except:
                pass

        browser.close()
    
    file.close()
    return found_jobs

if __name__ == "__main__":
    # Test it manually if we run this file directly
    scrape_jobs("Python Developer")