import sys

import requests

from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scraper.analyzer import generate_prospect_card
from scraper.claude_cli import ClaudeCLIError
from scraper.core import fetch_page, parse_page

load_dotenv()

OUR_SOLUTION = "a generic B2B software solution that saves time and cuts costs"


def main():
    url = input("Enter the company's website URL: ").strip()

    if not url:
        print("No URL entered. Exiting.")
        return

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        html = fetch_page(url)
    except requests.exceptions.RequestException as error:
        print(f"Failed to fetch {url}: {error}")
        return

    data = parse_page(html)

    print("\nAnalyzing company...\n")
    try:
        card = generate_prospect_card(OUR_SOLUTION, url, data["title"], data["text"])
    except ClaudeCLIError as error:
        print(f"Failed to generate prospect card: {error}")
        return

    print(card)


if __name__ == "__main__":
    main()
