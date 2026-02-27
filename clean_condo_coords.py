import pandas as pd

# 1. Load the data from your CSV
df = pd.read_csv('condo_with_coords.csv')

# 2. Extract only the 'lat_long' column
# Since the CSV reader has already parsed the string, the " quotes are already gone.
lat_long_list = df['lat_long']

# 3. Save the values to a new file (one coordinate pair per line)
with open('cleaned_lat_long.csv', 'w') as f:
    # Optional: Write a header if you want one
    # f.write("lat_long\n")
    for item in lat_long_list:
        f.write(f"{item}\n")

print("Cleaning complete. The coordinates are saved in 'cleaned_lat_long.csv'.")