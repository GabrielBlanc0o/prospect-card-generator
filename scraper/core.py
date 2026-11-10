import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"
    links = [a.get("href") for a in soup.find_all("a", href=True)]

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = " ".join(soup.get_text(separator=" ").split())

    return {
        "title": title,
        "links": links,
        "text": text,
    }
