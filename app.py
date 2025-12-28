import analyze_resume  # Import your analyzer script
import main            # Import your scraper script (which we just modified)

def start_app():
    print("🚀 STARTING AUTOMATED JOB AGENT")
    print("===============================")
    
    # 1. Run the Analyzer to get titles
    # (We are reusing the code from analyze_resume, but for now let's just ask user to pick one)
    # Ideally, analyze_resume should have a function that returns the list.
    # For this portfolio step, let's simulate the connection:
    
    print("\n📂 Reading Resume & Analyzing...")
    
    # We define the list manually here based on what your AI just found
    # (In the next version, we will make analyze_resume return this list automatically)
    suggested_titles = [
        "Junior Software Developer",
        "Full Stack Developer",
        "IT Support Specialist",
        "Junior DevOps Engineer"
    ]
    
    print("\n🤖 AI suggests these roles for you:")
    for i, title in enumerate(suggested_titles):
        print(f"{i+1}. {title}")
        
    # 2. Ask User for Confirmation
    print("\n-------------------------------------------------")
    selection = input("Which job title should I scrape? (Enter number, or 'all'): ")
    
    titles_to_scrape = []
    
    if selection.lower() == 'all':
        titles_to_scrape = suggested_titles
    elif selection.isdigit():
        index = int(selection) - 1
        if 0 <= index < len(suggested_titles):
            titles_to_scrape = [suggested_titles[index]]
        else:
            print("❌ Invalid selection.")
            return
    else:
        # User typed a custom search
        titles_to_scrape = [selection]

    # 3. Start the Scraper Loop
    print(f"\n🌍 Starting Global Search for: {titles_to_scrape}")
    
    for title in titles_to_scrape:
        print(f"\n🔎 Searching Indeed for: {title}...")
        main.scrape_jobs(title)
        print("   Thinking/Resting for 5 seconds...")
        import time
        time.sleep(5) # Pause between searches to be safe

    print("\n✅ DONE! All jobs saved to jobs.csv")

if __name__ == "__main__":
    start_app()