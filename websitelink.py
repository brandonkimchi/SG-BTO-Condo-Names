import re
import pandas as pd
import csv

BASE = "https://www.edgeprop.sg/condo-apartment/"

def condo_name_to_slug(name: str) -> str:
    if pd.isna(name):
        return ""

    s = str(name).strip()

    # Remove surrounding quotes
    if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ("'", '"')):
        s = s[1:-1].strip()

    # Remove leading "#"
    s = re.sub(r"^#\s*", "", s)

    # Convert apostrophes to dash (so D'FRESCO → D-FRESCO)
    s = s.replace("’", "-").replace("'", "-")

    # Handle (old) → old
    s = re.sub(r"\(\s*old\s*\)", " old", s, flags=re.IGNORECASE)

    # Replace @ with space
    s = s.replace("@", " ")

    # Remove any remaining invalid characters
    s = re.sub(r"[^A-Za-z0-9\s-]+", " ", s)

    # Normalize spaces
    s = re.sub(r"\s+", " ", s).strip()

    # Convert spaces to hyphens
    slug = s.replace(" ", "-").lower()

    # Remove duplicate hyphens
    slug = re.sub(r"-{2,}", "-", slug).strip("-")

    return slug


def make_url(name: str) -> str:
    slug = condo_name_to_slug(name)
    return BASE + slug if slug else ""


def main():
    df = pd.read_csv("edgeprop_condo_list.csv")
    col = df.columns[0]

    urls = df[col].apply(make_url)

    urls.to_csv(
        "edgeprop_condo_urls.csv",
        index=False,
        header=False,
        quoting=csv.QUOTE_ALL
    )

    print("Done.")


if __name__ == "__main__":
    main()