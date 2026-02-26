import csv
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://www.edgeprop.sg/condo-apartment/all"


def scrape_condo_names(url: str) -> list[str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; condo-list-script/1.0; +https://example.com)"
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    names = []
    seen = set()

    # The page contains the directory as a big list of <a href="/condo-apartment/<slug>">NAME</a>
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()

        if not href.startswith("/condo-apartment/"):
            continue
        if href in ("/condo-apartment/", "/condo-apartment/all"):
            continue

        text = a.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()

        if text and text not in seen:
            seen.add(text)
            names.append(text)

    return names


def main() -> int:
    out_path = Path("edgeprop_condo_list.csv").resolve()
    print("Saving to:", out_path)

    try:
        names = scrape_condo_names(URL)
    except Exception as e:
        print("ERROR while fetching/parsing:", e)
        return 1

    # Always write the file (even if 0 names, so you can see it created)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["condo_name"])
        for n in names:
            w.writerow([n])

    print(f"Wrote {len(names)} condo names to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())