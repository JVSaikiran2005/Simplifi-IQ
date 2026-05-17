from pathlib import Path
from typing import Any

from ..config import settings
from ..utils import extract_domain_from_email, normalize_website_url, safe_website_scrape


def enrich_company_profile(company_name: str, company_website: str, email: str) -> dict[str, Any]:
    website_url = normalize_website_url(company_website)
    scraped = safe_website_scrape(website_url)

    if not scraped.get("visible_text") and email:
        fallback_url = extract_domain_from_email(email)
        if fallback_url and fallback_url != website_url:
            fallback_scraped = safe_website_scrape(fallback_url)
            if fallback_scraped.get("visible_text"):
                scraped = {**scraped, **fallback_scraped}
                website_url = fallback_url

    profile = {
        "company_name": company_name,
        "company_website": website_url,
        "website_title": scraped.get("title", ""),
        "website_description": scraped.get("description", ""),
        "website_headings": scraped.get("headings", ""),
        "website_text": scraped.get("visible_text", ""),
        "scrape_error": scraped.get("error", ""),
    }

    return profile
