from seleniumbase import Driver
import csv
import time

def scrape_edgeprop_selenium(urls):
    # Initialize the Undetected Chrome Driver
    driver = Driver(uc=True, headless=True)
    
    final_results = []
    
    try:
        for url in urls:
            print(f"🌐 Opening: {url}")
            driver.get(url)
            
            # Wait for the "Details" section to be visible in the DOM
            # This solves the N/A issue caused by dynamic rendering
            driver.wait_for_element("h3:contains('Details')", timeout=20)
            
            # Use JavaScript execution to pull data from the background JSON-LD tag
            # This is the most reliable "Source of Truth" in the HTML source
            data = driver.execute_script("""
                const tags = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
                for (let tag of tags) {
                    const json = JSON.parse(tag.innerHTML);
                    if (json['@type'] === 'Product') {
                        const props = json.additionalProperty || [];
                        return {
                            name: json.name || "N/A",
                            district: props.find(p => p.name === 'District/Planning Area')?.value || "N/A",
                            completion: props.find(p => p.name === 'Completion')?.value || "N/A"
                        };
                    }
                }
                return null;
            """)
            
            if data:
                final_results.append([data['name'], data['district'], data['completion'], url])
                print(f"   ✅ Success: {data['name']}")
            else:
                print("   ❌ Error: Data block not found.")
                final_results.append(["N/A", "N/A", "N/A", url])
                
            # Random sleep to mimic human behavior
            time.sleep(3)

    finally:
        driver.quit()

    # Save final results to CSV
    with open("edgeprop_selenium_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Project Name", "District/Planning Area", "Completion", "URL"])
        writer.writerows(final_results)

if __name__ == "__main__":
    urls = ["https://www.edgeprop.sg/condo-apartment/1-king-albert-park"]
    scrape_edgeprop_selenium(urls)