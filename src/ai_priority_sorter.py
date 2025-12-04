import requests
import json
import time
import re
from bs4 import BeautifulSoup

INPUT_FILE = "data/targets.txt"
OUTPUT_FILE = "data/sorted_targets.txt"

def get_alexa_rank(domain):
    try:
        resp = requests.get(f"https://www.alexa.com/siteinfo/{domain}", timeout=10)
        if resp.status_code == 200:
            match = re.search(r'"globalRank":{"rank":([0-9]+)}', resp.text)
            if match:
                return int(match.group(1))
    except Exception:
        pass
    return 999999  # Default large rank if unknown

def detect_platform(domain):
    if "hackerone" in domain:
        return "HackerOne"
    elif "bugcrowd" in domain:
        return "Bugcrowd"
    elif "intigriti" in domain:
        return "Intigriti"
    elif "yeswehack" in domain:
        return "YesWeHack"
    elif "openbugbounty" in domain:
        return "OpenBugBounty"
    elif "federacy" in domain:
        return "Federacy"
    else:
        return "General"

def estimate_bounty_priority(domain):
    high = ["hackerone", "bugcrowd", "intigriti", "yeswehack", "openbugbounty", "federacy"]
    if any(x in domain for x in high):
        return 10
    if any(x in domain for x in ["meta", "apple", "tesla", "google", "microsoft", "paypal"]):
        return 9
    if any(x in domain for x in ["cloudflare", "amazon", "oracle", "zoom", "discord"]):
        return 8
    return 5

def sort_targets():
    print("🧠 AI Priority Target Sorter v12+ Initializing...")
    targets = []
    with open(INPUT_FILE, "r") as f:
        for line in f:
            domain = line.strip().lower()
            if not domain or domain.startswith("#"):
                continue
            platform = detect_platform(domain)
            bounty_score = estimate_bounty_priority(domain)
            alexa_rank = get_alexa_rank(domain)
            targets.append({
                "domain": domain,
                "platform": platform,
                "bounty_score": bounty_score,
                "alexa_rank": alexa_rank
            })
            time.sleep(0.2)

    print("📊 Sorting by AI priority formula (bounty_score * 100000 / alexa_rank)...")
    ranked = sorted(
        targets,
        key=lambda x: (x["bounty_score"] * 100000) / (x["alexa_rank"] + 1),
        reverse=True
    )

    with open(OUTPUT_FILE, "w") as f:
        for t in ranked:
            f.write(f"{t['domain']}  # {t['platform']} | Rank:{t['alexa_rank']} | Bounty:{t['bounty_score']}\n")

    print(f"✅ Sorted list saved → {OUTPUT_FILE}")
    print(f"🔥 Top 10 prioritized domains:")
    for t in ranked[:10]:
        print(f"  - {t['domain']} ({t['platform']}) | Rank:{t['alexa_rank']}")

if __name__ == "__main__":
    sort_targets()
