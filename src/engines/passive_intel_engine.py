import requests
import json
import tldextract

class PassiveIntelEngine:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.api_sources = [
            "https://crt.sh/?q={domain}&output=json",
            "https://jldc.me/anubis/subdomains/{domain}"
        ]

    def fetch_crtsh(self, domain):
        try:
            url = f"https://crt.sh/?q={domain}&output=json"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return []
            data = r.json()
            subs = set()
            for item in data:
                name = item.get("name_value", "")
                if domain in name:
                    subs.add(name.replace("*.", ""))
            return list(subs)
        except:
            return []

    def fetch_anubis(self, domain):
        try:
            url = f"https://jldc.me/anubis/subdomains/{domain}"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return []
            return r.json()
        except:
            return []

    def enumerate(self, domain):
        all_subs = []

        print(f"[INTEL] 🔍 Passive enumeration → {domain}")
        all_subs += self.fetch_crtsh(domain)
        all_subs += self.fetch_anubis(domain)

        all_subs = list(set(all_subs))
        print(f"[INTEL] ✅ Found {len(all_subs)} passive subs")

        return all_subs
