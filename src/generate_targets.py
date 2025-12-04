# =====================================================
# DIGITAL SENTINEL - TARGET GENERATOR BOT
# =====================================================
# Purpose: Fetch 500 authorized bug bounty domains
#          from public directories (HackerOne, Bugcrowd, etc.)
# =====================================================

import os
import re
import requests
from bs4 import BeautifulSoup

OUTPUT_FILE = "data/targets.txt"
os.makedirs("data", exist_ok=True)


def fetch_hackerone():
    print("[+] Fetching from HackerOne...")
    url = "https://hackerone.com/directory/programs"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    targets = []
    for a in soup.find_all("a", href=True):
        link = a["href"]
        if link.startswith("/"):
            continue
        m = re.search(r"https?://([^/]+)/?", link)
        if m:
            targets.append(m.group(1))
    return list(set(targets))[:150]


def fetch_bugcrowd():
    print("[+] Fetching from Bugcrowd...")
    url = "https://www.bugcrowd.com/bug-bounty-list/"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    targets = []
    for a in soup.find_all("a", href=True):
        m = re.search(r"https?://([^/]+)/?", a["href"])
        if m:
            targets.append(m.group(1))
    return list(set(targets))[:150]


def fetch_intigriti():
    print("[+] Fetching from Intigriti...")
    url = "https://www.intigriti.com/programs"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    targets = []
    for a in soup.find_all("a", href=True):
        m = re.search(r"https?://([^/]+)/?", a["href"])
        if m:
            targets.append(m.group(1))
    return list(set(targets))[:100]


def fetch_yeswehack():
    print("[+] Fetching from YesWeHack...")
    url = "https://www.yeswehack.com/programs"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    targets = []
    for a in soup.find_all("a", href=True):
        m = re.search(r"https?://([^/]+)/?", a["href"])
        if m:
            targets.append(m.group(1))
    return list(set(targets))[:100]


def generate_master_list():
    print("🚀 Generating combined authorized target list...")
    all_targets = set()

    for fetcher in [fetch_hackerone, fetch_bugcrowd, fetch_intigriti, fetch_yeswehack]:
        try:
            result = fetcher()
            all_targets.update(result)
        except Exception as e:
            print(f"[!] Error fetching: {e}")

    # Filter and clean
    final_targets = sorted(set([t.lower() for t in all_targets if "." in t]))[:500]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(final_targets))

    print(f"[+] Saved {len(final_targets)} authorized targets → {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_master_list()
