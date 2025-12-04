# src/engines/passive_intel_engine.py
# Passive intelligence engine: performs WHOIS, DNS, and TLD extraction

import requests
import tldextract
import os
import socket


class PassiveIntelEngine:
    def __init__(self):
        self.engine_name = "PassiveIntelEngine"

    def whois_lookup(self, domain):
        """Perform WHOIS lookup using a public API (fallback if offline)."""
        try:
            api = f"https://api.api-ninjas.com/v1/whois?domain={domain}"
            headers = {"X-Api-Key": os.getenv("API_NINJAS_KEY", "")}
            r = requests.get(api, headers=headers, timeout=6)
            if r.status_code == 200:
                data = r.json()
                registrar = data.get("registrar", "Unknown")
                creation_date = data.get("creation_date", "N/A")
                return f"Registrar: {registrar}, Created: {creation_date}"
            else:
                return f"WHOIS request failed (HTTP {r.status_code})"
        except Exception as e:
            return f"WHOIS error: {e}"

    def resolve_dns(self, domain):
        """Resolve A record of domain."""
        try:
            ip = socket.gethostbyname(domain)
            return f"{domain} → {ip}"
        except Exception as e:
            return f"DNS resolution failed: {e}"

    def extract_tld(self, target):
        """Extract top-level domain info."""
        try:
            ext = tldextract.extract(target)
            return f"Domain: {ext.domain}.{ext.suffix}, Subdomain: {ext.subdomain or 'None'}"
        except Exception as e:
            return f"TLD parse error: {e}"

    def run(self, target):
        """Run all passive intel methods."""
        print(f"\n[🕵️‍♂️] Running {self.engine_name} on target: {target}")
        try:
            tld_info = self.extract_tld(target)
            print(f"  🌍 {tld_info}")

            dns_info = self.resolve_dns(target)
            print(f"  🧭 {dns_info}")

            whois_info = self.whois_lookup(target)
            print(f"  📜 {whois_info}")

            print("✅ PassiveIntelEngine completed.\n")
        except Exception as e:
            print(f"❌ PassiveIntelEngine error: {e}")
