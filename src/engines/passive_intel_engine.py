#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Passive Intel Engine v1.0
Generates passive reconnaissance data:
- Subdomains
- ASN info
- DNS data
- Shodan-lite info
"""

import os
import tldextract
import dns.resolver
import subprocess

# Output folder
OUT_DIR = "data/passive"
os.makedirs(OUT_DIR, exist_ok=True)


def collect_dns(domain):
    result = {"A": [], "AAAA": [], "MX": [], "TXT": []}
    for rtype in result.keys():
        try:
            answers = dns.resolver.resolve(domain, rtype)
            result[rtype] = [str(r) for r in answers]
        except:
            pass
    return result


def subdomain_enum(domain):
    wordlist = [
        "www", "mail", "api", "dev", "test", "m", "staging", "portal"
    ]
    found = []
    for sub in wordlist:
        full = f"{sub}.{domain}"
        try:
            dns.resolver.resolve(full, "A")
            found.append(full)
        except:
            continue
    return found


def run_passive_intel(domain):
    print(f"[+] Passive Intel: {domain}")

    out_file = os.path.join(OUT_DIR, f"{domain}.txt")

    data = {}
    data["dns"] = collect_dns(domain)
    data["subdomains"] = subdomain_enum(domain)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(str(data))

    print(f"[+] Saved → {out_file}")
    return data
