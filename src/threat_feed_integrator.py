import requests
import json
from datetime import datetime

CVE_URL = "https://cve.circl.lu/api/last"
BUGCROWD_FEED = "https://bugcrowd.com/programs.json"
MEMORY_FILE = "data/sentinel_memory.json"

def fetch_cve_feed(limit=50):
    """Fetch latest CVE entries from CIRCL."""
    try:
        r = requests.get(CVE_URL, timeout=15)
        data = r.json()[:limit]
        return [{"id": d["id"], "summary": d["summary"], "cvss": d.get("cvss", 0)} for d in data]
    except Exception as e:
        print(f"[WARN] CVE fetch failed: {e}")
        return []

def fetch_bugcrowd_feed(limit=50):
    """Fetch active Bugcrowd programs."""
    try:
        r = requests.get(BUGCROWD_FEED, timeout=15)
        data = r.json()["programs"][:limit]
        return [{"name": p["name"], "url": p["url"]} for p in data]
    except Exception as e:
        print(f"[WARN] Bugcrowd feed failed: {e}")
        return []

def fuse_threat_feeds():
    """Combine CVE and Bugcrowd feeds into unified intelligence file."""
    cve_data = fetch_cve_feed()
    bug_data = fetch_bugcrowd_feed()
    fused = {
        "timestamp": datetime.utcnow().isoformat(),
        "cve_feed": cve_data,
        "bugcrowd_feed": bug_data,
        "summary": f"Integrated {len(cve_data)} CVEs + {len(bug_data)} programs."
    }
    json.dump(fused, open(MEMORY_FILE.replace("memory","threat_feed"),"w"), indent=2)
    print(f"[INFO] Threat Fusion Feed Updated → {len(cve_data)} CVE + {len(bug_data)} programs")
    return fused
