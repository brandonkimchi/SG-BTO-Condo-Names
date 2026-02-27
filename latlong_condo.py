import pandas as pd
import requests
import time

def get_coordinates(postal_code):
    """
    Ensures postal code is 6 digits and queries OneMap API.
    """
    # Convert to string, remove decimals, and pad to 6 digits
    clean_code = str(postal_code).split('.')[0].strip()
    formatted_code = clean_code.zfill(6)
    
    url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={formatted_code}&returnGeom=Y&getAddrDetails=N"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['found'] > 0:
                result = data['results'][0]
                return f"{result['LATITUDE']},{result['LONGITUDE']}", formatted_code
            return "Not Found", formatted_code
        return "API Error", formatted_code
            
    except Exception as e:
        return f"Error: {e}", formatted_code

def process_csv(input_csv, output_csv):
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f"Error: {input_csv} not found.")
        return

    target_col = 'postal_code' 
    if target_col not in df.columns:
        print(f"Error: Column '{target_col}' not found.")
        return

    total_rows = len(df)
    print(f"Starting process for {total_rows} rows...\n")

    results = []
    
    # Using enumerate to keep track of the row index
    for index, code in enumerate(df[target_col], start=1):
        coord_result, padded_code = get_coordinates(code)
        results.append(coord_result)
        
        # This prints the progress for every single row
        print(f"Row {index}/{total_rows} completed | Code: {padded_code} | Result: {coord_result}")
        
        # Small delay to prevent API blocking
        time.sleep(0.1) 
    
    df['lat_long'] = results
    df.to_csv(output_csv, index=False)
    print(f"\nFinished! Results saved to {output_csv}")

if __name__ == "__main__":
    process_csv('condo_postal_code.csv', 'condo_with_coords.csv')