# src/engines/passive_intel_engine.py

import requests
import tldextract
import time

class PassiveIntelEngine:
    def __init__(self):
        self.engine_name = "PassiveIntelEngine"

    def run(self, target):
        """
        Passive intel gathers:
        - WHOIS basic info
        - DNS Records
        - TLD Parsing
        """
        print(f"[+] Running Passive Intel on: {target}")

        data = {
            "domain": target,
            "tld": self._extract_tld(target),
            "dns": self._dns_lookup(target),
            "timestamp": time.time()
        }

        return data

    def _extract_tld(self, domain):
        parsed = tldextract.extract(domain)
        return {
            "subdomain": parsed.subdomain,
            "domain": parsed.domain,
            "suffix": parsed.suffix
        }

    def _dns_lookup(self, domain):
        try:
            import dns.resolver
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(domain, "A")
            return [str(r) for r in answers]
        except:
            return ["No DNS Record"]
