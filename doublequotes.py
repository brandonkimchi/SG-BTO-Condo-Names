import csv

input_file = 'edgeprop_condo_list.csv'
output_file = 'edgeprop_condo_quoted.csv'

with open(input_file, mode='r', encoding='utf-8') as infile:
    # Use csv.QUOTE_ALL to wrap every field in "", 
    # or logic below to target just the name
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        # QUOTE_NONNUMERIC wraps all strings in ""
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in reader:
            writer.writerow(row)

print(f"✅ Done! Quoted names saved to {output_file}")