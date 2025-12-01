import requests, json, os

BUGCROWD_URL = "https://api.bugcrowd.com/programs"
OUT_FILE = "data/targets/active_scopes.json"

def fetch_scopes():
    print("🔍 Fetching Bugcrowd Programs Scopes…")
    scopes = []
    # هەڵگرتنی demo data (لە وەک واقعی API پێویستە token رەسمی بێت)
    scopes.append({"program": "Tesla", "domains": ["tesla.com", "shop.tesla.com"]})
    scopes.append({"program": "Apple", "domains": ["apple.com", "developer.apple.com"]})
    os.makedirs("data/targets", exist_ok=True)
    json.dump(scopes, open(OUT_FILE, "w"), indent=2)
    print(f"✅ Saved {len(scopes)} programs to {OUT_FILE}")

if __name__ == "__main__":
    fetch_scopes()
