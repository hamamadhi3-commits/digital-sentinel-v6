# src/threat_intel_engine.py
# Digital Sentinel v6 — STEP 8: Threat Intelligence Fusion Engine

import os
import json
import requests
from datetime import datetime

class ThreatIntelEngine:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.intel_dir = os.path.join(base_dir, "data", "intel")
        os.makedirs(self.intel_dir, exist_ok=True)
        self.shodan_api_key = os.getenv("SHODAN_API_KEY", "").strip()

    def fetch_cve_feed(self):
        print("🛰 Fetching CVE feed...")
        url = "https://cve.circl.lu/api/last"
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.json()
                path = os.path.join(self.intel_dir, "cve_feed.json")
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                print(f"✅ CVE feed saved ({len(data)} records).")
                return data
            else:
                print("⚠️ CVE feed fetch failed.")
        except Exception as e:
            print(f"❌ CVE fetch error: {e}")
        return []

    def fetch_exploitdb_feed(self):
        print("🧩 Fetching Exploit-DB feed...")
        url = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/files_exploits.csv"
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                path = os.path.join(self.intel_dir, "exploitdb_feed.csv")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(r.text)
                print("✅ Exploit-DB feed saved.")
                return True
        except Exception as e:
            print(f"❌ ExploitDB fetch error: {e}")
        return False

    def query_shodan(self, query="ssl.cert.subject.CN:*.gov"):
        if not self.shodan_api_key:
            print("⚠️ Shodan API key not set.")
            return []
        print(f"🔎 Querying Shodan: {query}")
        try:
            url = f"https://api.shodan.io/shodan/host/search?key={self.shodan_api_key}&query={query}"
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                data = r.json()
                path = os.path.join(self.intel_dir, "shodan_intel.json")
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                print(f"✅ Shodan data saved ({len(data.get('matches', []))} hosts).")
                return data.get("matches", [])
        except Exception as e:
            print(f"❌ Shodan query error: {e}")
        return []

    def fuse_intelligence(self):
        print("🧠 Fusing threat intelligence feeds...")
        summary = {
            "cve_count": 0,
            "exploits_synced": False,
            "shodan_hosts": 0,
            "timestamp": datetime.utcnow().isoformat()
        }

        cves = self.fetch_cve_feed()
        exploits = self.fetch_exploitdb_feed()
        shodan_data = self.query_shodan()

        summary["cve_count"] = len(cves)
        summary["exploits_synced"] = bool(exploits)
        summary["shodan_hosts"] = len(shodan_data)

        summary_path = os.path.join(self.intel_dir, "fusion_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        print(f"✅ Threat intelligence fusion complete → {summary_path}")
        return summary
