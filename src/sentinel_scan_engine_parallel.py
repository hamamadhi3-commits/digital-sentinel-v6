#!/usr/bin/env python3
import subprocess
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

RESULT_DIR = "data/results"
os.makedirs(RESULT_DIR, exist_ok=True)

# -------------------------------------------
# Run Subfinder
# -------------------------------------------
def run_subfinder(domain):
    try:
        out = subprocess.check_output(
            ["subfinder", "-silent", "-d", domain], stderr=subprocess.DEVNULL
        ).decode().splitlines()
        return out
    except:
        return []

# -------------------------------------------
# Run HTTPX
# -------------------------------------------
def run_httpx(domains):
    if not domains:
        return []

    try:
        p = subprocess.Popen(
            ["httpx", "-silent"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        out = p.communicate(input="\n".join(domains).encode())[0]
        return out.decode().splitlines()
    except:
        return []

# -------------------------------------------
# Run Nuclei
# -------------------------------------------
def run_nuclei(targets):
    if not targets:
        return []

    try:
        p = subprocess.Popen(
            ["nuclei", "-json", "-silent"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        raw = p.communicate(input="\n".join(targets).encode())[0].decode().splitlines()

        findings = []
        for line in raw:
            try:
                findings.append(json.loads(line))
            except:
                pass

        return findings

    except:
        return []

# -------------------------------------------
# Main Scan Function
# -------------------------------------------
def run_full_scan(domain):
    print(f"🌐 Starting scan → {domain}")

    subdomains = run_subfinder(domain)
    print(f"  ➤ Subdomains: {len(subdomains)}")

    alive = run_httpx(subdomains)
    print(f"  ➤ Alive hosts: {len(alive)}")

    vulns = run_nuclei(alive)
    print(f"  ➤ Findings: {len(vulns)}")

    return vulns
