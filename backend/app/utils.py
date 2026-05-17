import re
from urllib.parse import urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

from .config import settings


def normalize_website_url(raw_url: str) -> str:
    raw_url = raw_url.strip()
    if not raw_url:
        raise ValueError("Website URL is required.")

    parsed = urlparse(raw_url)
    if not parsed.scheme:
        raw_url = f"https://{raw_url}"
        parsed = urlparse(raw_url)

    if not parsed.netloc:
        raise ValueError("Invalid website URL format.")

    normalized = urlunparse(parsed)
    return normalized


def extract_visible_text(soup: BeautifulSoup, max_chars: int = 2400) -> str:
    for tag in soup(['script', 'style', 'noscript', 'header', 'footer', 'nav', 'form']):
        tag.extract()

    text = soup.get_text(separator=" ", strip=True)
    return text[:max_chars]


def safe_website_scrape(url: str) -> dict[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=settings.WEBSITE_TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        description = ""
        if soup.find("meta", attrs={"name": "description"}):
            description = soup.find("meta", attrs={"name": "description"}).get("content", "").strip()
        elif soup.find("meta", attrs={"property": "og:description"}):
            description = soup.find("meta", attrs={"property": "og:description"}).get("content", "").strip()

        headings = []
        for heading in soup.find_all(["h1", "h2", "h3"]):
            heading_text = heading.get_text(strip=True)
            if heading_text:
                headings.append(heading_text)
                if len(headings) >= 8:
                    break

        visible_text = extract_visible_text(soup)
        html = str(soup.body) if soup.body else ""

        return {
            "title": title,
            "description": description,
            "headings": " | ".join(headings),
            "visible_text": visible_text,
            "raw_html": html,
        }
    except Exception as error:
        return {
            "title": "",
            "description": "",
            "headings": "",
            "visible_text": "",
            "raw_html": "",
            "error": str(error),
        }


def extract_domain_from_email(email: str) -> str:
    if "@" not in email:
        return ""
    domain = email.split("@")[-1]
    cleaned = re.sub(r"^www\.", "", domain.lower())
    return f"https://{cleaned}" if not cleaned.startswith("http") else cleaned
