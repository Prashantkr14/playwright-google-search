from playwright.sync_api import sync_playwright
import os
from datetime import datetime

def search_google():
    with sync_playwright() as p:
        # Determine headless mode based on environment
        headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        
        try:
            print("Navigating to Google...")
            page.goto("https://www.google.com")
            
            # Handle cookies
            try:
                accept_button = page.locator('button:has-text("Accept all")')
                if accept_button.is_visible(timeout=2000):
                    accept_button.click()
                    print("Accepted cookies")
            except:
                print("No cookie dialog found")
            
            # Perform search
            query = "what is the future of SDET role in IT"
            print(f"Searching for: {query}")
            
            search_box = page.locator('textarea[name="q"]')
            search_box.fill(query)
            search_box.press("Enter")
            
            # Wait for results
            page.wait_for_selector("#search", timeout=10000)
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs("results", exist_ok=True)
            page.screenshot(path=f"results/search_{timestamp}.png", full_page=True)
            print(f"Screenshot saved to results/search_{timestamp}.png")
            
            # Display results
            results = page.locator('h3').all()[:5]
            print(f"\nTop {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.text_content()}")
            
            print("\n✅ Search completed successfully!")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
            
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    search_google()