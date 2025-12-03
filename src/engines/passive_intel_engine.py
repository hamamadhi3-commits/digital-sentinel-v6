import requests
import tldextract
import json
import os
from bs4 import BeautifulSoup

RESULT_DIR = "data/results/"
os.makedirs(RESULT_DIR, exist_ok=True)


def save_result(domain, data):
    out = os.path.join(RESULT_DIR, f"{domain}_passive.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def fetch_html(domain):
    try:
        r = requests.get(f"http://{domain}", timeout=5)
        return r.text
    except:
        return ""


def extract_links(html):
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.find_all("a", href=True):
        links.append(a["href"])
    return links


def extract_subdomains(domain):
    # Simple placeholder — later we upgrade with amass/subfinder
    parts = domain.split(".")
    base = ".".join(parts[-2:])
    return [
        f"app.{base}",
        f"dev.{base}",
        f"api.{base}"
    ]


def passive_collect(domain):
    print(f"[+] Passive collecting → {domain}")

    html = fetch_html(domain)
    links = extract_links(html)
    subs = extract_subdomains(domain)

    result = {
        "domain": domain,
        "subdomains": subs,
        "links": links,
        "total_links": len(links)
    }

    save_result(domain, result)
    return result
