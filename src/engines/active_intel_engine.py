import requests
import json
import os
import tldextract
from bs4 import BeautifulSoup

OUTPUT_DIR = "data/active_intel/"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_html(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Sentinel-X Scanner)"}
        r = requests.get(url, headers=headers, timeout=10)
        return r.text
    except:
        return ""


def extract_emails(html):
    import re
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return list(set(re.findall(pattern, html)))


def extract_links(html, domain):
    soup = BeautifulSoup(html, "lxml")
    links = []

    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href and domain in href:
            links.append(href)

    return list(set(links))


def run_active_intel(domain):
    url = f"https://{domain}"
    print(f"🔍 Active-INTEL → {url}")

    html = fetch_html(url)

    result = {
        "domain": domain,
        "emails": extract_emails(html),
        "links": extract_links(html, domain)
    }

    path = os.path.join(OUTPUT_DIR, f"{domain}.json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2)

    return result
