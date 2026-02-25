import requests
from bs4 import BeautifulSoup
import csv
import time
import re

def get_town_mapping(dist_str):
    mapping = {
        "01": "Boat Quay, Chinatown, Marina Square", "02": "Shenton Way, Tanjong Pagar",
        "03": "Alexandra Road, Tiong Bahru, Queenstown", "04": "Keppel, Sentosa, Telok Blangah",
        "05": "Buona Vista, West Coast, Clementi", "06": "City Hall, North Bridge Road",
        "07": "Beach Road, Bugis, Rochor", "08": "Little India, Farrer Park",
        "09": "Orchard, River Valley", "10": "Bukit Timah, Holland, Tanglin",
        "11": "Newton, Dunearn, Watten Estate", "12": "Balestier, Toa Payoh, Serangoon",
        "13": "Potong Pasir, Macpherson", "14": "Eunos, Geylang, Paya Lebar",
        "15": "Katong, Marine Parade, Siglap", "16": "Bedok, Upper East Coast",
        "17": "Changi, Loyang, Pasir Ris", "18": "Tampines, Pasir Ris, Simei",
        "19": "Hougang, Sengkang, Punggol", "20": "Ang Mo Kio, Bishan, Thomson",
        "21": "Clementi, Upper Bukit Timah", "22": "Boon Lay, Jurong, Tuas",
        "23": "Bukit Batok, Choa Chu Kang, Hillview", "24": "Kranji, Lim Chu Kang, Tengah",
        "25": "Admiralty, Woodlands", "26": "Tagore, Yio Chu Kang",
        "27": "Sembawang, Yishun", "28": "Seletar, Yio Chu Kang"
    }
    return mapping.get(dist_str, "Unknown")

def scrape_by_district():
    base_url = "https://www.singaporeexpats.com/condo/district/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    all_condos = []

    for i in range(1, 29):
        dist_str = str(i).zfill(2)
        url = f"{base_url}{dist_str}"
        print(f"🔍 Fetching District {dist_str}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            town = get_town_mapping(dist_str)
            
            # The condo name is usually inside <a> tags within specific headers
            # We target text blocks that contain 'Estimated TOP'
            rows = soup.find_all(string=re.compile(r"Estimated TOP:"))

            for row in rows:
                parent = row.find_parent()
                if not parent: continue
                
                # Find the nearest <a> tag for the Condo Name
                name_tag = parent.find_previous('a') or parent.find('a')
                if not name_tag: continue
                
                name = name_tag.get_text(strip=True)
                
                # Search for TOP year in the parent's text
                year_match = re.search(r"Estimated TOP:\s*(\d{4})", parent.get_text())
                top_year = year_match.group(1) if year_match else "N/A"
                
                # Filtering for 2001+
                try:
                    if top_year != "N/A" and int(top_year) >= 2001:
                        all_condos.append([name, town, f"District {dist_str}", top_year])
                except ValueError:
                    continue

            time.sleep(1.5) # Anti-ban delay
            
        except Exception as e:
            print(f"Error on District {dist_str}: {e}")

    # Export
    filename = "sg_condo_list.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Condo Name", "Town", "District", "Launch Date (TOP)"])
        writer.writerows(all_condos)
    
    print(f"Success! Saved {len(all_condos)} condos to {filename}")

if __name__ == "__main__":
    scrape_by_district() 