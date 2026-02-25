import requests
from bs4 import BeautifulSoup
import csv

def scrape_bto_refined():
    url = "https://www.housingmap.sg/bto/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    print(f"Fetching data from {url}...")
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed. Status code: {response.status_code}")
            return
    except Exception as e:
        print(f"Error: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        print("Table not found.")
        return

    rows = table.find_all('tr')
    bto_list = []
    
    # Define your custom headers
    desired_headers = ["Town Name", "BTO Name", "Units", "Launch Date", "Type"]

    for row in rows[1:]:  # Skip the original header row
        cells = row.find_all('td')
        
        # Ensure row has enough data columns (at least Town, Name, Units, Date, Completion, Type)
        if len(cells) < 6:
            continue
            
        raw_data = [cell.get_text(strip=True) for cell in cells]
        
        # Skip 'Year' separator rows (usually Town is empty and Name contains 'Year')
        if not raw_data[0] and "Year" in raw_data[1]:
            continue
        # Skip rows that are empty or header repeats
        if raw_data[1] == "" or raw_data[1] == "BTO name":
            continue

        # Select only the specific indices we want
        # 0: Town, 1: BTO Name, 2: Units, 3: Launch Date, 5: Type
        refined_data = [
            raw_data[0], 
            raw_data[1], 
            raw_data[2], 
            raw_data[3], 
            raw_data[5]
        ]
        
        bto_list.append(refined_data)

    # Save to CSV
    filename = "sg_bto_list.csv"
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(desired_headers) 
            writer.writerows(bto_list)
        print(f"Success! Scraped {len(bto_list)} projects into {filename}")
    except IOError as e:
        print(f"CSV Error: {e}")

if __name__ == "__main__":
    scrape_bto_refined()