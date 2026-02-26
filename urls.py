input_file = "edgeprop_condo_urls.csv"
output_file = "urlz.py"

urls = []

# Read URLs (strip quotes and whitespace)
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        url = line.strip().strip('"')
        if url:
            urls.append(url)

# Write Python list file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("urls = [\n")
    for url in urls:
        f.write(f'    "{url}",\n')
    f.write("]\n")

print(f"Done. {len(urls)} URLs written to {output_file}")