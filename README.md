# Singapore BTO Historical Data Scraper

## Project Overview
This project is a Python-based web scraper designed to compile a comprehensive historical list of **Housing & Development Board (HDB) Build-To-Order (BTO)** projects in Singapore. 

Since the BTO system's inception in 2001, HDB typically removes project-specific information from its official portal once a sales exercise concludes. This tool solves that data-gap by scraping **housingmap.sg**, a community-driven archive that tracks BTO launches from 2001 to the present (including upcoming 2026 launches).

## Objective
The primary goal is to generate a clean, machine-readable dataset (`.csv`) containing essential details for every BTO project for use in:

## Extracted Data Points
For every BTO project, the scraper extracts the following specific fields:

| Field | Description |
| :--- | :--- |
| **Town Name** | The HDB estate (e.g., Tampines, Tengah, Bukit Merah). |
| **BTO Name** | The official name of the development (e.g., *Redhill Peaks*). |
| **Units** | The total number of dwelling units offered in that project. |
| **Launch Date** | The official date the project was released for application. |
| **Type** | The classification (Standard, Plus, or Prime/PLH). |

## Technical Stack
* **Language:** Python 
* **Libraries:** * `requests`: To handle HTTP requests and retrieve page content.
    * `BeautifulSoup4`: To parse the HTML DOM and navigate the table structure.
    * `csv`: To format and save the final output.


